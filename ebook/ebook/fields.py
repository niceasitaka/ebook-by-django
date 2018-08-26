import os

from django.db.models.fields.files import ImageField, ImageFieldFile
# 커스텀 필드는 ImageField(장고 모델 정의에 사용하는 필드 역할) 상속 필요, ImageFieldFile는 이미지 파일을 파일 시스템에 쓰고 삭제하는 작업이 필요할 때 사용
from PIL import Image


# 기존 이미지 파일명을 기준으로 썸네일 파일명 생성
def _add_thumb(s):
    parts = s.split(".")
	# -1은 리스트의 맨 마지막 부분을 의미 / insert할 경우 마지막 부분 바로 앞에 삽입됨
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

# 파일을 지우고 쓰는 작업 진행
class ThumbnailImageFieldFile(ImageFieldFile):
	# 썸네일 파일 경로 생성
    def _get_thumb_path(self):
        return _add_thumb(self.path)
    thumb_path = property(_get_thumb_path)
    
	# thumb_url 속성을 만듬
    def _get_thumb_url(self):
        return _add_thumb(self.url)
    thumb_url = property(_get_thumb_url)
	
	# 썸네일 파일 저장 메소드
    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)

        size = (128, 128) 
        img.thumbnail(size, Image.ANTIALIAS) # 128X128 크기의 이미지 생성
        background = Image.new('RGB', size, (255, 255, 255, 0)) # 썸네일 백그라운드(흰배경) 이미지 생성
        background.paste( # 썸네일 이미지와 백그라운드를 합쳐 정사각형 모양으로 생성
            img, ( int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2) ) )
        background.save(self.thumb_path, 'JPEG') # 썸네일 파일 저장 / thumb_path

	# delete 메소드 호출되면 원본 및 썸네일 파일 모두 삭제
    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)

# 장고 모델 정의
class ThumbnailImageField(ImageField):
	# 새로운 FileField를 정의할 때는 attr_class 속성에 지정 필요
    attr_class = ThumbnailImageFieldFile

	# thumb_width, thumb_height 모두 정의 가능
	# ImageField 상속받아 모델 정의
    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
