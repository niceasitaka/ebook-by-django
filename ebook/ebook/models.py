from django.db import models
from django.contrib.auth.models import User
from .fields import ThumbnailImageField
from django.urls import reverse

from django.db import models

class Books(models.Model):
	title = models.CharField("도서명", max_length = 100)
	author = models.CharField("저자", max_length = 50)
	description = models.CharField("책요약/소개", max_length=300, blank=True)
	# 커스텀 썸네일필드 사용, 파이썬 웹 프로그래밍 책 참고, ebook/fields.py 에 정의
	cover_image = ThumbnailImageField("도서 겉표지", upload_to='photo/%Y/%m', null=True)	
	# 텍스트 파일 형식의 도서
	content_text = models.FileField("텍스트형식 도서", upload_to='content/%Y/%m', null=True)
	# 이미지 파일 형식의 도서
	content_image = models.ImageField("이미지형식 도서",upload_to='content/%Y/%m', null=True)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('ebook:ebook_detail', args=(self.id,))
	
class RentHistory(models.Model):
	user = models.ForeignKey(User, verbose_name='대출회원', on_delete=models.CASCADE, null=True)
	book = models.ForeignKey(Books, verbose_name='대출도서', on_delete=models.CASCADE, null=True)
	rent_start = models.DateTimeField("대여시작일")
	rent_end = models.DateField("대여종료일")
	rent_status = models.BooleanField("반납여부")

	def __str__(self):
		return "{}-{}".format(self.user, self.book)
