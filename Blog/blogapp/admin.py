from django.contrib import admin

from blogapp.models import Post, Category, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','category','tag_list','title','description','image','created_at','updated_at','like')

    def tag_list(self, obj): #해당 post 객체의 모든 tag에 대해서 그 이름들을 컴마로 이어붙여 돌려줌
        return ','.join([t.name for t in obj.tags.all()])

    def get_queryset(self,request): #테이블로부터 포스트 가져올 때 tag도 같이 가져옴
        return super().get.queryset(request).prefetch_related('tags')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','description',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post','short_content','created_at','updated_at')

