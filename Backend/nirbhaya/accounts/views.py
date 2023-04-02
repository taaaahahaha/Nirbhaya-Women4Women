from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import *
import json



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def checkstatus(request):
    # Check if user is authenticated
    data = {
        'message':"You are authenticated"
    }
    return Response(data,status=status.HTTP_200_OK)



@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def login(request):

    data = request.POST
    username = data['username']
    password = data['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        token = Token.objects.get_or_create(user=user)[0].key
        # print(token)
        auth_login(request,user)

        data = {
            'message':'Success',
            'username':username,
            'token':token
        }
        
        return Response(data, status=status.HTTP_202_ACCEPTED)
        
    else:

        data = {
            'message':'Invalid credentials'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    request.user.auth_token.delete()
    auth_logout(request)
    return Response('User Logged out successfully')

 
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def signup(request):
    
    data = request.POST
    print(data,'main')
    username = data['username']
    password = data['password']
    name = data['name']
    dob = data['dob']
    gender = data['gender']

    print(data['data'], type(data['data']))
    sos = json.loads(data['data'])
    print("t")

    if User.objects.filter(username=username).exists():
        data = {
            "message":"Username Exists",
            "email":username,
            "status":False
        }
        return Response(data,status=status.HTTP_200_OK)

    user = User.objects.create_user(username=username,password=password)
    user.save()

    print('sos',sos)
    if len(sos[0]) == 1:
        ins = SOS.objects.create(
            user=user,
            name=sos[0],
            mobile_number=sos[1],
            relation=sos[2]
        )
        ins.save()
    else:
        for i in sos:  #
            print('i',i)
            ins = SOS.objects.create(
                user=user,
                name=i[0],
                mobile_number=i[1],
                relation=i[2]
            )
            ins.save()

    client = userProfile.objects.create(
        user=user,
        name=name,
        dob=dob,
        gender=gender
    )
    client.save()

    user = authenticate(username=username, password=password)

    
    token = Token.objects.get_or_create(user=user)[0].key
    # # print(token)
    auth_login(request,user)

    data = {
        "message":"User created successfully",
        "username":username,
        "token":token,
        "status":True
    }
    # print(data)
    
    return Response(data, status=status.HTTP_200_OK)

