from users.urls import urlpatterns as authentication_urls
from users.urls import urlpatterns as users_urls

urlpatterns = (
    authentication_urls
    + users_urls
    
)
