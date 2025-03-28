from flask import Blueprint, jsonify, render_template, send_from_directory


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    # return {'msg': 'ok'}, 200
    return render_template('index.html')


@home_bp.route('/test')
def test():
    return {'msg': 'ok'}, 200


import os
@home_bp.route('/serve-file/<filename>')
def serve(filename):
  if os.path.exists(os.path.join('static', filename)):
    return send_from_directory(directory='static',path=filename)
  return {}, 404



# celery experiment

from celery.result import AsyncResult
from .tasks import provider_closed_bookings_csv_export, admin_closed_booking_batch_csv_export


@home_bp.route('/admin/bookings/csv-exports')
def batch_export():
  task = admin_closed_booking_batch_csv_export.delay()
  return {
     'id': task.id
  }




@home_bp.route('/exports/<int:prov_id>')
def export_bookings_csv(prov_id):
  task = provider_closed_bookings_csv_export.delay(prov_id)
  return {
    'id': task.id
  }


@home_bp.route('/downloads/<task_id>')
def send_csv_export(task_id):
  task = AsyncResult(task_id)
  return {
     'id': task.id,
     'status': task.status,
     'result': task.result
  }


  # task = closed_bookings.delay()
  # return {
  #   'id': task.id
  # }






# @home_bp.route('/api/export')
# def export_csv():
#     result = csv_report.delay()
#     return jsonify({
#         'id': result.id,
#         'result': result.result,
#         'status': result.status
#     })


# @home_bp.route('/api/csv_report/<id>')
# def download_csv_report(id):
#     result = AsyncResult(id)
#     if result.status == 'SUCCESS' and result.successful():
#         return send_from_directory(directory='templates', path='index.html')
#     return jsonify({
#         'id': result.id,
#         'ready': result.ready(),
#         'successful': result.successful(),
#         'status': result.status,
#         'value': result.result if result.ready() else None
#     })


# @home_bp.route('/mail/<email>')
# def send_mail_with(email):
#     result = send_mail_async.delay(email)
#     return jsonify({
#         'id': result.id,
#         'result': result.result
#     })


