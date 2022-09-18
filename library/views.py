from django.shortcuts import render

from django.db.models import Q
from accounts import models as ac_models
from . import models
from librarian import models as lib_models

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
                        if uzr.is_user_blocked :
                            return Response({'success':'false','error_msg':'USER BLOCKED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        # try:#do user has authorization
                        #     kwg=uzr.authorize.__dict__

                        # except:
                        #     return Response({'success':'false','error_msg':'USER UNAUTHORIZED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)

                        # for  i in Dkwargs:#does all given permitions are present
                        #     if Dkwargs[i]!=kwg[i]:

                        #         return Response({'success':'false','error_msg':'USER UNAUTHORIZED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        #     else:
                        #         print('match ',i,kwg[i],Dkwargs[i])
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
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


######################Following APIs should be accessed through a normal User’s account############


#####################Following APIs should be accessed through Super admin ####################

class get_create_update_delete_library(APIView):
    #@is_authenticate(CURD_library=True)
    def get(self,request,id=None):
        try:
            if id is not None:
                book=list(ac_models.library_info.objects.filter(id=id))
                if book==[]:
                    return Response({'success':'false',
                                    'error_msg':'lib data not found ',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
                f1=serializers.library_data(book,many=True)
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"result":f1.data},
                                    },status=status.HTTP_202_ACCEPTED)

            user=list(ac_models.library_info.objects.all())
            f2=serializers.library_data(user,many=True)
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"result":f2.data},
                                    },status=status.HTTP_202_ACCEPTED)

        except:
            return Response({'success':'false',
                                'error_msg':'invalid lib id ',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
    
    @is_authenticate()
    def post(self, request):
        f1 = serializers.add_lib(data=request.POST)
        if f1.is_valid():
            f1.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def put(self,request,id):
        try:
            
            f1=list(ac_models.library_info.objects.filter(id=id))
            if f1==[]:
                return Response({'success':'false',
                                'error_msg':"Data does not exists ",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            
            f1=f1[0]
            f_1=serializers.add_lib(data=request.POST,instance=f1)
            if f_1.is_valid():
                f_1.save()
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f_1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def delete(self,request,id):

            try:
                
                book=list(ac_models.library_info.objects.filter(id=id))
                if book==[]:
                    return Response({'success':'false',
                                        'error_msg':'invalid_lib id',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                book=book[0]
                book.delete()
                return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{  },
                                        },status=status.HTTP_202_ACCEPTED)
            except:
                return Response({'success':'false',
                                        'error_msg':'invalid_lib id',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)

class signup_super_admin(APIView):
    def get(self,request):
        f0=serializers.password()
        f1=serializers.create_users_form()

        return Response({**f1.data,**f0.data
                            },status=status.HTTP_202_ACCEPTED)
    
    def post(self, request):
        f1=serializers.create_users_form(data=request.POST)
       
        if f1.is_valid():
            check_list = list(ac_models.Users.objects.filter((Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number']))|
                                                                        Q(email=request.POST['email'])))
                                                           
            del_acc=[]
            if check_list != []:
                for i in check_list:
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
                # user=f1.save()
                uzr=ac_models.Users()
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
                # tem= models.authorizations()
                # tem.usr=uzr
                # tem.Create_a_new_book=True
                # tem.Edit_an_existing_book=True
                # tem.Delete_a_book=True
                # tem.Retrieve_book_data=True
                # tem.Create_auser=True
                # tem.Delete_a_user=True
                # tem.Lend_the_book=True
                # tem.save()
                uzr_token=ac_models.users_token(users=uzr,token=sec)
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
    #@is_authenticate(Delete_a_user=True)
    def delete(self,request):

            try:
                
                uzr=list(ac_models.Users.objects.filter(id=request.POST['id']))
                if uzr==[]:
                    return Response({'success':'false',
                                        'error_msg':'invalid_user id',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                uzr=uzr[0]
                uzr.delete()
                return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{  },
                                        },status=status.HTTP_202_ACCEPTED)
            except:
                return Response({'success':'false',
                                        'error_msg':'invalid_user id',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)

class add_librarian_from_super_admin(APIView):
    def get(self,request):
        f0=serializers.password()
        f1=serializers.create_librarian_form()

        return Response({**f1.data,**f0.data
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request):
        f1=serializers.create_librarian_form(data=request.POST)
       
        if f1.is_valid():
            check_list = list(ac_models.libraians.objects.filter((Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number']))|
                                                                        Q(email=request.POST['email'])))
                                                           
            del_acc=[]
            if check_list != []:
                for i in check_list:
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
                # user=f1.save()
                uzr=ac_models.libraians()
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
                # tem= models.authorizations()
                # tem.usr=uzr
                # tem.Create_a_new_book=True
                # tem.Edit_an_existing_book=True
                # tem.Delete_a_book=True
                # tem.Retrieve_book_data=True
                # tem.Create_auser=True
                # tem.Delete_a_user=True
                # tem.Lend_the_book=True
                # tem.save()
                uzr_token=ac_models.librarians_token(users=uzr,token=sec)
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

    @is_authenticate()
    def delete(self,request):

            try:
                
                book=list(ac_models.libraians.objects.filter(id=request.POST['id']))
                if book==[]:
                    return Response({'success':'false',
                                        'error_msg':'invalid_lib id',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                book=book[0]
                book.delete()
                return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{  },
                                        },status=status.HTTP_202_ACCEPTED)
            except:
                return Response({'success':'false',
                                        'error_msg':'invalid_lib id',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)