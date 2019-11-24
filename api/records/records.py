from rest_framework import serializers, generics
from api.models import ReserveRecord, UseRecord, BreachRecord

class ReserveSerializer(serializers.ModelSerializer):
    submit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ReserveRecord
        exclude = ['user']
        depth = 2

class QueryReserve(generics.ListAPIView):
    serializer_class = ReserveSerializer

    def get_queryset(self):
        return ReserveRecord.objects.filter(user=self.request.user)

class UseSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UseRecord
        exclude = ['user']
        depth = 2

class QueryUse(generics.ListAPIView):
    serializer_class = UseSerializer

    def get_queryset(self):
        return UseRecord.objects.filter(user=self.request.user)

class BreachSerializer(serializers.ModelSerializer):
    submit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = BreachRecord
        exclude = ['user']
        depth = 2

class QueryBreach(generics.ListAPIView):
    serializer_class = BreachSerializer

    def get_queryset(self):
        return BreachRecord.objects.filter(user=self.request.user)