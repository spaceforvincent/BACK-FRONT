from django.shortcuts import render
from django.views import View
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView
from blogapp.models import Category, Post, Tag, Comment
from django.http import JsonResponse
from api.utils import obj_to_post,prev_next_post,obj_to_comment
# Create your views here.

class ApiPostLV(BaseListView):
    # model = Post
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


    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_post(obj, False) for obj in qs]
        
        pageCnt = context['paginator'].num_pages
        curPage = context['page_obj'].number


        jsonData = {
            'postList' : postList,
            'pageCnt' : pageCnt,
            'curPage' : curPage,
        }
        return JsonResponse(data=jsonData,safe=True,status=200)


class ApiPostDV(BaseDetailView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        post = obj_to_post(obj)
        prevPost, nextPost = prev_next_post(obj)

        qsComment = obj.comment_set.all() #obj : pk로 검색한 특정 post 레코드
        commentList = [obj_to_comment(obj) for obj in qsComment]

        jsonData = {
            'post':post,
            'prevPost': prevPost,
            'nextPost':nextPost,
            'commentList':commentList,
        }
        return JsonResponse(data=jsonData,safe=True,status=200)

    
class ApiCateTagView(View):
    def get(self, request, *args, **kwargs):
        qs1 = Category.objects.all()
        qs2 = Tag.objects.all()
        cateList = [cate.name for cate in qs1]
        tagList = [tag.name for tag in qs2]

        jsonData = {
            'cateList': cateList,
            'tagList': tagList,
        }
        return JsonResponse(data=jsonData, safe=True, status=200)

class ApiPostLikeDV(BaseDetailView):
    model = Post

    def render_to_response(self,context, **response_kwargs):
        obj = context['object'] #post 테이블에서 특정 pk로 꺼내온 레코드  
        obj.like += 1
        obj.save()
        return JsonResponse(data=obj.like, safe=False,status=200) #safe는 딕셔너리 일때 true

class ApiCommentCV(BaseCreateView):
    model = Comment
    fields='__all__'
    
    def form_valid(self, form) :
        self.object = form.save() #새로운 레코드 생성
        comment = obj_to_comment(self.object)
        return JsonResponse(data=comment,safe=True,status=201) #딕셔너리 타입이므로 true
    def form_invalid(self, form) :
        return JsonResponse(data=form.errors,safe=True,status=400) #딕셔너리 타입이므로 true
