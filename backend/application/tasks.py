import csv
import time
from celery import shared_task
from datetime import datetime
from application.extensions import db
from application.admin.models import Category
from application.providers.models import Provider, Service
from application.customers.models import Booking, Customer
from application.customers.schemas import BookingSchema
from application.providers.schemas import ServiceSchema
from .mail import send_email
from .utils import format_report


@shared_task(ignore_result=False, name='provider_closed_bookings_csv_export')
def provider_closed_bookings_csv_export(prov_id):
    provider = Provider.query.filter_by(id=prov_id).first()
    prov_services = provider.services.all()
    prov_closed_bookings = []
    booking_schema = BookingSchema(exclude=['review'])

    for service in prov_services:
        service_name = service.name
        service_bookings = service.bookings.all()

        for booking in service_bookings:
            if booking.is_closed:
                closed_booking = booking_schema.dump(booking)
                closed_booking['service'] = service_name
                prov_closed_bookings.append(closed_booking)
    
    csv_file_name = f"ProvID_{prov_id}_closed_bookings_{datetime.now().strftime('%f')}.csv" 

    with open(f'static/{csv_file_name}', 'w', newline = "") as csvfile:

        closed_booking_csv = csv.writer(csvfile, delimiter = ',')
        closed_booking_csv.writerow(['Booking ID','Service','Customer','Booking Date','Closed Date','Commission','Booking Amount','Final Amount'])

        for booking in prov_closed_bookings:
            booking_id = booking.get('id')
            service_name = booking.get('service')
            customer = booking.get('customer').get('user').get('username')
            booking_date = booking.get('book_date')
            closed_date = booking.get('closed_date')
            commission = booking.get('payment').get('commission_fee')
            booking_amount = booking.get('payment').get('amount')
            final_amount = booking_amount - commission
   
            closed_booking_csv.writerow([booking_id, service_name, customer, booking_date, closed_date, commission, booking_amount, final_amount])
    
    prov_email = provider.user.email
    message = format_report('templates/prov_closed_bookings.html')

    send_email(
        to_address=prov_email,
        subject='closed booking csv export',
        message=message,
        attachment_file=f'static/{csv_file_name}'
    )
    time.sleep(20)
    return csv_file_name



@shared_task(ignore_result=True, name='customer_bookings_monthly_report')
def customer_bookings_monthly_report():
    customers = Customer.query.filter_by(is_blocked=False).all()

    booking_schema = BookingSchema(exclude=['customer', 'review'])
    for customer in customers:
        cust_bookings = []

        cust_bookings_data = (
            db.session.query(
                Booking, Service.name, Category.name
            )
            .outerjoin(Service, Booking.service)
            .outerjoin(Provider, Service.provider)
            .outerjoin(Category, Provider.category)
            .filter(
                Booking.cust_id==customer.id
            )
            .all()
        )

        if len(cust_bookings_data) > 0:
            for booking_obj, service_name, category_name in cust_bookings_data:
                booking = booking_schema.dump(booking_obj)
                booking['service'] = service_name
                booking['category'] = category_name
                cust_bookings.append(booking)

            cust_user_details = customer.user
            cust_username = cust_user_details.username
            cust_email = cust_user_details.email

            data = {
                'username': cust_username,
                'bookings': cust_bookings
            }

            message = format_report('templates/cust_bookings_monthly_report.html', data=data)

            send_email(
                to_address=cust_email,
                subject='monthly booking report',
                message=message
            )

    return 'Monthly Report sent to all customers.....'


@shared_task(ignore_result=True, name='admin_closed_booking_batch_csv_export')
def admin_closed_booking_batch_csv_export():
    closed_bookings = Booking.query.filter_by(is_closed=True).all()
    booking_schema = BookingSchema(exclude=['review'])
    service_schema = ServiceSchema()

    csv_file_name = f"admin_closed_bookings_{datetime.now().strftime('%f')}.csv" 

    with open(f'static/{csv_file_name}', 'w', newline = "") as csvfile:

        closed_booking_csv = csv.writer(csvfile, delimiter = ',')
        closed_booking_csv.writerow(['Booking ID','Service','Category','Provider','Customer','Booking Date','Closed Date','Payment Date','Commission Fee','Platform Fee','Transaction Fee','Booking Amount','Final Amount'])

        for booking_obj in closed_bookings:
            service = service_schema.dump(booking_obj.service)
            booking = booking_schema.dump(booking_obj)

            booking_id = booking.get('id')
            service_name = service.get('name')
            category_name = service.get('provider').get('category').get('name')
            provider_name = service.get('provider').get('user').get('username')
            customer_name = booking.get('customer').get('user').get('username')
            booking_date = booking.get('book_date')
            closed_date = booking.get('closed_date')
            payment_date = booking.get('payment').get('updated_at')
            commission_fee = booking.get('payment').get('commission_fee')
            platform_fee = booking.get('payment').get('platform_fee')
            transaction_fee = booking.get('payment').get('transaction_fee')
            booking_amount = booking.get('payment').get('amount')
            final_amount = booking_amount + platform_fee + transaction_fee

            closed_booking_csv.writerow([booking_id,service_name,category_name,provider_name,customer_name,booking_date,closed_date,payment_date,commission_fee,platform_fee,transaction_fee,booking_amount,final_amount])

    message = format_report('templates/prov_closed_bookings.html')

    send_email(
        to_address='admin@househelpnow.com',
        subject='batch closed booking csv export',
        message=message,
        attachment_file=f'static/{csv_file_name}'
    )

    return csv_file_name


