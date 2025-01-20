from django.contrib import admin
from django.urls import path, include
# from base.urls import urlPatterns
# from django.http import HttpResponse

from django.conf import settings
from django.conf.urls.static import static 
# def home(request):
#     return HttpResponse('<h1 align = center > Hello Django  <h1>')
# def room(request):
#     return HttpResponse('<h2 align = center > Hello to Room <h1>')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home),
    # path('page2/', room),
   
   path('', include('base.urls')),
   path('api/', include('base.api.urls')),


]

urlpatterns+= static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)