from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'ebook', views.EbookViewSet)

# config 의 urls 에서 namespace 를 사용하려면 app_name 지정 필수
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
	path('booksearch/', views.NaverSearch.as_view(), name='ebook_api_search'), #/ebook/booksearch/

	path('api/', include(router.urls)), #/ebook/api/
]	
