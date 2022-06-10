from django.shortcuts import render
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from blogapp.models import Post
from django.http import JsonResponse
from api.utils import obj_to_post,prev_next_post
# Create your views here.

class ApiPostLV(BaseListView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_post(obj, False) for obj in qs]
        return JsonResponse(data=postList,safe=False,status=200)


class ApiPostDV(BaseDetailView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        post = obj_to_post(obj)
        prevPost, nextPost = prev_next_post(obj)

        jsonData = {
            'post':post,
            'prevPost': prevPost,
            'nextPost':nextPost,
        }
        return JsonResponse(data=jsonData,safe=True,status=200)