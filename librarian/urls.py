from django.urls import path
from . import views


urlpatterns = [
#------------urls links--------------------------
path('crud_book_detail-<id>',views.get_create_update_delete_book.as_view(),name='crud_book_detail'),
path('crud_book_detail',views.get_create_update_delete_book.as_view(),name='crud_book_detail'),
path('add_user_from_librarian',views.add_user_from_librarian.as_view(),name='add_user_from_librarian'),
path('lend_the_book',views.lend_the_book_by_librarian.as_view(),name='lend_the_book'),

]