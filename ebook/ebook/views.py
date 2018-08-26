from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from datetime import timedelta, date

from ebook.models import Books, RentHistory

# 전체 책 목록뷰
class EbookLV(ListView):
	model = Books

# 책 등록뷰
class EbookCV(LoginRequiredMixin, CreateView): # 로그인 필수
	model = Books
	fields = ['title', 'author', 'description', 'image', 'content']
	template_name = 'ebook/books_form.html'
	success_url = reverse_lazy('ebook:index') # form_valid 함수 진행이 성공적이면 index로 이동
	
	# POST로 들어온 데이터가 유효하면 CreateView 클래스의 form_valid 메소드 호출
	def form_valid(self, form): 
		return super(EbookCV, self).form_valid(form) 
		# super()에 의해 상위 클래스의 form_valid 메소드의 form.save() 실행됨(DB에 반영 후 success_url 리다이렉트)

# 각 책들의 상세뷰
class EbookDV(LoginRequiredMixin, DetailView):
	model = Books
	template_name = 'ebook/books_detail.html'

# 책 대출을 위한 rent 함수 실행
# DB에 데이터 삽입 진행
# @require_POST # POST를 제외한 다른 접근에 대해서는 빈 페이지와 405코드를 반환함. 필요 시 사용 예정
@login_required
def rent(request, pk):
	# get_object_or_404을 쓰지 않은 이유 : book=pk 에 해당하는 다수 row 를 가져오지 못하기 때문
	# rent = get_object_or_404(RentHistory, book=pk)
	rent = RentHistory.objects.filter(book=pk)
	for i in rent:
		# 사용자가 이미 대출했었고 반납되지 않은 책을 선택했을 시,
		if i.user == request.user and i.rent_status == False:
			#messages.info(request, '{}까지 열람 가능한 동일 도서가 있습니다.'.format(i.rent_end))
			return redirect('ebook:list_check')
	
	rent_start = date.today()
	rent_end = date.today() + timedelta(days=7) # 대출 기간은 7일
	db_insert = RentHistory(rent_start=rent_start, rent_end=rent_end, rent_status=False, book_id=pk, user=request.user)
	db_insert.save()

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

	# ebook_rent_list.html 에 대출했던 사용자, 반납 상태를 고려하여 책 목록을 표시
	def get_queryset(self):
		return RentHistory.objects.filter(user=self.request.user, rent_status=False)

# 책 내용 보여주기(책 읽기)
@login_required
def ebook_content(request, pk):
	rent = RentHistory.objects.get(id=pk)
	# open 함수에서 arg를 받을 때는 str 형으로 변환 필요
	file_path = str(rent.book.content)
	# close() 함수를 쓰지 않기 위해 컨텍스트 매니저 사용 / 한 쌍으로 함께 실행되어야 하는 연결된 수행 코드를 한 번에 처리
	with open('C:/python/django_test/ebook/media/' + file_path) as book:
		content = book.read()
	return render(request, 'ebook/ebook_content.html', {'content': content})




