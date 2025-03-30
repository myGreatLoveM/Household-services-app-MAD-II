from application import create_app
from application.extensions import db
from application.worker import celery_init_app
from configs import DevelopmentConfig, CeleryConfig
from celery import Celery



app = create_app(__name__, DevelopmentConfig)

# with app.app_context():
    # from application.seed import create_initial_data
    # create_initial_data(DevelopmentConfig)

celery = celery_init_app(app, CeleryConfig)
celery.autodiscover_tasks()


from application.tasks import customer_bookings_monthly_report, provider_pending_bookings_update_status_remainder, provider_upcoming_active_bookings_remainder
from celery.schedules import crontab


@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    
    # sender.add_periodic_task(
    #     crontab(minute='*/2'), 
    #     customer_bookings_monthly_report.s(), 
    #     name='monthly report of bookings for customer every 2 minutes'
    # )

    # sender.add_periodic_task(
    #     crontab(minute='*/2'), 
    #     provider_pending_bookings_update_status_remainder.s(), 
    #     name='daily remainder for pending bookings of all provider to update status sent every 2 minutes'
    # )

    # sender.add_periodic_task(
    #     crontab(minute='*/2'), 
    #     provider_upcoming_active_bookings_remainder.s(), 
    #     name='daily remainder for upcoming active bookings of all providers sent every two minutes'
    # )

    sender.add_periodic_task(
        crontab(day_of_month=1, hour=5, minute=30), 
        customer_bookings_monthly_report.s(), 
        name='monthly report of bookings for customer on the first day of every month'
    )

    sender.add_periodic_task(
        crontab(hour='17', minute='30'), 
        provider_pending_bookings_update_status_remainder.s(), 
        name='daily remainder for pending bookings of all provider to update status sent every day at 5:30 PM'
    )

    sender.add_periodic_task(
        crontab(hour='21', minute='0'), 
        provider_upcoming_active_bookings_remainder.s(), 
        name='daily remainder for upcoming active bookings of all providers sent every day at 9:00 PM'
    )




if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
        debug=app.config.get("FLASK_DEBUG")
    )