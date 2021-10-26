"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books import views as books
from user import views as user
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', books.index),
    path('book/list/', books.booklist),
    path("book/detail/",books.DetailView),
    path("book/collect/",books.collectBookView),
    path("book/message/my/",books.mymessageList),
    path("book/message/del/",books.delmymessage),
    path("artile/list/",books.artilceList),
    path('search/', books.searchView),
    path('spider/', books.start_spider),
    path('person/', user.personView),
    path('collect/book/', books.collectBookList),
    path('add/comment/', books.addChildView),
    path('login/', user.loginUser),
    path('signup/', user.signup),
    path('logout/', user.logoutuser),
    path('password/', user.changepassword),
    path('change/person/', user.changeperson),
    path('change/pic/', user.changePic),
    path('me/message/', books.messageList),
    path('add/article/', books.addArticle),
    path('article/del/', books.articleDel),
    path('article/detail/', books.articleDetailInfo),
    path('', books.home),
]
