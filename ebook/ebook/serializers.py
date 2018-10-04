from rest_framework import serializers

from .models import Books

class EbookSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='ebook:books-detail')
	# conf 의 urls.py 에서 ebook 네임스페이스가 명시되었기 때문에 view_name 인자에도 네임스페이스 명시 필요

	class Meta:
		model = Books
		fields = ['url', 'title', 'author', 'description',
					'cover_image', 'content_text', 'content_image']
