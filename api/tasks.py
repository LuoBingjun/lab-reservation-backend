from api.models import ReserveRecord, BreachRecord, UseRecord
from django.utils import timezone

import datetime
def update_AM():
    breach = ReserveRecord.objects.filter(date=datetime.date.today(), time='AM', checked=True)
    for item in breach:
        BreachRecord.objects.create(user=item.user, operator=item.operator, date=item.date, time=item.time, note=item.note, submit_time=item.submit_time)
    breach.delete()

    to_delete = ReserveRecord.objects.filter(date=datetime.date.today(), time='AM', checked=False)
    to_delete.delete()

    finish = UseRecord.objects.filter(start_time__contains=datetime.date.today())
    for item in finish:
        if not item.end_time:
            item.machine.avaliable = True
            item.machine.save()
            item.end_time=timezone.now()
            item.save()

def update_PM():
    breach = ReserveRecord.objects.filter(date=datetime.date.today(), time='PM', checked=True)
    for item in breach:
        BreachRecord.objects.create(user=item.user, operator=item.operator, date=item.date, time=item.time, note=item.note, submit_time=item.submit_time)
    breach.delete()

    to_delete = ReserveRecord.objects.filter(date=datetime.date.today(), time='PM', checked=False)
    to_delete.delete()

    finish = UseRecord.objects.filter(start_time__contains=datetime.date.today())
    for item in finish:
        if not item.end_time:
            item.machine.avaliable = True
            item.machine.save()
            item.end_time=timezone.now()
            item.save()

def update_Day():
    breach = ReserveRecord.objects.filter(date=datetime.date.today(), checked=True)
    for item in breach:
        BreachRecord.objects.create(user=item.user, operator=item.operator, date=item.date, time=item.time, note=item.note, submit_time=item.submit_time)
    breach.delete()

    to_delete = ReserveRecord.objects.filter(date=datetime.date.today(), checked=False)
    to_delete.delete()

    finish = UseRecord.objects.filter(start_time__contains=datetime.date.today())
    for item in finish:
        if not item.end_time:
            item.machine.avaliable = True
            item.machine.save()
            item.end_time=timezone.now()
            item.save()