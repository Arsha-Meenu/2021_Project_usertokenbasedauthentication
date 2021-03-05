from django.contrib import admin
from django.urls import path
from user_auth_app import views

# swagger section
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title = 'api swagger')

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Students Details",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.remote"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simpleapi/',views.simpleapi.as_view(),name="simpleapi"),
    path('register/',views.RegisterClass.as_view(),name="register_Api"),
    path('login/',views.LoginClass.as_view(),name="login_Api"),
    path('permission/<int:pk>/',views.UserViewSet.as_view({'get': 'list','put':'update','delete':'destroy'}),name='viewset'),
    # # integrate the django-rest-swagger in your django-rest application
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # admin can view and delete user details
    path('adminuserpermission/<int:pk>/',views.AdminUserPermission.as_view(),name = "adminuserdelete"),

     
   
]
