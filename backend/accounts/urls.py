 
from django.urls import path
from .views import  UserProfileView, CredentialsView, CheckAvailability, CreateUserDataView,ListUserDataView,UpdateUserDataView, DeleteUserDataView


 
urlpatterns = [
    path('user/info/',  UserProfileView.as_view(), name='user-profile'),
    path('author/credentials/',  CredentialsView.as_view(), name='author-credentials'),
    path('check-availability/', CheckAvailability.as_view(), name='check_availability'),
    path('create/user-data/', CreateUserDataView.as_view(), name='user-data'),
    path('view/user-data/', ListUserDataView.as_view(), name='view-user-data'), 
    path('update/user-data/', UpdateUserDataView.as_view(), name='update-user-data'),
    path('delete/user-data/', DeleteUserDataView.as_view(), name='delete-user-data'),
    
     
     ]
 
