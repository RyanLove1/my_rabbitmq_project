from rest_framework import serializers

from MyRab.models import Student, MyClass


class TestRabbitmqSer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class MyClassSer(serializers.ModelSerializer):
    class Meta:
        model = MyClass
        fields = '__all__'