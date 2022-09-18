from django.urls import path
from . import views


urlpatterns = [
#------------urls links--------------------------
path('get_create_update_delete_library',views.get_create_update_delete_library.as_view(),name='get_create_update_delete_library'),
path('get_create_update_delete_library-<id>',views.get_create_update_delete_library.as_view(),name='get_create_update_delete_library'),
path('signup_super_admin',views.signup_super_admin.as_view(),name='add_librarian_from_super_admin'),
path('add_librarian_from_super_admin',views.add_librarian_from_super_admin.as_view(),name='add_librarian_from_super_admin')
]