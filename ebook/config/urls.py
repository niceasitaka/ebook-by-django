from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
	# auth 앱의 URLconf에는 /login/, /logout/과 같이 URL이 미리 정의됨
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/register/', views.UserCreateView.as_view(), name='register'),
	path('accounts/register/done/', views.UserCreateDoneTV.as_view(), name='register_done'),
	
	path('', views.HomeView.as_view(), name='home'),
	# config 의 urls 에서 namespace 를 사용하려면 app_name 지정 필수
	path('ebook/', include('ebook.urls', namespace='ebook')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
