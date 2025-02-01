from flask import Flask, request, jsonify, session, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import timedelta
from datetime import datetime
import json
import os
import time
from worker import celery
from werkzeug.utils import secure_filename
from flask_caching import Cache
from model import Customer, HouseholdServices, HouseholdServicesRequest, db
from task import export_csv
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
import base64
matplotlib.use('agg')

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ os.path.join(current_dir, "householdservices.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Akshay@123"
app.config["JWT_SECRET_KEY"] = "Akshay@123"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

app.config["UPLOAD_EXTENSIONS"] = [".pdf"]
app.config["UPLOAD_PATH"] = os.path.join(current_dir, "pdf")

celery.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/1",
    timezone="Asia/Kolkata"
)
cache = Cache(app)
jwt = JWTManager(app)

db.init_app(app)
# celery.init_app(app)
cache.init_app(app)
app.app_context().push() 
CORS(app, supports_credentials=True)


def create_admin():
    with app.app_context():
        admin_user = Customer.query.filter_by(role="admin").first()
        if not admin_user:
            admin_user = Customer(customer_name="admin", password="8887832", email= "admin@hhs.com", role = "admin", is_approved=True)
            db.session.add(admin_user)
            db.session.commit()
            return jsonify({"message": "Admin user created successfully", "status": "success"})
        else:
            return jsonify({"message": "Admin user already exists", "status": "error"})

with app.app_context():
    db.create_all()
    create_admin()

@jwt_required()
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the API", "status": "success"})

@cache.cached(timeout=120)
@app.route("/hhs_admin_login", methods=["GET","POST"])
def hhs_admin_login():
    data = request.get_json()
    customer_name = data.get("customer_name")
    password = data.get("password")
    admin_check = Customer.query.filter_by(role="admin").first()
    if admin_check and admin_check.password == password:
        identity = {"customer_id": admin_check.id, "role": admin_check.role}
        access_token = create_access_token(identity=json.dumps(identity))
        session["customer_name"] = customer_name
        session["role"] = "admin"
        return jsonify(
            {"message": "Successfully logged in",
             "token": access_token,
             "customer_name": customer_name,
             "role" : admin_check.role}
            ), 200
    else:
       return jsonify({"message": "Incorrect username or password"}), 401

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    customer_name = data.get("customer_name")
    password = data.get("password")
    customer_check = Customer.query.filter_by(customer_name=customer_name).first()
    

    if customer_check and password == customer_check.password:
        if customer_check.is_blocked:
            return jsonify({"error": "Your account has been blocked. Please contact the admin."}), 401

        session["customer_id"] = customer_check.id
        session["role"] = customer_check.role
        identity = {"customer_id": customer_check.id, "role": customer_check.role}
        token = create_access_token(identity=json.dumps(identity))
        if customer_check.role == "service_professional":
            if customer_check.is_approved == False:
                return jsonify({"error": "Please wait until the admin approves you."}), 401
            if customer_check.service_id == None:
                return jsonify({"error": "The service you requested is currently unavailable. Please create a new account with other service."}), 401
            return jsonify({"message": "Successfully logged in",
             "token": token,
             "customer_name": customer_name,
             "role" : customer_check.role}
            ), 200

        if customer_check.role == "home_owner":

            return jsonify({"message": "Successfully logged in",
             "token": token,
             "customer_name": customer_name,
             "role" : customer_check.role}
            ), 200

    return jsonify(
        {"error": "Login failed. Please check username and password"}), 401


@app.route("/service_professional_register", methods=["POST"])
def service_professional_register():
    customer_name = request.form.get("customer_name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    address = request.form.get("address")
    pincode = request.form.get("pincode")
    service_professional_file = request.files.get("service_professional_file")
    service_professional_experience = request.form.get("service_professional_experience")
    service_id = request.form.get("service")  # Frontend sends service ID

    # Check if username exists
    existing_customer = Customer.query.filter_by(customer_name=customer_name).first()
    if existing_customer:
        return jsonify({"error": "The username already exists. Please try another username."}), 400

    # Validate service ID
    service_record = HouseholdServices.query.get(service_id)
    if not service_record:
        return jsonify({"error": "Invalid service selected."}), 400

    # Handle file upload
    file_name = None
    if service_professional_file:
        file_extension = os.path.splitext(service_professional_file.filename)[1]
        if file_extension not in app.config["UPLOAD_EXTENSIONS"]:
            return jsonify({"error": "Only PDF files are allowed."}), 400
        file_name = secure_filename(customer_name + file_extension)
        service_professional_file.save(os.path.join(app.config["UPLOAD_PATH"], file_name))

    # Register new service professional
    new_customer = Customer(
        customer_name=customer_name,
        password=password,
        email=email,
        contact_phone=phone,
        address=address,
        pincode=pincode,
        role="service_professional",
        service_professional_file=file_name,
        service_professional_experience=service_professional_experience,
        service_id=service_id
    )
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Successfully registered. Please login to continue."}), 201


@app.route("/home_owner_register", methods=["POST"])
def home_owner_register():
    data = request.get_json()
    customer_name = data.get("customer_name")
    password = data.get("password")
    address = data.get("address")
    pincode = data.get("pincode")
    email = data.get("email")
    contact_phone = data.get("phone")

    customer_check = Customer.query.filter_by(customer_name=customer_name).first()
    if customer_check:
        return jsonify({"error": "The username already exists. Please try another username."}), 400

    customer = Customer(customer_name=customer_name, password=password, email = email,
                        contact_phone=contact_phone, address=address, pincode=pincode, is_approved=True, role="home_owner")
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "Succesfully registered. Please login to continue."}), 201

@jwt_required()
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("customer_name", None)
    session.pop("role", None)
    return jsonify({"message": "Successfully logged out"}), 200


@app.route("/get_home_owners", methods=["GET"])
def get_home_owners():
    home_owners = Customer.query.filter_by(role="home_owner").all()
    home_owner_list = [home_owner.convert_to_json() for home_owner in home_owners]
    return jsonify({"home_owners": home_owner_list}), 200


@app.route("/get_services", methods=["GET"])
def get_services():
    services = HouseholdServices.query.all()
    service_list = [service.convert_to_json() for service in services]
    return jsonify({"services": service_list}), 200

@app.route("/get_approved_service_professionals", methods=["GET"])
def get_approved_service_professionals():
    approved_service_professionals = Customer.query.filter_by(role="service_professional", is_approved=True).all()
    approved_service_professional_list = [
        {
            "id": approved_service_professional.id,
            "customer_name": approved_service_professional.customer_name,
            "address": approved_service_professional.address,
            "pincode": approved_service_professional.pincode,
            "service_professional_experience": approved_service_professional.service_professional_experience,
            "service": approved_service_professional.service.service_name,
            "contact_phone": approved_service_professional.contact_phone,
        }for approved_service_professional in approved_service_professionals]
    return jsonify({"approved_service_professionals": approved_service_professional_list}), 200
   
@app.route("/get_unapproved_service_professionals", methods=["GET"])
@jwt_required()
def get_unapproved_service_professionals():
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    unapproved_service_professionals = Customer.query.filter_by(role="service_professional", is_approved=False).all()
    unapproved_service_professional_list = [
        {
            "id": unapproved_service_professional.id,
            "customer_name": unapproved_service_professional.customer_name,
            "address": unapproved_service_professional.address,
            "pincode": unapproved_service_professional.pincode,
            "service_professional_experience": unapproved_service_professional.service_professional_experience,
            "service": unapproved_service_professional.service.service_name
        }for unapproved_service_professional in unapproved_service_professionals]
    return jsonify({"unapproved_service_professionals": unapproved_service_professional_list}), 200



# <!-- Admin Dashboard Routes -->
@app.route("/admin_dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    try:
        current_user = json.loads(get_jwt_identity())
        if current_user.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 401

        services = HouseholdServices.query.all()
        home_owners = Customer.query.filter_by(role="home_owner").all()
        unapproved_service_professionals = Customer.query.filter_by(is_approved=False, role="service_professional").all()
        approved_service_professionals = Customer.query.filter_by(is_approved=True, role="service_professional").all()
        services_json =[service.convert_to_json() for service in services]
        home_owners_json = [home_owner.convert_to_json() for home_owner in home_owners]
        unapproved_service_professionals_json=[usp.convert_to_json() for usp in unapproved_service_professionals]
        approved_service_professionals_json=[asp.convert_to_json() for asp in approved_service_professionals]
        return jsonify({
            "services": services_json,
            "home_owners": home_owners_json,
            "unapproved_service_professionals": unapproved_service_professionals_json,
            "approved_service_professionals":approved_service_professionals_json,
        }), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


@app.route("/admin_dashboard/create_service", methods=["POST"])
@jwt_required() 
def create_service():
    current_user = json.loads(get_jwt_identity())
    print(current_user)
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    print(data)
    service_name = data.get("service_name")
    description = data.get("description")
    price = data.get("price")
    service_type = data.get("service_type")
    new_service = HouseholdServices(service_name=service_name, description=description, price=price, service_type=service_type)
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service created successfully!"}), 201


@app.route("/admin_dashboard/edit_service/<int:service_id>", methods=["GET", "PUT"])
@jwt_required()
def edit_service(service_id):
    current_user = json.loads(get_jwt_identity())
    print(current_user)

    if current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    service = HouseholdServices.query.get_or_404(service_id)

    if request.method == "GET":
        service_json = service.convert_to_json()
        return jsonify({"service": service_json}), 200

    elif request.method == "PUT":
        if request.content_type != "application/json":
            return jsonify({"error": "Invalid content type"}), 415

        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400

            service.service_name = data.get("service_name", service.service_name)
            service.description = data.get("description", service.description)
            service.price = data.get("price", service.price)
            service.service_type = data.get("service_type", service.service_type)

            db.session.commit()
            return jsonify({"message": "Service updated successfully!"}), 200

        except Exception as e:
            print("Error updating service:", e)
            db.session.rollback()
            return jsonify({"error": "Failed to update service"}), 500


@app.route("/admin_dashboard/delete_service/<int:service_id>", methods=["DELETE"])
@jwt_required()
def delete_service(service_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    service = HouseholdServices.query.get_or_404(service_id)
    approved_service_professionals = Customer.query.filter_by(role="service_professional", service_id=service_id).all()
    for service_professional in approved_service_professionals:
        db.session.delete(service_professional)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully!"}), 200


@app.route("/admin_dashboard/block/<int:customer_id>", methods=["POST"])
@jwt_required()
def block(customer_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    customer = Customer.query.get_or_404(customer_id)
    customer.is_blocked = True
    db.session.commit()
    return jsonify({"message": "User blocked successfully!"}), 200


@app.route("/admin_dashboard/unblock/<int:customer_id>", methods=["POST"])
@jwt_required()
def unblock(customer_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    customer = Customer.query.get_or_404(customer_id)
    customer.is_blocked = False
    db.session.commit()
    return jsonify({"message": "User unblocked successfully!"}), 200



@app.route("/admin_dashboard/approve_service_professional/<int:request_id>", methods=["POST"])
@jwt_required()
def approve_service_professional(request_id):
    print("Request ID",request_id)
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    request = Customer.query.get_or_404(request_id)
    request.is_approved = True
    db.session.commit()
    return jsonify({"message": "Service professional request approved successfully!"}), 200



@app.route("/admin_dashboard/reject_service_professional/<int:request_id>", methods=["POST"])
@jwt_required()
def reject_service_professional(request_id):
    print("Request ID",request_id)
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    request = Customer.query.get_or_404(request_id)
    request.is_approved = False
    db.session.delete(request)
    db.session.commit()
    return jsonify({"message": "Service professional request rejected successfully!"}), 200


# @cache.cached(timeout=120)
@app.route("/admin_dashboard/view_service_professional/<int:customer_id>", methods=["GET"])
@jwt_required()
def view_service_professional(customer_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    sp = Customer.query.get_or_404(customer_id)
    print(sp)
    customer_list = [{
        "id": sp.id,
        "customer_name": sp.customer_name,
        "email": sp.email,
        "contact_phone": sp.contact_phone,
        "address": sp.address,
        "pincode": sp.pincode,
        "service": sp.service.service_name,
    } ]
    file_name = sp.service_professional_file
    file_path = os.path.join(current_dir, "static", "pdf", file_name)
    return jsonify({
        "customer": customer_list,
        "file_path": file_path,
        "file_name": file_name
    }), 200


@app.route("/admin_dashboard/summary", methods=["GET"])
@jwt_required()
def admin_summary():
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    
    home_owner_count = Customer.query.filter_by(role="home_owner").count()
    service_professional_count = Customer.query.filter_by(role="service_professional").count()
    accepted_count = HouseholdServicesRequest.query.filter_by(service_status="accepted").count()
    pending_count = HouseholdServicesRequest.query.filter_by(service_status="pending").count()
    rejected_count = HouseholdServicesRequest.query.filter_by(service_status="rejected").count()
    closed_count = HouseholdServicesRequest.query.filter_by(service_status="closed").count()
    
    request_count_sum = accepted_count + pending_count + rejected_count + closed_count

    img_dir = os.path.join(current_dir, "img")
    os.makedirs(img_dir, exist_ok=True)

    img_1_path = os.path.join(img_dir, "img_1.png")
    categories = ["Home Owner", "Service Professional"]
    user_count = [home_owner_count, service_professional_count]

    try:
        plt.figure(figsize=(8, 6))
        sns.barplot(x=categories, y=user_count)
        plt.title("No of users by categories")
        plt.xlabel("Categories")
        plt.ylabel("Count")
        plt.savefig(img_1_path, format="png")
    finally:
        plt.close()

    try:
        with open(img_1_path, "rb") as image_file:
            img_1_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        img_1_base64 = ""

    img_2_path = os.path.join(img_dir, "img_2.png")

    if request_count_sum != 0:
        try:
            plt.figure(figsize=(8, 6))
            plt.pie([accepted_count, pending_count, rejected_count, closed_count],
                    labels=["Accepted", "Pending", "Rejected", "Closed"],
                    autopct="%1.1f%%",
                    colors=["lightgreen", "yellow", "red", "lightblue"])
            plt.title("Status of Requests")
            plt.savefig(img_2_path, format="png")
        finally:
            plt.close()

        try:
            with open(img_2_path, "rb") as image_file:
                img_2_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            img_2_base64 = ""
    else:
        img_2_base64 = ""

    return jsonify({
        "home_owner_count": home_owner_count,
        "service_professional_count": service_professional_count,
        "accepted_count": accepted_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count,
        "closed_count": closed_count,
        "img_1": img_1_base64,
        "img_2": img_2_base64
    }), 200


@app.route("/admin_dashboard/search", methods=["POST"])
@jwt_required()
def admin_search():
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    search_by = data.get("search_by")
    search_term = data.get("search_term")

    if search_by and search_term:
        if search_by == "customer_name":
            customers = Customer.query.filter(Customer.customer_name.like("%" + search_term + "%")).all()
            customer_json = []
            for customer in customers:
                customer_json.append(customer.convert_to_json())
            return jsonify({"home_owners": customer_json}), 200
        elif search_by == "service_name":
            services = HouseholdServices.query.filter(HouseholdServices.service_name.like("%" + search_term + "%")).all()
            service_json = []
            for service in services:
                service_json.append(service.convert_to_json())
            return jsonify({"services": service_json}), 200
        elif search_by == "service_professional_name":
            approved_service_professionals = Customer.query.filter(Customer.customer_name.like("%" + search_term + "%")).all()
            approved_service_professional_json = []
            for asp in approved_service_professionals:
                approved_service_professional_json.append(asp.convert_to_json())
            return jsonify({"approved_service_professionals": approved_service_professional_json}), 200

    return jsonify({"error": "Invalid search parameters"}), 400

# @cache.cached(timeout=120)
@app.route('/home_owner_dashboard', methods=['GET'])
@jwt_required()
def home_owner_dashboard():
    current_user = json.loads(get_jwt_identity())
    id = current_user["customer_id"]
    if  current_user.get("role") != "home_owner":
        return jsonify({"message" : "Access denied"}), 401
    homeowner = Customer.query.filter_by(id=id).first()
    services = HouseholdServices.query.join(Customer).filter(Customer.is_approved == True).all()
    services_list = [{
        "id": service.id,   
        "service_name": service.service_name,
        "description": service.description,
        "price": service.price,
        "time": service.time,
        "service_type": service.service_type,
        "experience": service.experience,
    } for service in services]
    service_history = HouseholdServicesRequest.query.filter_by(home_owner_id=homeowner.id).filter(HouseholdServicesRequest.service_professional_id.is_not(None)).all()
    print(service_history)
    customer_name = homeowner.customer_name
    service_history_list=[{
            "id": request.id,
            "service_id": request.service_id,
            "service_professional": request.service_professional.customer_name,
            "service_name": request.service.service_name,
            "home_owner_id": request.home_owner_id,
            "service_professional_id": request.service_professional_id,
            "service_status": request.service_status,
            "type_of_request": request.type_of_request,
            "description": request.description,
            "remarks": request.remarks,
            "date_of_request": request.date_of_request.isoformat(),
            "date_of_completion": request.date_of_completion.isoformat() if request.date_of_completion else None,
            "rating_by_home_owner": request.rating_by_home_owner,
            "review_by_home_owner": request.review_by_home_owner
    } for request in service_history]
    return jsonify({
        'services': services_list,
        'service_history':service_history_list,
        'customer_name': customer_name
    })


@app.route('/home_owner_dashboard/create_request/<int:service_id>', methods=[ 'GET','POST'])
@jwt_required()
def create_request(service_id):
    current_user = json.loads(get_jwt_identity())
    id = current_user["customer_id"]
    if  current_user.get("role") != "home_owner":
        return jsonify({"message" : "Access denied"}), 401
    
    if request.method == 'GET':
        service = HouseholdServices.query.get(service_id)
        service_name = service.service_name
        service_professionals = Customer.query.filter_by(service_id=service_id).all()
        service_professionals_list = [{
            'id': service_professional.id,
            'customer_name': service_professional.customer_name
        } for service_professional in service_professionals]
        return jsonify({
            'service_name': service_name,
            'service_professionals': service_professionals_list
        }), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        service_professional_id = data.get('service_professional_id')
        description = data.get('description')
        homeowner = Customer.query.filter_by(id=id).first()
        service = HouseholdServices.query.get(service_id)
        service_name = service.service_name
        new_request = HouseholdServicesRequest(service_id=service_id, home_owner_id=homeowner.id,
                                                service_professional_id=service_professional_id, description=description,
                                                service_status="pending", type_of_request="private", date_of_request=datetime.now())
        db.session.add(new_request)
        db.session.commit()
        return jsonify({
            'message': 'Service request created successfully!',
        }), 201


@app.route('/home_owner_dashboard/edit_request/<int:service_request_id>', methods=['GET', 'PUT'])
@jwt_required()
def edit_request(service_request_id):
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "home_owner":
        return jsonify({"message": "Access denied"}), 401
    service_request = HouseholdServicesRequest.query.get_or_404(service_request_id)
    print(service_request)
    if request.method == 'GET':
        service_professionals = service_request.service_professional.customer_name
        return jsonify({
            'description': service_request.description,
            'service_name': service_request.service.service_name,
            'service_professional': service_professionals
        }), 200

    elif request.method == 'PUT':
        data = request.get_json()
        description = data.get('description')
        service_request.description = description
        db.session.commit()
        return jsonify({'message': 'Service updated successfully!'}), 200


@app.route("/home_owner_dashboard/delete_request/<int:service_request_id>", methods=["DELETE"])
@jwt_required()
def delete_request(service_request_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "home_owner":
        return jsonify({"message" : "Access denied"}), 401
    service_request = HouseholdServicesRequest.query.get_or_404(service_request_id)
    db.session.delete(service_request)
    db.session.commit()
    return jsonify({'message': 'Service request deleted successfully!'}), 200

@app.route("/home_owner_dashboard/search", methods=["POST"])
@jwt_required()
def home_owner_search():
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "home_owner":
        return jsonify({"message" : "Access denied"}), 401
    data = request.get_json()
    search_by = data.get("search_by")
    search_term = data.get("search_term")
    if search_by and search_term:
        if search_by == "pincode":
            services = HouseholdServices.query.join(Customer).filter(Customer.is_approved == True, Customer.pincode.like("%"+search_term+"%")).all()
        elif search_by == "address":
            services = HouseholdServices.query.join(Customer).filter(Customer.is_approved == True, Customer.address.like("%"+search_term+"%")).all()
        elif  search_by == "service_name":
            services = HouseholdServices.query.join(Customer).filter(Customer.is_approved == True, HouseholdServices.service_name.like("%"+search_term+"%")).all()
    
    else:
        services = HouseholdServices.query.join(Customer).filter(Customer.is_approved == True).all()
    service_list =[{
        'id': service.id,
        'service_name': service.service_name,
        'description': service.description,
        'price': service.price,
        'service_type': service.service_type, 
    } for service in services]
    return jsonify({
        'services': service_list,
    }), 200


@app.route("/home_owner_dashboard/close_request/<int:service_request_id>", methods=["POST"])
@jwt_required()
def close_request(service_request_id):
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "home_owner":
        return jsonify({"message": "Access denied"}), 401

    service_request = HouseholdServicesRequest.query.get_or_404(service_request_id)
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    rating = data.get("rating")
    review = data.get("review")
    if not rating or not review:
        return jsonify({'error': 'Rating and review are required'}), 400

    service_request.service_status = "closed"
    service_request.rating_by_home_owner = int(rating)
    service_request.review_by_home_owner = review
    service_request.date_of_completion = datetime.now()

    sp_rating_update = Customer.query.get(service_request.service_professional_id)
    if sp_rating_update:
        r = sp_rating_update.rating_count
        sp_rating_update.rating_count = sp_rating_update.rating_count + 1
        sp_rating_update.avg_rating = (sp_rating_update.avg_rating * r + int(rating)) / (sp_rating_update.rating_count)

    db.session.commit()
    return jsonify({'message': 'Request closed successfully!'}), 200

@app.route("/home_owner_dashboard/create_open_request/<int:service_id>", methods=["POST"])
@jwt_required()
def create_open_request(service_id):
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "home_owner":
        return jsonify({"message": "Access denied"}), 401
    id = current_user["customer_id"]
    home_owner_id = id
    request = HouseholdServicesRequest(home_owner_id=home_owner_id, service_id=service_id, type_of_request="public", service_status="pending", date_of_request=datetime.now())
    db.session.add(request)
    db.session.commit()
    return jsonify({'message': 'Request sent successfully! to all the service professionals related to this service'}), 200


@app.route("/home_owner_dashboard/bidding_requests", methods=["GET"])
@jwt_required()
def bidding_requests():
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "home_owner":
        return jsonify({"message": "Access denied"}), 401
    id = current_user["customer_id"]
    name = Customer.query.filter_by(id=id).first().customer_name
    home_owner_id = id
    print(home_owner_id)
    requests = HouseholdServicesRequest.query.filter_by(service_status="pending", type_of_request="public", home_owner_id=home_owner_id).filter(HouseholdServicesRequest.service_professional_id.is_not(None)).all()
    requests_list = [{
        "id": request.id,
        "service_name": request.service.service_name,   
        "service_professional_name": request.service_professional.customer_name,
        "service_professional_id": request.service_professional_id,
        "service_professional_address": request.service_professional.address,
        "service_professional_contact": request.service_professional.contact_phone,
        "service_professional_email": request.service_professional.email,
        "date_of_request": request.date_of_request,
        "date_of_completion": request.date_of_completion,
        "service_status": request.service_status,
        "rating": request.rating_by_home_owner,
        "review": request.review_by_home_owner,
        "type_of_request": request.type_of_request,
        "home_owner_id": request.home_owner_id,
    } for request in requests]
    return jsonify({"requests": requests_list,
                    "customer_name" : name}), 200


@app.route("/home_owner_dashboard/accept_bid/<int:request_id>", methods=["PUT"])
@jwt_required()
def accept_bid_home_owner(request_id):
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "home_owner":
        return jsonify({"message": "Access denied"}), 401
    requests = HouseholdServicesRequest.query.filter_by(id=request_id).first()
    requests.service_status = "accepted"
    old_request = HouseholdServicesRequest.query.filter_by(home_owner_id=requests.home_owner_id, type_of_request="public", service_id=requests.service_id, service_status="pending").all()
    for n in old_request:
        db.session.delete(n)
    db.session.commit()
    return jsonify({'message': 'Bid accepted successfully!'}), 200


@app.route("/home_owner_dashboard/reject_bid/<int:request_id>", methods=["DELETE"])
@jwt_required()
def reject_bid_homeowner(request_id):
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "home_owner":
        return jsonify({"message": "Access denied"}), 401
    requests = HouseholdServicesRequest.query.filter_by(id=request_id).first()
    db.session.delete(requests)
    db.session.commit()
    return jsonify({'message': 'Bid rejected successfully!'}), 200



# <Service Professional Dashboard Routes>

# @cache.cached(timeout=120)
@app.route("/service_professional_dashboard", methods=["GET"])
@jwt_required()
def service_professional_dashboard():
    current_user = json.loads(get_jwt_identity())
    id = current_user["customer_id"]
    customer_name = Customer.query.filter_by(id=id).first().customer_name
    if  current_user.get("role") != "service_professional":
        return jsonify({"message" : "Access denied"}), 401
    
    sid = Customer.query.filter_by(customer_name=customer_name).first().id
    service_professional = Customer.query.filter_by(id=sid).first()
    if service_professional.is_approved == False:
        return jsonify({"message": "Please wait until the admin approves you.", "status": "warning"}), 403
    
    pending_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=sid, service_status="pending", type_of_request="private").all()
    pending_requests_list = [{
        'id': request.id,
        'home_owner_name': request.home_owner.customer_name,
        'service_name': request.service.service_name,
        'description': request.service.description, 
        'price': request.service.price,
        'date_of_request': request.date_of_request,
        'address': request.home_owner.address
    } for request in pending_requests]

    accepted_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=sid, service_status="accepted").all()
    accepted_requests_list = [{
        'id': request.id,
        'home_owner_name': request.home_owner.customer_name,
        'service_name': request.service.service_name,
        'description': request.service.description, 
        'price': request.service.price,
        'date_of_request': request.date_of_request,
        'address': request.home_owner.address
    } for request in accepted_requests]
    closed_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=sid, service_status="closed").all()
    closed_requests_list = [{
        'id': request.id,
        'home_owner_name': request.home_owner.customer_name,
        'service_name': request.service.service_name,
        'description': request.service.description, 
        'price': request.service.price,
        'rating': request.rating_by_home_owner,
        'review': request.review_by_home_owner,
        'date_of_request': request.date_of_request,
        'address': request.home_owner.address
    }for request in closed_requests]
    return jsonify({
        "pending_requests": pending_requests_list,
        "accepted_requests": accepted_requests_list,
        "closed_requests": closed_requests_list,
        "customer_name": customer_name
    })


@app.route("/service_professional_dashboard/open_requests_service_professional", methods=["GET"])
@jwt_required()
def open_requests_service_professional():
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "service_professional":
        return jsonify({"message": "Access denied"}), 401
    id = current_user["customer_id"]
    sp = Customer.query.filter_by(id=id).first().customer_name
    service_professional = Customer.query.filter_by(customer_name=sp).first()
    received_requests = HouseholdServicesRequest.query.filter_by(service_status="pending", type_of_request="public", service_id=service_professional.service_id).filter(HouseholdServicesRequest.service_professional_id == None).all()
    sent_requests = HouseholdServicesRequest.query.filter_by(service_status="pending", type_of_request="public", service_id=service_professional.service_id, service_professional_id=service_professional.id).all()
    received_request_list = [{
        'id': request.id,
        'home_owner_name': request.home_owner.customer_name,
        'service_name': request.service.service_name,
        'description': request.service.description, 
        'price': request.service.price,
        'date_of_request': request.date_of_request,
        'address': request.home_owner.address
    } for request in received_requests]
    sent_request_list = [{
        'id': request.id,
        'home_owner_name': request.home_owner.customer_name,
        'service_name': request.service.service_name,
        'description': request.service.description, 
        'price': request.service.price,
        'date_of_request': request.date_of_request,
        'address': request.home_owner.address
    }for request in sent_requests]
    return jsonify({
        "received_requests": received_request_list,
        "sent_requests": sent_request_list,
        "customer_name": sp 
    }), 200

@app.route("/service_professional_dashboard/bid_request/<int:request_id>", methods=["POST"])
@jwt_required()
def bid_request(request_id):
    current_user = json.loads(get_jwt_identity())
    if current_user.get("role") != "service_professional":
        return jsonify({"message": "Access denied"}), 401
    id = current_user["customer_id"]
    description = request.json.get("description")
    spid = id
    service_id = Customer.query.filter_by(id=spid).first().service_id
    home_owner_id = HouseholdServicesRequest.query.filter_by(id=request_id).first().home_owner_id
    new_request = HouseholdServicesRequest(home_owner_id=home_owner_id, service_id=service_id, service_professional_id=spid, type_of_request="public", service_status="pending", description=description, date_of_request=datetime.now())
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'message': 'Bid request sent successfully!'}), 200

@app.route("/service_professional_dashboard/accept_request/<int:request_id>", methods=["POST"])
@jwt_required()
def accept_request(request_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "service_professional":
        return jsonify({"message" : "Access denied"}), 401
    
    request = HouseholdServicesRequest.query.get(request_id)
    if request is None:
        return jsonify({"message": "Request not found", "status": "error"}), 404
    
    request.service_status = "accepted"
    db.session.commit()
    return jsonify({"message": "Request accepted successfully!", "status": "success"})



@app.route("/service_professional_dashboard/reject_request/<int:request_id>", methods=["POST"])
@jwt_required()
def reject_request(request_id):
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "service_professional":
        return jsonify({"message" : "Access denied"}), 401
    
    request = HouseholdServicesRequest.query.get(request_id)
    if request is None:
        return jsonify({"message": "Request not found", "status": "error"}), 404
    
    request.service_status = "rejected"
    db.session.commit()
    return jsonify({"message": "Request rejected successfully!", "status": "warning"})





@app.route("/data_export", methods=["GET"])
@jwt_required()
def data_export():
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "service_professional":
        return jsonify({"message" : "Access denied"}), 401
    service_professional = Customer.query.filter_by(id = current_user.get("customer_id")).first()
    sid = service_professional.id
    closed_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=sid, service_status="closed").all()
    if service_professional:
        request_details = [{
                    'customer_name': request.home_owner.customer_name,'service_name': request.service.service_name,
                    'service_professional_name': request.service_professional.customer_name,'date_of_request': request.date_of_request,
                    'date_of_completion' : request.date_of_completion,'rating' : request.rating_by_home_owner,
                    'remarks': request.review_by_home_owner
            } for request in closed_requests]
        export_csv(request_details, service_professional.email)
        return jsonify({"message":"You data export task has been initiated. Please check your inbox,"}), 200
    
    
@app.route("/closed_requests", methods=["GET"])
@jwt_required()
def closed_requests():
    current_user = json.loads(get_jwt_identity())
    if  current_user.get("role") != "service_professional":
        return jsonify({"message" : "Access denied"}), 401
    service_professional = Customer.query.filter_by(id = current_user.get("customer_id")).first()
    print(service_professional.id)
    closed_requests = HouseholdServicesRequest.query.filter_by(service_professional_id = current_user.get("customer_id"),service_status='closed').all()
    if service_professional:
        request_details = [{
                    'customer_name': request.home_owner.customer_name,'service_name': request.service.service_name,
                    'service_professional_name': request.service_professional.customer_name,'date_of_request': request.date_of_request,
                    'date_of_completion' : request.date_of_completion,'rating' : request.rating_by_home_owner,
                    'remarks': request.review_by_home_owner
            } for request in closed_requests]
         
    return jsonify({"closed_requests": request_details,
                   "customer_name": service_professional.customer_name}),200

@app.route('/test_cache')
@cache.cached(timeout=10)
def test_cache():
    time.sleep(5)
    return f"Test is working {time.localtime()}"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)