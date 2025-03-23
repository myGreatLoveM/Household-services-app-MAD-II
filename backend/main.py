from application import create_app
from application.extensions import db
from application.worker import celery_init_app
from configs import DevelopmentConfig, CeleryConfig
from celery import Celery
from application.tasks import add
from celery.schedules import crontab


app = create_app(__name__, DevelopmentConfig)

celery = celery_init_app(app, CeleryConfig)

# with app.app_context():
    # from application.seed import create_initial_data
    # create_initial_data(DevelopmentConfig)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):

    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, add.s(1, 2), name='add every 10')

    sender.add_periodic_task(
        crontab(hour=15, minute=22), 
        add.s(1, 2), 
        name='add every 10'
    )


if __name__ == '__main__':
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
        debug=app.config.get("FLASK_DEBUG")
    )