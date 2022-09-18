from django.urls import path
from . import views


urlpatterns = [
#------------urls links--------------------------

path('get_own_barrowed_book',views.get_own_barrowed_book_list.as_view(),name='get_own_barrowed_book'),
path('get_book_data_from_partculer_lib-<id>',views.get_book_data_from_partculer_library.as_view(),name='get_book_data_from_partculer_lib'),
path('return_book_from_a_lib',views.return_book_from_a_library.as_view(),name='return_book_from_a_lib'),

]