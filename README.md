# ebook 대여 시스템 구현
> 사용자가 ebook을 대여하고 볼 수 있도록 구현함

## 개요
- 대여한 ebook은 일정 기간동안 열람 가능
  - 대여 기간이 끝나면 다시 대여 신청 필요
- 사용자 별로 대여한 ebook만 볼 수 있도록 구현
- ebook 등록 가능
  - 이미지 또는 텍스트 형식의 도서 업로드 가능
  - 등록된 형식에 따라 브라우저에 보여질 수 있도록 구현
- REST API 적용
  - API root : /ebook/api/
  - E북 리스트 : /ebook/api/ebook/    
  - 보유도서 검색 : /ebook/api/ebook/?search=
 
- 아래 내용을 바탕으로 구현
  - 파이썬 웹 프로그래밍 실전편
  - https://wayhome25.github.io/ (초보몽키의 개발공부로그)
  
- pythonanywhere 배포버전 웹 주소
  - http://niceasitaka.pythonanywhere.com/
  
- AWS 배포버전 웹 주소
  - http://13.59.79.195/