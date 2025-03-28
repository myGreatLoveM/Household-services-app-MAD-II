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


from application.tasks import monthly_report
from celery.schedules import crontab


@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):


    sender.add_periodic_task(
        crontab(minute='*/2'), 
        monthly_report.s(), 
        name='monthly report every 2 minutes'
    )

    # sender.add_periodic_task(
    #     crontab(hour=15, minute=22), 
    #     add.s(1, 2), 
    #     name='add every 10'
    # )


if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
        debug=app.config.get("FLASK_DEBUG")
    )