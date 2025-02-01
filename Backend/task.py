from worker import celery
from celery.schedules import crontab
from model import Customer, HouseholdServicesRequest
from jinja2 import Template
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.mime.multipart import MIMEMultipart
import csv
import os

def send_email(email, subject, email_content,attachment=None):
    # Define email server and credentials
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "admin@hhs.com"
    sender_password = ""
    print("Email sent to", email)
    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    if email_content:
        msg.attach(MIMEText(email_content, "html"))

    if attachment:
        with open(attachment, "rb") as attachement_content:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachement_content.read())
            encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= %s" % os.path.basename(attachment))

        msg.attach(part)

    # Set up email server
    server = smtplib.SMTP(host=smtp_server_host, port=smtp_port)
    print(msg)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully")

def get_html_report(customer_name, data):
    with open('report.html', 'r') as f:
        jinja_template = Template(f.read())
        html_report = jinja_template.render(customer_name=customer_name, data=data)
        

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=22, minute=52),
        daily_reminder.s(),
        name='daily_reminder at every 6:30 pm',
    )
    sender.add_periodic_task(
        crontab(hour=22, minute=52),
        monthly_report.s(),
        name='monthly_report on the first day of every month',
    )
@celery.task
def test(arg):
    print(arg)

@celery.task
def daily_reminder():
    customers = Customer.query.filter_by(role='service_professional').all()
    for customer in customers:
        pending_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=customer.id, service_status='pending').all()
        print(pending_requests)
        if pending_requests:
            msg = f"Hi {customer.customer_name}, you have {len(pending_requests)} pending requests. Please find the details below:\n\n"
            for request in pending_requests:
                msg += f"Request ID: {request.id}\n"
                msg += f"Customer Name: {request.home_owner.customer_name}\n"
                msg += f"Service Type: {request.service.service_type}\n"
                msg += f"Date of Request: {request.date_of_request}\n"
                msg += f"Remarks: {request.remarks}\n\n"
            msg += "Please accept or reject the requests. "
            send_email(email=customer.email, email_content=msg, subject="Daily Reminder")
    print("Reminder Sent Successfully")

@celery.task
def monthly_report():
    customers = Customer.query.filter_by(role='service_professional').all()
    for customer in customers:
        total_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=customer.id).count()
        total_closed_requests = HouseholdServicesRequest.query.filter_by(service_professional_id=customer.id, service_status='closed').count()
        data = {
            'customer_name': customer.customer_name,
            'total_requests': total_requests,
            'total_closed_requests': total_closed_requests,
            'percentage_closed': (total_closed_requests / total_requests) * 100 if total_requests > 0 else 0
        }
        print(data)
        html_report = get_html_report(customer_name=customer.customer_name, data=data)
        send_email(email=customer.email, email_content=html_report, subject="Monthly Report")
    print("Report Sent Successfully")


@celery.task
def export_csv(service_details, email):
    with open('export.csv', 'w', newline='') as csvfile:
        print("service_details", service_details)
        print("email", email)
        fieldnames = ['customer_name','service_name', 'service_professional_name', 'date_of_request', 'date_of_completion', 'rating', 'remarks']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(service_details)
        send_email(email=email, subject="CSV Export", email_content="Please find the attached CSV file.", attachment="export.csv")

    return "CSV exported successfully"