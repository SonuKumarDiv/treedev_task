from django.urls import path
from . import views

app_name='account'
#<a href='#' data-toggle='tooltip'title='Tooltip'>skjd</a>
urlpatterns = [
#------------admin urls links--------------------------
path('login_admin_api',views.login_admin_api.as_view(),name='login_admin_api'),
path('logout_api',views.logout_api.as_view(),name='logout_api'),
path('sign_up_user',views.signup_super_user.as_view(),name='sign_up_users'),
path('login_librarian_api',views.login_librarian_api.as_view(),name='login_admin_api'),
path('logout_librarian_api',views.logout_librarian_api.as_view(),name='logout_api'),
path('login_student_api',views.login_student_api.as_view(),name='sign_up_users'),
path('logout_stu_api',views.logout_student_api.as_view(),name='sign_up_users'),
]