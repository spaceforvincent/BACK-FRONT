1. python -m venv venv
2. source venv/Scripts/activate (mac : source/venv/bin/activate)
3. pip install django==3.2.12
4. django-admin startproject blog .
5. settings.py ->  'DIRS': [BASE_DIR / 'templates'],

6. templates 폴더 프로젝트 바깥에 생성

7. settings.py -> DATABASES -> 'NAME': BASE_DIR / 'db' / 'db.sqlite3', 

8. LANGUAGE_CODE = 'ko-kr'

   TIME_ZONE = 'Asia/Seoul'

   USE_TZ = False

9. settings.py에 추가

```python
STATICFILES_DIRS = (BASE_DIR / 'static',)
#STATIC_ROOT = 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

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

14.templates 폴더에 agency 부트스트랩 파일들 복사해와서 index.html -> home.html 이름 변경

