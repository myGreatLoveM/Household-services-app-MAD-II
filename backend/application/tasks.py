import csv
import time
from celery import shared_task
from datetime import datetime
from application.providers.models import Provider
from application.customers.schemas import BookingSchema
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
            final_amount = booking_amount -commission
   
            closed_booking_csv.writerow([booking_id, service_name, customer, booking_date, closed_date, commission, booking_amount, final_amount])
    
    prov_username = provider.user.username
    message = format_report('templates/prov_closed_bookings.html')

    send_email(
        to_address=prov_username,
        subject='closed booking csv export',
        message=message,
        attachment_file=f'static/{csv_file_name}'
    )

    return csv_file_name



@shared_task(ignore_result=True, name='monthly_report')
def monthly_report():
    message = format_report('templates/index.html')
    send_email(
        to_address='test@test.com',
        subject='monthly_report',
        message=message
    )
    return 'Monthly Report sent...'

        