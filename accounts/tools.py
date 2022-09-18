from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . import models
#from . import forms
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import random
from django.contrib.auth import login,logout,authenticate
from django.conf import settings
from accounts import models as admin_models
from django.forms.models import model_to_dict
import pytz,datetime
from django.views.decorators.csrf import ensure_csrf_cookie

def code(data):
    def code_(num):
        key=[
        ['x', 'K', '7', 'A', 'Z', '-'],
        ['U', 'd', 'B', 'w', 'i', 'C'],
        ['y', 'J', 'V', 'e', 'o', '1'],
        ['m', '_', 'f', '.', 'F', '2'],
        ['Y', 'D', 'E', 'r', 'T', '~'],
        ['t', 'O', 'z', 's', 'b', '5'],
        ['j', 'h', 'H', 'L', 'P', '3'],
        ['G', 'p', 'u', '8', 'N', 'I'],
        ['R', '0', 'l', '6', 'v', 'q'],
        ['W', 'Q', 'M', 'k', 'n', 'g']]
        ln=10
        s=[]
        while True:
            if num<=1:
                s.append(key[num][random.randint(0,5)])
                break
            t1=num//ln
            a=num%ln
            s.append(key[a][random.randint(0,5)])
            num=t1
        e=''
        for i in s[::-1]:
           e+=i
        return e
    spacer=['a', 'X', '4', 'S', 'c', '9']
    s=''
    for i in str(data):
        s+=code_(ord(i))+spacer[random.randint(0,5)]
    print(s)
    return s


def decode(data):
    key={'x': 0, 'K': 0, '7': 0, 'A': 0, 'Z': 0, '-': 0, 'U': 1, 'd': 1, 'B': 1, 'w': 1, 'i': 1, 'C': 1, 'y': 2, 'J': 2, 'V': 2, 'e': 2, 'o': 2, '1': 2, 'm': 3, '_': 3, 'f': 3, '.': 3, 'F': 3, '2': 3, 'Y': 4, 'D': 4, 'E': 4, 'r': 4, 'T': 4, '~': 4, 't': 5, 'O': 5, 'z': 5, 's': 5, 'b': 5, '5': 5, 'j': 6, 'h': 6, 'H': 6, 'L': 6, 'P': 6, '3': 6, 'G': 7, 'p': 7, 'u': 7, '8': 7, 'N': 7, 'I': 7, 'R': 8, '0': 8, 'l': 8, '6': 8, 'v': 8, 'q': 8, 'W': 9, 'Q': 9, 'M': 9, 'k': 9, 'n': 9, 'g': 9}
    spacer=['a', 'X', '4', 'S', 'c', '9']
    ln=10
    for i in spacer:
        data=data.replace(i,'#')
    data=data[:len(data)-1].split('#')
    op=''
    for i in data:
        l=0
        g=0
        for k in list(i)[::-1]:
           l+=key[k]*(ln**g)
           g+=1
        op+=chr(l)
    print(op)
    return(op)

def codetoken(id,type='User',time=1,token=''):
    return code(type+'='+code(str(id))+','+
        str(datetime.datetime.now(tz=pytz.UTC)+datetime.timedelta(days=time))+','+token)

def decodetoken(data):

    r= decode(data).split(',')
    print(r)
    r[0]=r[0].split('=')
    r[0][1]=decode(r[0][1])
    return [*r[0],r[1],r[2]]

def get_user(usertype,id,time,token):
    if usertype=='User':
        user=list(models.Users.objects.filter(id=id))
        if user!=[]:
            user=user[0]
            if user.token.token==token:
                return user
            else:
                return []
        else:
            return []
    elif usertype=='student':
        user=list(models.student.objects.filter(id=id))
        if user!=[]:
            user=user[0]
            if user.token.token==token:
                return user
            else:
                return []
        else:
            return []
    elif usertype=='librarian':
        user=list(models.libraians.objects.filter(id=id))
        if user!=[]:
            user=user[0]
            if user.token.token==token:
                return user
            else:
                return []
        else:
            return []
    else:
        return []

def beautify_variable(s):
    return s.replace('_',' ').capitalize()

def beautify_errors(*args):
    s=''
    for i in args:
        for k in i:
            s+=beautify_variable(k)+' : '+i[k][0]+'\n'
    return s


