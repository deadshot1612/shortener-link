from django.urls import path

# Import the home view
from .views import home_view, redirect_url_view, all_urls_view,delete

appname = "shortener"

urlpatterns = [
    # Home view
    path('', home_view, name='homepage'),
    path('mylinks/', all_urls_view , name='all_links' ),
    path('<str:shortened_part>', redirect_url_view, name='redirect'),
    path('delete/<int:pk>',delete, name='delete')
]