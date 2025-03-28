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


from application.tasks import customer_bookings_monthly_report
from celery.schedules import crontab


@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):

    sender.add_periodic_task(
        crontab(minute='*/2'), 
        customer_bookings_monthly_report.s(), 
        name='customer monthly report for bookings every 2 minutes'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, hour=5, minute=30), 
        customer_bookings_monthly_report.s(), 
        name='customer monthly report for bookings every 2 minutes'
    )



if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
        debug=app.config.get("FLASK_DEBUG")
    )