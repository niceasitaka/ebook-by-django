from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

# 가장 첫화면 뷰
class HomeView(TemplateView):
	template_name = 'home.html'
	
# 계정 생성
class UserCreateView(CreateView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm # 장고에서 제공하는 기본 폼
	success_url = reverse_lazy('register_done')

# 계정 생성 완료
class UserCreateDoneTV(TemplateView):
	template_name = 'registration/register_done.html'

# login_requied() 함수는 데코레이터로 사용되기 때문에 일반 함수에만 적용 가능
# 클래스에 적용하기 위함
class LoginRequiredMixin(object):
	@classmethod # 상속받아도 해당 클래스의 속성을 사용하기 위함이지만, 여기서는 왜 쓰느지 모르겠다..
	def as_view(cls, **initkwargs):
		view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
		return login_required(view)
