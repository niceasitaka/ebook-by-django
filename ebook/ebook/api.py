# urllib는 웹 클라이언트를 작성하는데 사용되는 모듈들이 있음
# request는 클라이언트의 요청 처리
# parse는 URL을 분석 후 속성 구분함
import urllib.request


import json

def api_get_book(title):
	client_id = "mS4g5rpgZfPVn8PiXz07" # 애플리케이션 등록시 발급 받은 값 입력
	client_secret = "fjXvfNEq3r" # 애플리케이션 등록시 발급 받은 값 입력
	encText = urllib.parse.quote(title) # UTF-8 형식으로 URL 인코딩
	url = "https://openapi.naver.com/v1/search/book?query=" + encText +"&display=10&sort=count"
	# URL 요청과 관련된 정보를 담는 역할
	request = urllib.request.Request(url)
	# 네이버 오픈 API는 기본적으로 클라이언트 아이디와 시크릿값을 헤더에 포함하여 전송해야 이용가능
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	response = urllib.request.urlopen(request) # header 정보를 포함한 request 객체를 전달
	rescode = response.getcode() # response의 HTTP status code 를 리턴

	if(rescode==200):
		response_body = response.read() # 응답 받은 내용 읽기
		json_rt = response_body.decode('utf-8') # UTF-8 형식으로 디코딩
		py_rt = json.loads(json_rt) # 응답 받은 내용이 json 형태이므로 파이썬에서 json을 읽기 위한 역할
		items = py_rt["items"] # 응답 내용 중 items dict 만 가져옴(도서 정보 관련)
		return items
	else:
		print("Error Code:" + rescode)