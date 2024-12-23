from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time
import json
import random
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from .models import RoomMember
# Create your views here.


def index(request):
    return render(request, 'videochat/index.html')

def room(request):
    return render(request, 'videochat/room.html')

@csrf_exempt
def get_token(request):    
    appId= '303468ce452f4351ba2a4a199eb5c1de'
    appCertificate = '223f0bc915924236a02a2c36189cf672'
    data = json.loads(request.body)
    channelName = data['channel']


    uid = random.randint(1, 230)
    experationTimeInSeconds = 3600*24
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + experationTimeInSeconds
    role = 1
    # secondaryAppCertificate = 'aa8364af64a9406aba64bc6a58642fac' ??????


    token: str = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid':uid, 'username':request.user.username}, safe=False)




@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member , created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['uid'],
        room_name=data['room_name']
        )
    return JsonResponse({'name':data['name']}, safe=False)
    

def getMember(request):
    uid = request.GET.get('uid')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )

    return JsonResponse({'name':member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['uid'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)