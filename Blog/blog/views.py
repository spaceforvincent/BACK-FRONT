from django.views.generic import TemplateView, ListView
from api.utils import obj_to_post
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from blogapp.models import Post
import json

# class HomeView(TemplateView):
#     template_name = "home.html"

@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomeView(ListView):
    # model = Post
    template_name = "home.html"
    paginate_by = 3

    def get_queryset(self):
        paramCate = self.request.GET.get('category')
        paramTag = self.request.GET.get('tag')
        if paramCate:
            qs = Post.objects.filter(category__name__iexact=paramCate) #iexact : 대소문자 구별하지 않고 그 테이블로부터 일부 레코드만 가져옴
        elif paramTag:
            qs = Post.objects.filter(tags__name__iexact=paramTag)
        else:
            qs = Post.objects.all()
        return qs

    def get_context_data(self, *, object_list = None, **kwargs):
        context =  super().get_context_data()
        postList = [obj_to_post(obj) for obj in context['object_list']]    
        pageCnt = context['paginator'].num_pages    
        curPage = context['page_obj'].number

        dataDict = {
            'postList' : postList,
            'pageCnt' : pageCnt,
            'curPage' : curPage
        }    

        context['myJson'] = json.dumps(dataDict)
        return context