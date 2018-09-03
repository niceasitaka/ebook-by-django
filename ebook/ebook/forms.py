from django import forms

class PostSearchForm(forms.Form):
	# search_word은 input 태그의 name 속성이 됨, 태그에 입력된 값을 저장
	search_word = forms.CharField(label = '도서 검색(제목, 작가, 요약)')
	
class NaverAPISearchForm(forms.Form):
	# search_word은 input 태그의 name 속성이 됨, 태그에 입력된 값을 저장
	keyword = forms.CharField(label = '네이버 도서 검색')