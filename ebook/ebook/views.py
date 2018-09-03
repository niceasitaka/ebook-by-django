from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger

from datetime import timedelta, date

from ebook.models import Books, RentHistory
from ebook.forms import PostSearchForm, NaverAPISearchForm
from ebook.api import api_get_book

# 전체 책 목록뷰
# 리스트 페이지에서 검색 기능 추가
class EbookLV(ListView, FormView):
	form_class = PostSearchForm # 폼으로 사용될 클래스 지정
	model = Books
	paginate_by = 3 # 페이지에 개체 3개만 표시
		
	def form_valid(self, form):
		# POST 요청의 search_word의 파라미터 값을 추출해 schWord에 지정, search_word는 PostSearchForm에서 정의한 필드이름
		schWord = '%s' % self.request.POST['search_word']
		# Q 객체는 filter 메소드의 매칭 조건을 다양하게 함
		# icontains는 대소문자를 구분하지 않고 단어가 포함되어 있는지 검사
		# distinct는 중복 제외
		post_list = Books.objects.filter(Q(title__icontains=schWord)|
			Q(description__icontains=schWord)|Q(author__icontains=schWord)).distinct()

		# 템플릿에 넘겨줄 context를 사전형으로 미리 정의
		context = {}
		context['form'] = form
		context['search_word'] = schWord
		context['object_list'] = post_list
		
		return render(self.request, 'ebook/books_list.html', context) # No Redirection	
		
# 도서 등록뷰
# 도서가 text 형식일 경우
class EbookCVText(LoginRequiredMixin, CreateView): # 로그인 필수
	model = Books
	fields = ['title', 'author', 'description', 'cover_image', 'content_text']
	template_name = 'ebook/books_text_form.html'
	success_url = reverse_lazy('ebook:index') # form_valid 함수 진행이 성공적이면 index로 이동
	
	# POST로 들어온 데이터가 유효하면 CreateView 클래스의 form_valid 메소드 호출
	def form_valid(self, form):
		messages.info(self.request, '도서 등록 완료')
		return super(EbookCVText, self).form_valid(form) 
		# super()에 의해 상위 클래스의 form_valid 메소드의 form.save() 실행됨(DB에 반영 후 success_url 리다이렉트)
		
# 책 등록뷰
# 도서가 image(jpg, png 등) 형식일 경우
# EbookCVText 클래스와 로직 동일
class EbookCVImage(LoginRequiredMixin, CreateView): # 로그인 필수
	model = Books
	fields = ['title', 'author', 'description', 'cover_image', 'content_image']
	template_name = 'ebook/books_image_form.html'
	success_url = reverse_lazy('ebook:index')
	
	def form_valid(self, form):
		messages.info(self.request, '도서 등록 완료')
		return super(EbookCVImage, self).form_valid(form) 

# 각 책들의 상세뷰
class EbookDV(LoginRequiredMixin, DetailView):
	model = Books
	template_name = 'ebook/books_detail.html'

# 책 대출을 위한 rent 함수 실행
# DB에 데이터 삽입 진행
@require_POST # POST를 제외한 다른 접근에 대해서는 빈 페이지와 405코드를 반환함.
@login_required
def rent(request, pk):
	# get_object_or_404을 쓰지 않은 이유 : book=pk 에 해당하는 다수 row 를 가져오지 못하기 때문
	# rent = get_object_or_404(RentHistory, book=pk)
	rent = RentHistory.objects.filter(book=pk)
	for i in rent:
		# 사용자가 이미 대출했었고 반납되지 않은 책을 선택했을 시,
		if i.user == request.user and i.rent_status == False:
			messages.info(request, '{}까지 열람 가능한 동일 도서가 있습니다.'.format(i.rent_end))
			return redirect('ebook:list_check')
	
	rent_start = date.today()
	rent_end = date.today() + timedelta(days=7) # 대출 기간은 7일
	db_insert = RentHistory(rent_start=rent_start, rent_end=rent_end, rent_status=False, book_id=pk, user=request.user)
	db_insert.save()
	messages.info(request, '대여성공! 열람 가능한 기간은 {}까지 입니다.'.format(rent_end))
	return redirect('ebook:list_check')

# 대출 만료 날짜에 따라 반납 여부 결정
# 사용자가 열람 가능한 책 목록을 볼 경우 무조건 rent_check 함수 실행됨
# URL 로직은 무조건 아래와 같이 진행되도록 함
# /ebook/rentlist_check/ -> /ebook/rentlist/
@login_required
def rent_check(request):
	rent = RentHistory.objects.filter(user=request.user)
	for i in rent:
		if i.rent_end < date.today():
			i.rent_status = True
			i.save()
			
	return redirect('ebook:rent_list')

# 열람 가능한 책 목록뷰
# rent_check 함수 선실행
class EbookRentLV(LoginRequiredMixin, ListView):
	model = RentHistory
	template_name = 'ebook/ebook_rent_list.html'
	paginate_by = 5

	# ebook_rent_list.html 에 대출했던 사용자, 반납 상태를 고려하여 책 목록을 표시
	def get_queryset(self):
		return RentHistory.objects.filter(user=self.request.user, rent_status=False)

# 책 내용 보여주기(책 읽기)
@login_required
def ebook_content(request, pk):
	rent = RentHistory.objects.get(id=pk)
	# Books 테이블의 텍스트형 도서가 업로드된 경우
	if rent.book.content_text:
		# open 함수에서 arg를 받을 때는 str 형으로 변환 필요
		file_path = str(rent.book.content_text)
		# close() 함수를 쓰지 않기 위해 컨텍스트 매니저 사용 / 한 쌍으로 함께 실행되어야 하는 연결된 수행 코드를 한 번에 처리
		with open('C:/python/django_test/ebook/ebook/media/' + file_path) as book:
			content = book.read()
		
		context = {}
		context['content'] = content
		context['title'] = rent.book.title
		context['author'] = rent.book.author	
		return render(request, 'ebook/ebook_content.html', context)
	# Books 테이블의 이미지형 도서가 업로드된 경우
	else :
		# 아래 주석과 같이 코딩할 경우, content_path 자체가 ImageFieldFile 형식으로 되어 있어 str로 리턴 불가(이미지 파일은 url 형식으로 리턴 필요)
		#content_path = rent.book.content_image
		#content = 'C:/python/django_test/ebook/ebook/media/' + content_path
		content = rent.book.content_image.url
		return render(request, 'ebook/ebook_content_image.html', {'content': content})

# 네이버 도서 검색 API 연동
class NaverSearch(FormView):
	form_class = NaverAPISearchForm
	template_name = 'ebook/ebook_api_search.html'
	def form_valid(self, form):
		keyword = self.request.POST['keyword'] 
		books = api_get_book(keyword) # 검색된 단어는 api 연동 함수로 전달 후 리턴 받음
		context = {}
		context['form'] = form
		context['books'] = books # 도서 관련 내용은 모두 해당 dict에 지정
		
		return render(self.request, self.template_name, context)
