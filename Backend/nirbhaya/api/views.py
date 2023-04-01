# Imports for REST api's
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings

# Imports for Google maps direction API 
import polyline
import json
import requests

# Imports for Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

# Private credentials (API Keys)
import api.secrets.secrets

# Aadhar card scan
from api.pyaadhaar.pyaadhaar.decode import AadhaarOldQr, AadhaarSecureQr


@api_view(["GET"])
@permission_classes([AllowAny])
def test(request):
    
    d = {
        'message':"Success"
    }
    return Response(d)


@api_view(["POST"])
@permission_classes([AllowAny])
def home(request):
    data = request.POST
    # data = json.loads(request.body)
    print(data)
    
    # key = secrets.apikey
    # # source = f"{data['source']['lat']}, {data['source']['lng']}"
    # # destination = f"{data['destination']['lat']}, {data['destination']['lng']}"

    # source = f"{source_lat}, {source_lng}"
    # destination = f"{dest_lat}, {dest_lng}"

    # url = f'''https://maps.googleapis.com/maps/api/directions/json?origin={source}&destination={destination}&key={key}'''
    # payload={}
    # headers = {}
    # response = requests.request("GET", url, headers=headers, data=payload)

    # overview_polygon = response.json()["routes"][0]["overview_polyline"]["points"]
    # waypoints = polyline.decode(overview_polygon, 5)
    
    waypoints = [(19.08562, 72.90911), (19.08528, 72.90858), (19.08518, 72.90843), (19.08512, 72.90851), (19.08484, 72.90877), (19.08443, 72.90902), (19.08366, 72.90919), (19.08328, 72.90917), (19.08238, 72.909), (19.07933, 72.90799), (19.07855, 72.90772), (19.07808, 72.90752), (19.07721, 72.90718), (19.07536, 72.90635), (19.07527, 72.90629), (19.07519, 72.90621), (19.07513, 72.90613), (19.0751, 72.90597), (19.07508, 72.90538), (19.07507, 72.90538), (19.07504, 72.90538), (19.07499, 72.90534), (19.07496, 72.90529), (19.07496, 72.90522), (19.07498, 72.90517), (19.07503, 72.90513), (19.07509, 72.90511), (19.07524, 72.9041), (19.07532, 72.9034), (19.07443, 72.90318), (19.07426, 72.90313), (19.07428, 72.90304), (19.07436, 72.90306), (19.07449, 72.90309), (19.07479, 72.90196), (19.07496, 72.90095), (19.07503, 72.90072), (19.07455, 72.90047), (19.07381, 72.90009), (19.07371, 72.89998), (19.07359, 72.89975), (19.07354, 72.89966), (19.07338, 72.89985), (19.07335, 72.9), (19.07331, 72.90011), (19.07328, 72.90016), (19.07317, 72.90022), (19.07296, 72.90028), (19.07274, 72.90031), (19.07261, 72.90031), (19.07255, 72.90026), (19.07249, 72.89995)]

    d = {
        'route':waypoints,
        'reports':[]
    }
    return Response(d)


@api_view(["POST"])
@permission_classes([AllowAny])
def reports(request):
    print(settings.BASE_DIR)
    cred = credentials.Certificate(os.path.join(settings.BASE_DIR,"api/secrets/fb-pk.json"))
    firebase_admin.initialize_app(cred,{
        'databaseURL' : 'https://nirbhaya-f32ba-default-rtdb.asia-southeast1.firebasedatabase.app/  '
    })
    ref = db.reference("/reports")
    ref.set({
        "Books":
        {
            "book1": {
                "name" : "This is name for book1",
                "desc" : "Blabla"
            },
            "book2": {
                "name" : "This is name for book2",
                "desc" : "Blabla"
            }
        }
    })

    d = {
        "message" : "Success"
    }
    return Response(d)


def get_qr_data(qr):
    decoded_data = decode_qr(qr)
    return decoded_data
    
def decode_qr(data):
    try:
        obj_sec = AadhaarSecureQr(int(data))
        res = obj_sec.decodeddata()
        data = {
            "name":res["name"],
            "dob":res["dob"],
            "gender":res["gender"],
        }
        return data
        
    except:
        obj_old = AadhaarOldQr(data)
        res = obj_old.decodeddata()
        data = {
            "name":res["n"],
            "dob":res["d"],
            "gender":res["g"],
        }
        return data

@api_view(["POST"])
@permission_classes([AllowAny])
def qr(request):
    # print(request.POST['data'],'a')
    res = get_qr_data(request.POST['data'])
    print("res",res)
    return Response(res)