from accounts.models import *
from .models import *
from rest_framework import serializers
from rest_framework.serializers import IntegerField

class SOSSerializer(serializers.ModelSerializer):
    # id = IntegerField(required=False)
    
    class Meta:
        model = SOS
        fields = ['name','mobile_number','relation']

class SOSSerializer2(serializers.ModelSerializer):
    # id = IntegerField(required=False)
    
    class Meta:
        model = SOS
        fields = ['mobile_number']

class userProfileSerializer(serializers.ModelSerializer):
    # id = IntegerField(required=False)
    
    class Meta:
        model = userProfile
        fields = ['name','dob','gender']


class SafespacesSerializer(serializers.ModelSerializer):
    id = IntegerField(required=False)
    
    class Meta:
        model = Safespaces
        fields = '__all__'


