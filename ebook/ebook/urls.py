from django.urls import path
from ebook import views

app_name = 'ebook'
urlpatterns = [
	path('', views.EbookLV.as_view(), name='index'), # /ebook/
	path('ebook/', views.EbookLV.as_view(), name='ebook_list'), # /ebook/ebook/
	path('regtext/', views.EbookCVText.as_view(), name='ebook_text_add'), # /ebook/regtext/ , 텍스트 도서 업로드
	path('regimage/', views.EbookCVImage.as_view(), name='ebook_image_add'), # /ebook/regimage/ , 이미지 도서 업로드
	path('ebook/<int:pk>/', views.EbookDV.as_view(), name='ebook_detail'), # /ebook/1/
	path('ebook/<int:pk>/rentreg/', views.rent, name='ebook_rent'), # /ebook/1/rentreg/
	path('rentlist_check/', views.rent_check, name='list_check'), # /ebook/rentlist_check/
	path('rentlist/', views.EbookRentLV.as_view(), name='rent_list'), # /ebook/rentlist/
	path('ebook/<int:pk>/content/', views.ebook_content, name='ebook_content'), # /ebook/1/content/

]	
