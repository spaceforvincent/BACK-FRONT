from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from api.utils import obj_to_post, prev_next_post, obj_to_comment
from blogapp.models import Post,Category,Tag

import json

# class PostDV(TemplateView):
#     template_name = 'blogapp/post_detail.html'

class PostDV(DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDV, self).get_context_data()
        
        obj = context['object']
        post = obj_to_post(obj)
        prevPost, nextPost = prev_next_post(obj)

        qsComment = obj.comment_set.all()
        commentList = [obj_to_comment(obj) for obj in qsComment]

        qs1 = Category.objects.all()
        qs2 = Tag.objects.all()
        cateList = [cate.name for cate in qs1]
        tagList = [tag.name for tag in qs2]


        dataDict = {
            'post': post,
            'prevPost': prevPost,
            'nextPost': nextPost,
            'commentList': commentList,
            'cateList' : cateList,
            'tagList' : tagList,
        }

        context['myJson'] = json.dumps(dataDict)
        return context