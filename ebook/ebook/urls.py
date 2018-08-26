from django.urls import path
from ebook import views

app_name = 'ebook'
urlpatterns = [
	path('', views.EbookLV.as_view(), name='index'), # /ebook/
	path('ebook/', views.EbookLV.as_view(), name='ebook_list'), # /ebook/ebook/
	path('register/', views.EbookCV.as_view(), name='ebook_add'), # /ebook/register/
	path('ebook/<int:pk>/', views.EbookDV.as_view(), name='ebook_detail'), # /ebook/1/
	path('ebook/<int:pk>/rentreg/', views.rent, name='ebook_rent'), # /ebook/1/rentreg/
	path('rentlist_check/', views.rent_check, name='list_check'), # /ebook/rentlist_check/
	path('rentlist/', views.EbookRentLV.as_view(), name='rent_list'), # /ebook/rentlist/
	path('ebook/<int:pk>/content/', views.ebook_content, name='ebook_content'), # /ebook/1/content/

]	
