1. python -m venv venv

2. source venv/Scripts/activate (mac : source/venv/bin/activate)

3. pip install django==3.2.12

4. django-admin startproject blog .

5. secret key 보호

   - secret.json 생성
   - settings.py에서 SECRET_KEY 가져와 복붙
   - settings.py에서 SECRET_KEY 있던 자리에 아래 부분 입력

   ```
   from pathlib import Path
   
   # Build paths inside the project like this: BASE_DIR / 'subdir'.
   BASE_DIR = Path(__file__).resolve().parent.parent
   
   
   # Quick-start development settings - unsuitable for production
   # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
   
   # SECURITY WARNING: keep the secret key used in production secret!
   import os, json
   from django.core.exceptions import ImproperlyConfigured
   
   # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   
   secret_file = os.path.join(BASE_DIR, 'secrets.json')
   
   with open(secret_file) as f:
       secrets = json.loads(f.read())
   
   def get_secret(setting, secrets=secrets):
       try:
           return secrets[setting]
       except KeyError:
           error_msg = "Set the {} environment variable".format(setting)
           raise ImproperlyConfigured(error_msg)
   
   SECRET_KEY = get_secret("SECRET_KEY")
   ```

   - .gitignore에 secrets.json 추가 (난 이미 했으니까 생략)

6. 'DIRS': [os.path.join(BASE_DIR , 'templates')],

7. templates 폴더 프로젝트 바깥에 생성

8. settings.py -> DATABASES ->'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),

9. LANGUAGE_CODE = 'ko-kr'

   TIME_ZONE = 'Asia/Seoul'

   USE_TZ = False

10. settings.py에 추가

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #개발자가 관리하는 파일들 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') #사용자가 업로드한 파일 관리

#AUTH_USER_MODEL = 

#LOGGING = 
```

10. python manage.py migrate
11. python manage.py createsuperuser
11. urls.py

```python
from blog.views import HomeView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
]

```

13. views.py

```python
from django.views.generic import TemplateView

class ModelView(TemplateView):
    template_name = "home.html"

```

14.agency 부트스트랩 파일들 복사해와서 

​	css, js -> static	

​	index.html -> home.html 이름 변경

15. home.html에서 src = 'assets/' -> src = "{% static 'assets/' %}"로 변경

    href도 static 파일들은 static 형식으로 변경

16. 그 외에 알아서 꾸미기
17. python manage.py startapp blogapp
18. settings.py -> installed app 등록

19. models.py

```python
from django.db import models

class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank = True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField('TITLE', max_length=50)
    description = models.CharField("DESCRIPTION", max_length=100, blank=True, help_text='Simple one line text')
    image = models.ImageField('IMAGE', blank=True, upload_to='blog/%Y/%m', blank=True, null=True)
    content = models.TextField('CONTENT')
    created_at = models.DateTimeField('CREATED_AT',auto_now_add=True)
    updated_at = models.DateTimeField('UPDATED_AT',auto_now=True)
    like = models.PositiveSmallIntegerField('LIKE', default=0)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField('DESCRIPTON', max_length=100, blank=True, help_text="simple one line text")

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField('CONTENT')
    created_at = models.DateTimeField('CREATED_AT', auto_now_add=True)
    updated_at = models.DateTimeField('UPDATED_AT', auto_now = True)

```



20. admin.py

```python
from django.contrib import admin

from blogapp.models import Post, Category, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','category','tag_list','title','description','image','created_at','updated_at','like')

    def tag_list(self, obj): #해당 post 객체의 모든 tag에 대해서 그 이름들을 컴마로 이어붙여 돌려줌
        return ','.join([t.name for t in obj.tags.all()])

    def get_queryset(self,request): #테이블로부터 포스트 가져올 때 tag도 같이 가져옴
        return super().get_queryset(request).prefetch_related('tags')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','description',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post','short_content','created_at','updated_at')


```



21. python manage.py makemigrations
22. python manage.py migrate
23. blog -> urls.py에 path('blog/', include('blogapp.urls')) 추가
24. blogapp -> urls.py

```python
from django.urls import path

from blogapp import views

app_name= 'blog'
urlpatterns = [
    path('post/<int:pk>/', views.PostDV.as_view(), name='post_detail'),
]
```

25. blogapp -> views.py

```python
from django.shortcuts import render
from django.views.generic import DetailView

from blogapp.models import Post

class PostDV(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    

```

26. templates 폴더 밑에 blogapp폴더 > post_detail.html 생성

27. 파일 업로드를 위한 설정

```python
#blog > urls.py에 아래 내용 추가
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root='settings.MEDIA_ROOT')
```

28. base.html 만들어 상속

29. home.html 작성

30. post_detail.html 작성





