from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.mail import mail_admins

import json
import datetime

from api.models import User, UserGroup, Operator, Machine, ReserveRecord, UseRecord
from main import settings

class QueryUsed1Serializer(serializers.Serializer):
    dates = serializers.ListField(child=serializers.DateField())

class QueryUsed2Serializer(serializers.Serializer):
    start = serializers.DateField()
    length = serializers.IntegerField()

class QueryUsed(APIView):
    def post(self, request):
        info1 = QueryUsed1Serializer(data=request.data)
        info2 = QueryUsed2Serializer(data=request.data)
        if info1.is_valid():
            dates = info1.validated_data['dates']
            res = []
            for date in dates:
                if date in settings.CLOSE_DATE:
                    AM_len = 0
                    PM_len = 0
                else:
                    AM_len = settings.OPEN_NUM - len(ReserveRecord.objects.filter(date=date, time='AM', checked=True))
                    PM_len = settings.OPEN_NUM - len(ReserveRecord.objects.filter(date=date, time='PM', checked=True))
                res.append({
                    'date' : str(date),
                    'AM': AM_len,
                    'PM': PM_len
                })
            return Response(res, status=200)
        elif info2.is_valid():
            date = info2.validated_data['start']
            length = info2.validated_data['length']
            day = datetime.timedelta(days=1)
            res=[]
            for i in range(length):
                if date in settings.CLOSE_DATE:
                    AM_len = 0
                    PM_len = 0
                else:
                    AM_len = settings.OPEN_NUM - len(ReserveRecord.objects.filter(date=date, time='AM', checked=True))
                    PM_len = settings.OPEN_NUM - len(ReserveRecord.objects.filter(date=date, time='PM', checked=True))
                res.append({
                    'date' : str(date),
                    'AM': AM_len,
                    'PM': PM_len
                })
                date += day
            return Response(res, status=200)
        else:
            return Response(info2.errors, status=400)

class OpInfoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=16)

    class Meta:
        model = Operator
        fields = ['id','name']


class SubmitSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.ChoiceField(['AM','PM'])
    operators = serializers.ListField(child=OpInfoSerializer())
    note = serializers.CharField()

class Submit(APIView):
    def post(self, request):
        info = SubmitSerializer(data=request.data)
        if info.is_valid():
            date = info.validated_data['date']
            time = info.validated_data['time']
            operators = info.validated_data['operators']
            note = info.validated_data['note']

            group = UserGroup.objects.get(user=request.user)
            occupied = ReserveRecord.objects.filter(user=request.user)
            if len(operators) + len(occupied) > group.max_reserve:
                return Response('Beyond max reserve limit', status=400)

            reserved = ReserveRecord.objects.filter(date=date, time=time)
            if len(reserved) + len(operators) <= 8:
                for op in operators:
                    operator = Operator(**op)
                    operator.save()
                    record = ReserveRecord(
                        user=request.user,
                        operator=operator,
                        date=date,
                        time=time,
                        checked=True,
                        note=note
                    )
                    record.save()
                return Response(status=200)
            else:
                return Response('Inadequate machine', status=400)
        else:
            return Response(info.errors, status=400)

class SpecialSubmitSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    operators = serializers.ListField(child=OpInfoSerializer())
    note = serializers.CharField()

class SpecialSubmit(APIView):
    def post(self, request):
        info = SpecialSubmitSerializer(data=request.data)
        if info.is_valid():
            date = info.validated_data['date']
            time = info.validated_data['time']
            operators = info.validated_data['operators']
            note = info.validated_data['note']

            for op in operators:
                operator = Operator(**op)
                operator.save()
                record = ReserveRecord(
                    user=request.user,
                    operator=operator,
                    date=date,
                    time='OT',
                    special_time=time,
                    checked=False,
                    note=note
                )
                record.save()
                mail_admins(
                    '特殊预约申请',
                    '新收到用户{0}发来的特殊预约申请，具体内容请查看\nhttp://www.lbjthu.tech:8080/admin/api/reserverecord/{1}\n申请日期：{2}'.format(request.user, record.id, record.date),
                    fail_silently=True,
                )
            return Response(status=200)
        else:
            return Response(info.errors, status=400)

class CancelSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class Cancel(APIView):
    def post(self, request):
        info = CancelSerializer(data=request.data)
        if info.is_valid():
            id = info.validated_data['id']
            record = ReserveRecord.objects.filter(user=request.user, id=id)
            if record.exists():
                record.delete()
                return Response(status=200)
            else:
                return Response('no such record', status=400)
        else:
            return Response(info.errors, status=400)

class ReserveRecordSerializer(serializers.ModelSerializer):
    submit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ReserveRecord
        fields = ['id', 'operator', 'time', 'note', 'submit_time']
        depth = 2

class QuerySigninSerializer(serializers.Serializer):
    id = serializers.DecimalField(max_digits=10, decimal_places=0)

class QuerySignin(generics.ListAPIView):
    serializer_class = ReserveRecordSerializer
    pagination_class = None
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        info = QuerySigninSerializer(data=self.request.query_params)
        if info.is_valid():
            id = info.validated_data['id']
            return ReserveRecord.objects.filter(checked=True, date=datetime.date.today(), operator__id=id)
        else:
            return []

class SigninSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class Signin(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        info = SigninSerializer(data=request.data)
        if info.is_valid():
            id = info.validated_data['id']
            records = ReserveRecord.objects.filter(pk=id)
            machines = Machine.objects.filter(available=True)
            if records.exists() and machines.exists():
                record = records[0]
                machine = machines[0]
                UseRecord.objects.create(machine=machine, user=record.user, operator=record.operator, start_time=datetime.datetime.now(), note=record.note)
                machine.available=False
                machine.save()
                record.delete()
                return Response({
                    'machine_id':machine.id
                },status=200)
            else:
                return Response('reserve record or machine error', status=400)
        else:
            return Response(info.errors, status=400)
