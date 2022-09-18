from django.db import models

# Create your models here.
class Users(models.Model):
    email=models.EmailField(max_length=60, unique=True)
    username=models.CharField(max_length=30,default='')
    password=models.TextField(default="")
    user_type= models.CharField(max_length=12,default='User') # student,librarian,superadmin
    profile_pic=models.ImageField(upload_to='user/profile_image',default='deafult_profile_pic.jpeg')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    address=models.CharField(max_length=150)
    is_user_blocked=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=200,default='')

class users_token(models.Model):
	users=models.OneToOneField(Users,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.users)+'token='+str(self.token)

class student(models.Model):
    email=models.EmailField(max_length=60, unique=True)
    username=models.CharField(max_length=30,default='')
    password=models.TextField(default="")
    user_type= models.CharField(max_length=12,default='student') # student,librarian,superadmin
    profile_pic=models.ImageField(upload_to='user/profile_image',default='deafult_profile_pic.jpeg')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    address=models.CharField(max_length=150)
    is_user_blocked=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=200,default='')

class student_token(models.Model):
	users=models.OneToOneField(student,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.users)+'token='+str(self.token)
class libraians(models.Model):
    email=models.EmailField(max_length=60, unique=True)
    username=models.CharField(max_length=30,default='')
    password=models.TextField(default="")
    user_type= models.CharField(max_length=12,default='librarian') # student,librarian,superadmin
    profile_pic=models.ImageField(upload_to='user/profile_image',default='deafult_profile_pic.jpeg')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    address=models.CharField(max_length=150)
    is_user_blocked=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=200,default='')

class librarians_token(models.Model):
	users=models.OneToOneField(libraians,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.users)+'token='+str(self.token)


class Book_details(models.Model):
    Book_name=models.CharField(max_length=30,default='')
    author_name=models.CharField(max_length=30,default='')
    publications=models.TextField(default="")
    book_quantity= models.IntegerField(default='0') 

class library_info(models.Model):
    librarians=models.ForeignKey(libraians,blank=True,null=True,on_delete=models.SET_NULL,related_name='User')
    library_name=models.CharField(max_length=150)
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    address=models.CharField(max_length=150)
    book_details=models.ForeignKey(Book_details,blank=True,null=True,on_delete=models.SET_NULL,related_name='books')
    book_issu_by=models.ForeignKey(student,blank=True,null=True,on_delete=models.SET_NULL,related_name='book_barrower')
    issu_date=models.DateTimeField(auto_now_add=True)
    