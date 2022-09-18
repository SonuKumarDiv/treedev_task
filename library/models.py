from django.db import models

from accounts import models as ac_models
# Create your models here.

class authorizations(models.Model):
    usr=models.OneToOneField(ac_models.Users,on_delete=models.CASCADE, null=True,blank=True,related_name='authorize')
    Role=models.CharField(max_length=100,null=True,blank=True)
    #librarians roles and permissions 
    view_subadmin=models.BooleanField(default=False)
    manage_subadmin=models.BooleanField(default=False)
    Create_a_new_book=models.BooleanField(default=False)
    Edit_an_existing_book=models.BooleanField(default=False)
    Delete_a_book=models.BooleanField(default=False)
    Retrieve_book_data=models.BooleanField(default=False)
    Create_auser=models.BooleanField(default=False)
    Delete_a_user=models.BooleanField(default=False)
    Lend_the_book=models.BooleanField(default=False)

    # User Roles and permissions
    all_books_borrowed=models.BooleanField(default=False)
    all_books_borrowed=models.BooleanField(default=False)
    Return_the_borrowed_book=models.BooleanField(default=False)
    
    # SuperUser Roles and permissions
    CURD_library=models.BooleanField(default=False)
    create_librarian=models.BooleanField(default=False)
    delete_librarian=models.BooleanField(default=False)