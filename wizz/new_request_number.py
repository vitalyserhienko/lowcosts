from .models import Price
import datetime


def new_request_number():
  last_request_number = Price.objects.all().order_by('id').last()
  if not last_request_number:
    return 'RQ' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
  request_id = last_request_number.request_id
  request_int = int(request_id[8:12])
  new_request_int = request_int + 1
  new_request_id = 'RQ' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_request_int).zfill(4)
  return new_request_id
