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

```python
{% load static %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>{% block title %}{% endblock title %}</title>
        <!-- Favicon-->
        <link rel="icon" type="image/x-icon" href="{%static 'assets/favicon.ico'%}" />
        <!-- Font Awesome icons (free version)-->
        <script src="https://use.fontawesome.com/releases/v6.1.0/js/all.js" crossorigin="anonymous"></script>
        <!-- Google fonts-->
        <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700" rel="stylesheet" type="text/css" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="{%static 'css/styles.css'%}" rel="stylesheet" />
        {% block extra-style %}{% endblock extra-style %}

    </head>
    <body id="page-top">
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
            <div class="container">
                <div class="navbar-brand">Blog</div>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    Menu
                    <i class="fas fa-bars ms-1"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav text-uppercase ms-auto py-4 py-lg-0">
                        <li class="nav-item"><a class="nav-link" href="#page-top">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="#portfolio">Blog</a></li>
                        <li class="nav-item"><a class="nav-link" href="#team">Iam</a></li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'admin:index' %}">Admin</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <!-- Masthead-->
        <header class="masthead">
            <div class="container">
                <div class="masthead-subheading">Welcome To Our Blog!</div>
                <div style="margin-bottom:250px;">저의 일상 생활과 관련된 사항을 기록하고 있습니다.</div>
            </div>
        </header>

        {% block content %}
        {% endblock content %}

        
        {% block footer %}{% endblock footer %}

        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
        <!-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *-->
        <!-- * *                               SB Forms JS                               * *-->
        <!-- * * Activate your form at https://startbootstrap.com/solution/contact-forms * *-->
        <!-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *-->
        <script src="https://cdn.startbootstrap.com/sb-forms-latest.js"></script>

        {% block extra-script %}{% endblock extra-script %}
    </body>
</html>
```

29. home.html

```python
{% extends 'base.html' %}

{% load static %}

{% block title %}home.html{% endblock title %}

    {% block content %}
        <!-- Blog Grid-->
        <section class="page-section bg-light" id="portfolio">
            <div class="container">
                <div class="text-center">
                    <h2 class="section-heading text-uppercase">Posts</h2>
                    <h3 class="section-subheading text-muted">Lorem ipsum dolor sit amet consectetur.</h3>
                </div>
                <div class="row">
                    <div class="col-lg-4 col-sm-6 mb-4">
                        <!-- Portfolio item 1-->
                        <div class="portfolio-item">
                            <a class="portfolio-link" href="{% url 'blog:post_detail' 1 %}">
                                <div class="portfolio-hover">
                                    <div class="portfolio-hover-content"><i class="fas fa-plus fa-3x"></i></div>
                                </div>
                                <img class="img-fluid" src="{%static 'assets/img/portfolio/1.jpg'%}" alt="..." />
                            </a>
                            <div class="portfolio-caption">
                                <div class="portfolio-caption-heading">Threads</div>
                                <div class="portfolio-caption-subheading text-muted">Illustration</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-sm-6 mb-4">
                        <!-- Portfolio item 2-->
                        <div class="portfolio-item">
                            <a class="portfolio-link" data-bs-toggle="modal" href="#portfolioModal2">
                                <div class="portfolio-hover">
                                    <div class="portfolio-hover-content"><i class="fas fa-plus fa-3x"></i></div>
                                </div>
                                <img class="img-fluid" src="{%static 'assets/img/portfolio/2.jpg'%}" alt="..." />
                            </a>
                            <div class="portfolio-caption">
                                <div class="portfolio-caption-heading">Explore</div>
                                <div class="portfolio-caption-subheading text-muted">Graphic Design</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-sm-6 mb-4">
                        <!-- Portfolio item 3-->
                        <div class="portfolio-item">
                            <a class="portfolio-link" data-bs-toggle="modal" href="#portfolioModal3">
                                <div class="portfolio-hover">
                                    <div class="portfolio-hover-content"><i class="fas fa-plus fa-3x"></i></div>
                                </div>
                                <img class="img-fluid" src="{% static 'assets/img/portfolio/3.jpg' %}" alt="..." />
                            </a>
                            <div class="portfolio-caption">
                                <div class="portfolio-caption-heading">Finish</div>
                                <div class="portfolio-caption-subheading text-muted">Identity</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!-- Iam-->
        <section class="page-section bg-light" id="team">
            <div class="container">
                <div class="text-center">
                    <h2 class="section-heading text-uppercase">About Vincent</h2>
                    <h3 class="section-subheading text-muted">Lorem ipsum dolor sit amet consectetur.</h3>
                </div>
                <div class="row">
                    <div class="col-lg-4">
                        <div class="team-member">
                            <img class="mx-auto rounded-circle" src="{%static 'assets/img/team/1.jpg'%}" alt="..." />
                            <h4>Vincent Choi</h4>
                            <p class="text-muted">???</p>
                            <a class="btn btn-dark btn-social mx-2" href="#!" aria-label="Parveen Anand Twitter Profile"><i class="fab fa-twitter"></i></a>
                            <a class="btn btn-dark btn-social mx-2" href="#!" aria-label="Parveen Anand Facebook Profile"><i class="fab fa-facebook-f"></i></a>
                            <a class="btn btn-dark btn-social mx-2" href="#!" aria-label="Parveen Anand LinkedIn Profile"><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                    <div class="col-lg-8">
                        내 소개 내용...
                    </div>
                </div>
            </div>
        </section>      
    {% endblock content%}

    {% block footer %}
            <!-- Footer-->
            <footer class="footer py-4">
                <div class="container">
                    <div class="row align-items-center">
                        <div class="col-lg-4 text-lg-start">Copyright &copy; Your Website 2022</div>
                        <div class="col-lg-4 my-3 my-lg-0">
                            <a class="btn btn-dark btn-social mx-2" href="#!" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                            <a class="btn btn-dark btn-social mx-2" href="#!" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                            <a class="btn btn-dark btn-social mx-2" href="#!" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                        </div>
                        <div class="col-lg-4 text-lg-end">
                            <a class="link-dark text-decoration-none me-3" href="#!">Privacy Policy</a>
                            <a class="link-dark text-decoration-none" href="#!">Terms of Use</a>
                        </div>
                    </div>
                </div>
            </footer>
    {% endblock footer %}
    
```

30. post_detail.html

```python
{% extends 'base.html' %}

{% load static %}

 {% block title %}post_detail.html{% endblock title %}
{% block content %}
        <!-- Post Detail Grid-->
        <section class="page-section bg-light" id="post">
            <div class="container mt-5">
                <div class="row">
                    <div class="col-lg-8">
                        <!-- Post content-->
                        <article>
                            <!-- Post header-->
                            <header class="mb-4">
                                <!-- Post title-->
                                <h1 class="fw-bolder mb-1">Welcome to Blog Post!</h1>
                                <!-- Post meta content-->
                                <div class="text-muted fst-italic mb-2">Posted on January 1, 2022 by Start Bootstrap</div>
                                <!-- Post categories-->
                                <a class="badge bg-secondary text-decoration-none link-light" href="#!">Web Design</a>
                                <a class="badge bg-secondary text-decoration-none link-light" href="#!">Freebies</a>
                            </header>
                            <!-- Preview image figure-->
                            <figure class="mb-4"><img class="img-fluid rounded" src="https://dummyimage.com/900x400/ced4da/6c757d.jpg" alt="..." /></figure>
                            <!-- Post content-->
                            <section class="mb-5">
                                <p class="fs-5 mb-4">Science is an enterprise that should be cherished as an activity of the free human mind. Because it transforms who we are, how we live, and it gives us an understanding of our place in the universe.</p>
                                <p class="fs-5 mb-4">The universe is large and old, and the ingredients for life as we know it are everywhere, so there's no reason to think that Earth would be unique in that regard. Whether of not the life became intelligent is a different question, and we'll see if we find that.</p>
                                <p class="fs-5 mb-4">If you get asteroids about a kilometer in size, those are large enough and carry enough energy into our system to disrupt transportation, communication, the food chains, and that can be a really bad day on Earth.</p>
                                <h2 class="fw-bolder mb-4 mt-5">I have odd cosmic thoughts every day</h2>
                                <p class="fs-5 mb-4">For me, the most fascinating interface is Twitter. I have odd cosmic thoughts every day and I realized I could hold them to myself or share them with people who might be interested.</p>
                                <p class="fs-5 mb-4">Venus has a runaway greenhouse effect. I kind of want to know what happened there because we're twirling knobs here on Earth without knowing the consequences of it. Mars once had running water. It's bone dry today. Something bad happened there as well.</p>
                            </section>
                        </article>
                        <!-- Comments section-->
                        <section class="mb-5">
                            <div class="card bg-light">
                                <div class="card-body">
                                    <!-- Comment form-->
                                    <form class="mb-4"><textarea class="form-control" rows="3" placeholder="Join the discussion and leave a comment!"></textarea></form>
                                    <!-- Comment with nested comments-->
                                    <div class="d-flex mb-4">
                                        <!-- Parent comment-->
                                        <div class="flex-shrink-0"><img class="rounded-circle" src="https://dummyimage.com/50x50/ced4da/6c757d.jpg" alt="..." /></div>
                                        <div class="ms-3">
                                            <div class="fw-bold">Commenter Name</div>
                                            If you're going to lead a space frontier, it has to be government; it'll never be private enterprise. Because the space frontier is dangerous, and it's expensive, and it has unquantified risks.
                                            <!-- Child comment 1-->
                                            <div class="d-flex mt-4">
                                                <div class="flex-shrink-0"><img class="rounded-circle" src="https://dummyimage.com/50x50/ced4da/6c757d.jpg" alt="..." /></div>
                                                <div class="ms-3">
                                                    <div class="fw-bold">Commenter Name</div>
                                                    And under those conditions, you cannot establish a capital-market evaluation of that enterprise. You can't get investors.
                                                </div>
                                            </div>
                                            <!-- Child comment 2-->
                                            <div class="d-flex mt-4">
                                                <div class="flex-shrink-0"><img class="rounded-circle" src="https://dummyimage.com/50x50/ced4da/6c757d.jpg" alt="..." /></div>
                                                <div class="ms-3">
                                                    <div class="fw-bold">Commenter Name</div>
                                                    When you put money directly to a problem, it makes a good headline.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- Single comment-->
                                    <div class="d-flex">
                                        <div class="flex-shrink-0"><img class="rounded-circle" src="https://dummyimage.com/50x50/ced4da/6c757d.jpg" alt="..." /></div>
                                        <div class="ms-3">
                                            <div class="fw-bold">Commenter Name</div>
                                            When I look at the universe and all the ways the universe wants to kill us, I find it hard to reconcile that with statements of beneficence.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                    <!-- Side widgets-->
                    <div class="col-lg-4">
                        <!-- Search widget-->
                        <div class="card mb-4">
                            <div class="card-header">Search</div>
                            <div class="card-body">
                                <div class="input-group">
                                    <input class="form-control" type="text" placeholder="Enter search term..." aria-label="Enter search term..." aria-describedby="button-search" />
                                    <button class="btn btn-primary" id="button-search" type="button">Go!</button>
                                </div>
                            </div>
                        </div>
                        <!-- Categories widget-->
                        <div class="card mb-4">
                            <div class="card-header">Categories</div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-sm-6">
                                        <ul class="list-unstyled mb-0">
                                            <li><a href="#!">Web Design</a></li>
                                            <li><a href="#!">HTML</a></li>
                                            <li><a href="#!">Freebies</a></li>
                                        </ul>
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-unstyled mb-0">
                                            <li><a href="#!">JavaScript</a></li>
                                            <li><a href="#!">CSS</a></li>
                                            <li><a href="#!">Tutorials</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Side widget-->
                        <div class="card mb-4">
                            <div class="card-header">Side Widget</div>
                            <div class="card-body">You can put anything you want inside of these side widgets. They are easy to use, and feature the Bootstrap 5 card component!</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        {% endblock content %}
        

```

