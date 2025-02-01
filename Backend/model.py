from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.Integer,nullable=True)
    address = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    avg_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    service_professional_file = db.Column(db.String(100), nullable=True)
    service_professional_experience = db.Column(db.String(100), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey("householdservices.id", ondelete="CASCADE"), nullable=True)

    service = db.relationship("HouseholdServices", back_populates="service_professional")
    home_owner_request = db.relationship("HouseholdServicesRequest", back_populates="home_owner", foreign_keys="HouseholdServicesRequest.home_owner_id")
    service_professional_request = db.relationship("HouseholdServicesRequest", back_populates="service_professional", foreign_keys="HouseholdServicesRequest.service_professional_id")

    def convert_to_json(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "password": self.password,
            "contact_phone": self.contact_phone,
            "address": self.address,
            "pincode": self.pincode,
            "is_blocked": self.is_blocked,
            "email": self.email,
            "role": self.role,
            "is_approved": self.is_approved,
            "avg_rating": self.avg_rating,
            "rating_count": self.rating_count,
            "service_professional_file": self.service_professional_file,
            "service_professional_experience": self.service_professional_experience,
            "service_id": self.service_id
        }



class HouseholdServices(db.Model):
    __tablename__ = "householdservices"
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    time = db.Column(db.Integer, nullable=True)
    service_type = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.Integer, nullable=True)
    service_professional = db.relationship("Customer", back_populates="service", cascade="all, delete")
    requests= db.relationship("HouseholdServicesRequest", back_populates="service", cascade="all, delete-orphan")

    def convert_to_json(self):
        return {
            "id": self.id,
            "service_name": self.service_name,
            "description": self.description,
            "price": self.price,
            "time": self.time,
            "service_type": self.service_type,
            "experience": self.experience
        }

class HouseholdServicesRequest(db.Model):
    __tablename__ = "householdservicesrequest"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("householdservices.id"), nullable=False)
    home_owner_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    service_professional_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=True)
    service_status = db.Column(db.String(80), nullable=False)
    type_of_request = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    remarks = db.Column(db.String(100), nullable=True)
    date_of_request = db.Column(db.Date)
    date_of_completion = db.Column(db.Date, nullable=True)
    rating_by_home_owner = db.Column(db.Float, nullable=True)
    review_by_home_owner = db.Column(db.String(80), nullable=True)

    service = db.relationship("HouseholdServices", back_populates="requests")
    home_owner = db.relationship("Customer", back_populates="home_owner_request",foreign_keys=[home_owner_id])
    service_professional = db.relationship("Customer", back_populates="service_professional_request",foreign_keys=[service_professional_id])


    def convert_to_json(self):
        return {
            "id": self.id,
            "service_id": self.service_id,
            "home_owner_id": self.home_owner_id,
            "service_professional_id": self.service_professional_id,
            "service_status": self.service_status,
            "type_of_request": self.type_of_request,
            "description": self.description,
            "remarks": self.remarks,
            "date_of_request": self.date_of_request,
            "date_of_completion": self.date_of_completion,
            "rating_by_home_owner": self.rating_by_home_owner,
            "review_by_home_owner": self.review_by_home_owner
        }