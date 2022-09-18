
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import random
from django.db.models import Q
from library import models as lib_models
import pytz,datetime
import secrets
import bcrypt
from google.auth.transport import requests
from google.oauth2 import id_token

import jwt
from .tools import codetoken, decodetoken, get_user,beautify_errors
def login_admin(userid,token=''):
    token=codetoken(userid,type='User',token=token)
    return token
def logout_admin(token):
    try:
        data=decodetoken(token)
        uzr=list(models.Users.objects.filter(id=data[1]))

        if uzr!=[]:
            uzr=uzr[0]
            uzr.token.token=''
            uzr.token.save()
            return True
        else:
            return False
    except Exception as e:
        return False

def login_provider(userid,token=''):
    token=codetoken(userid,type='librarian',token=token)
    return token
def logout_provider(token):
    try:
        data=decodetoken(token)
        uzr=list(models.libraians.objects.filter(id=data[1]))

        if uzr!=[]:
            uzr=uzr[0]
            uzr.token.token=''
            uzr.token.save()
            return True
        else:
            return False
    except Exception as e:
        return False

def login_consumer(userid,token=''):
    token=codetoken(userid,type='student',token=token)
    return token
def logout_consumer(token):
    try:
        data=decodetoken(token)
        uzr=list(models.student.objects.filter(id=data[1]))

        if uzr!=[]:
            uzr=uzr[0]
            uzr.token.token=''
            uzr.token.save()
            return True
        else:
            return False
    except Exception as e:
        return False


def login_not_required(*ag,**kg):
    def inner(func):
        def wrapper(*args,**kwargs):
            if 'HTTP_AUTHORIZATION'not in args[1].META :
                return func(*args,**kwargs)
            else:
                
                if args[1].META['HTTP_AUTHORIZATION']=='':
                    return func(*args,**kwargs)
                else:
                    return Response({'success':'false','error_msg':'USER IS LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'USER IS LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)

        return wrapper
    return inner
def login_required(*ag,**kg):
    def inner(func):
        def wrapper(*args,**kwargs):
            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=decodetoken(args[1].META['HTTP_AUTHORIZATION'])
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                if len(data)==4 and time>datetime.datetime.now():
                    uzr= get_user(*data)
                    if uzr!=[]:
                        if uzr.token.token=='':
                            return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            return func(*args,**kwargs)
        return wrapper
    return inner

from django.core.serializers import serialize
##ADMIN-----------------
class login_admin_api(APIView):
    @login_not_required()
    def get(self,request):
        f1=serializers.userlogin()
        return Response(f1.data,status=status.HTTP_202_ACCEPTED)

    @login_not_required()
    def post(self,request):
        f1=serializers.userlogin(data=request.data)
        if (f1.is_valid()):
            user=list(models.Users.objects.filter(email=request.POST['email']))
            print('hiiiiii',user)
            if user!=[]:
                user=user[0]
                print('hiiiiii',user)
            else:
                return Response({'success':'false',
                                    'error_msg':'User does not exist',
                                    'errors':'Invalid email',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)

            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                print(request.session.session_key,'\n-=-',request.META)
                print(request.COOKIES)
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token.token=sec
                user.token.save()
                re=login_admin(user.id,token=sec)
                
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':serialize('json', [user]),},
                                    'token':re,
                                },status=status.HTTP_202_ACCEPTED)

            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),

                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'log_in_parameters_not_correct',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class logout_api(APIView):
    @login_required()
    def get(self,request):
        val=logout_admin(request.META['HTTP_AUTHORIZATION'])
        if val:
            return Response({'success':'true',
            'error_msg':'',
            'response':{},

            },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                'error_msg':'Logout fail',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class login_student_api(APIView):
    @login_not_required()
    def get(self,request):
        f1=serializers.userlogin()
        return Response(f1.data,status=status.HTTP_202_ACCEPTED)

    @login_not_required()
    def post(self,request):
        f1=serializers.userlogin(data=request.data)
        if (f1.is_valid()):
            user=list(models.student.objects.filter(email=request.POST['email']))
            print('hiiiiii',user)
            if user!=[]:
                user=user[0]
                print('hiiiiii',user)
            else:
                return Response({'success':'false',
                                    'error_msg':'User does not exist',
                                    'errors':'Invalid email',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)

            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                print(request.session.session_key,'\n-=-',request.META)
                print(request.COOKIES)
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token.token=sec
                user.token.save()
                re=login_consumer(user.id,token=sec)
                #login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':serialize('json', [user]),},
                                    'token':re,
                                    # 'auth':{'sessionid':request.session.session_key,
                                    #         'csrftoken':request.META['CSRF_COOKIE']


                                },status=status.HTTP_202_ACCEPTED)

            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),

                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'log_in_parameters_not_correct',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class logout_student_api(APIView):
    @login_required()
    def get(self,request):
        val=logout_consumer(request.META['HTTP_AUTHORIZATION'])
        if val:
            return Response({'success':'true',
            'error_msg':'',
            'response':{},

            },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                'error_msg':'Logout fail',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class login_librarian_api(APIView):
    @login_not_required()
    def get(self,request):
        f1=serializers.userlogin()
        return Response(f1.data,status=status.HTTP_202_ACCEPTED)

    @login_not_required()
    def post(self,request):
        f1=serializers.userlogin(data=request.data)
        if (f1.is_valid()):
            user=list(models.libraians.objects.filter(email=request.POST['email']))
            print('hiiiiii',user)
            if user!=[]:
                user=user[0]
                print('hiiiiii',user)
            else:
                return Response({'success':'false',
                                    'error_msg':'User does not exist',
                                    'errors':'Invalid email',
                                    'response':{},

                                },status=status.HTTP_400_BAD_REQUEST)

            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                print(request.session.session_key,'\n-=-',request.META)
                print(request.COOKIES)
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token.token=sec
                user.token.save()
                re=login_provider(user.id,token=sec)
                
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':serialize('json', [user])},
                                    'token':re,
                                    


                                },status=status.HTTP_202_ACCEPTED)

            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),

                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'log_in_parameters_not_correct',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class logout_librarian_api(APIView):
    @login_required()
    def get(self,request):
        val=logout_provider(request.META['HTTP_AUTHORIZATION'])
        if val:
            return Response({'success':'true',
            'error_msg':'',
            'response':{},

            },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                'error_msg':'Logout fail',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)


def genrate_pass():
    passw=''
    for i in range(10):
        passw+=secrets.choice([
        secrets.choice([chr(ii) for ii in range(48,57)]),
        secrets.choice([chr(ii) for ii in range(65,90)]),
        secrets.choice([chr(ii) for ii in range(91,112)]),
        secrets.choice(['!','@','#','$','%','^','&','*']),
                        ])
    return str(passw)

class signup_super_user(APIView):
    def get(self,request):
        f0=serializers.password()
        f1=serializers.create_users_form()

        return Response({**f1.data,**f0.data
                            },status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        f1=serializers.create_users_form(data=request.POST)
       
        if f1.is_valid():
            
           
            check_list = list(models.Users.objects.filter((Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number']))|
                                                                        Q(email=request.POST['email'])))
            #check_list = list(models.Providers.objects.filter(Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number'])))                                                            
            del_acc=[]
            if check_list != []:
                for i in check_list:
                    #check_list = list(models.Providers.objects.filter(Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number'])))
                    if i.country_code==request.POST['country_code'] and i.phone_number==request.POST['phone_number'] and i.is_verified==True:
                        return Response({'success':'false',
                                        'error_msg':'This phone number already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                    elif i.email==request.POST['email'] and i.is_verified==True:
                        return Response({'success':'false',
                                        'error_msg':'This email already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                    else:
                        del_acc.append(i)
            if del_acc!=[]:
                for i in del_acc:
                    i.delete()
            sec=''
            for i in range(5):
                sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

            try:
                user=f1.save()
                uzr=models.Users()
                uzr.username=request.POST['username']
                uzr.address=request.POST['address']
                uzr.country_code=request.POST['country_code']
                uzr.phone_number=request.POST['phone_number']
                uzr.email=request.POST['email']
                uzr.is_verified=True
                uzr.otp=sec
                uzr.save()
                password=request.POST['password'].encode('utf-8')
                uzr.password=bcrypt.hashpw(password,bcrypt.gensalt())
                uzr.password=uzr.password.decode("utf-8")
                uzr.save()
                # tem= lib_models.authorizations()
                # tem.user=user
                # tem.CURD_library=True
                # tem.create_librarian=True
                # tem.delete_librarian=True
                # tem.save()
                uzr_token=models.users_token(users=uzr,token=sec)
                uzr_token.save()
                return Response({'success':'True',
                                'error_msg':"",
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'success':'false',
                                'error_msg':"Something Bad happened",
                                'errors':{},
                                'response':{str(e)},
                                },status=status.HTTP_400_BAD_REQUEST)

            
        else:
            return Response({'success':'false',
                                'error_msg':beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
