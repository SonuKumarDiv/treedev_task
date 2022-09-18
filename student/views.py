from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.db.models import Q
from accounts import models as ac_models
from . import models

from . import serializers
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize
import datetime
import secrets
from django.core.mail import send_mail
import secrets
import bcrypt
import time
from jose import jwt
from accounts.tools import code, decode, codetoken, decodetoken, get_user, beautify_errors

def is_authenticate(*Dargs,**Dkwargs):
    def inner(fun):
        def wrapper(*args,**kwargs):
            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=decodetoken(args[1].META['HTTP_AUTHORIZATION'])
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)

                if len(data)==4 and time>datetime.datetime.now():
                    uzr= get_user(*data)
                    if uzr!=[]:
                        if uzr.is_user_blocked :
                            return Response({'success':'false','error_msg':'USER BLOCKED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        
                        return fun(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            # return fun(*args,**kwargs)
        return wrapper
    return inner


def get_JWT(request):
    data=decodetoken(request.META['HTTP_AUTHORIZATION'])
    requstuser=get_user(*data)
    payload = {
        'name': requstuser.username,
        'email': requstuser.email,
        'iat': int(time.time()), #datetime.datetime.now() - datetime.timedelta(minutes=1),
        'external_id': "pro-"+requstuser.id,
        'exp': int(time.time()) + 3000#datetime.datetime.now() + datetime.timedelta(minutes=5)
        }
    token = jwt.encode(payload, 'C47D02EDD664451E50C908A3FFE36D3A6978953A41418D012B8B656370D05168')
    return HttpResponse(token, content_type="text/plain")

class get_own_barrowed_book_list(APIView):

    @is_authenticate(all_books_borrowed=True)
    def post(self,request):
        data=decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=get_user(*data)
        try:
            
                book=list(ac_models.library_info.objects.filter(book_issu_by=requstuser))
                if book==[]:
                    return Response({'success':'false',
                                    'error_msg':'book data not found ',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
                f1=serializers.show_lib_data(book,many=True)
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"result":f1.data},
                                    },status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'success':'false',
                                'error_msg':'invalid book id ',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class get_book_data_from_partculer_library(APIView):
    #@is_authenticate(all_books_borrowed=True)
    def post(self,request,id):
        data=decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=get_user(*data)
        try:
                book=list(ac_models.library_info.objects.filter(id=id,book_issu_by=requstuser))
                if book==[]:
                    return Response({'success':'false',
                                    'error_msg':'book data not found ',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
                f1=serializers.show_lib_data(book,many=True)
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"result":f1.data},
                                    },status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'success':'false',
                                'error_msg':'invalid book id ',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class return_book_from_a_library(APIView):   
    @is_authenticate()    
    def put(self, request):
        # try:
            # data=decodetoken(request.META['HTTP_AUTHORIZATION'])
            # requstuser=get_user(*data)
            lib=ac_models.library_info.objects.get(pk=int(request.POST["lib_id"]))
            print('llllllll',lib)
            book_details=ac_models.Book_details.objects.get(pk=int(request.POST["book_id"]))
            print('llllllll',book_details)
            # book=book[0]
            
            exist = list(lib.book_details.all())
            print('llllllll',book_details)
            if(book_details not in exist):
                return Response({'success':'false',
                                'error_msg':"boo already removed",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            lib.book_details.remove(book_details)
            lib.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        # except  Exception as ex:
        #     return Response({'success':'false',
        #                         'error_msg':"book or lib does not exists",
        #                         'errors':{},
        #                         'response':{}
        #                         },status=status.HTTP_400_BAD_REQUEST)
