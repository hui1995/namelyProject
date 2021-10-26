from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from books.models import Book, Category, Comment, Comment2, CollectBook, Article, Message
from user.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from books import spider
import json


def start_spider(request):
    spider.start_spider()
    return JsonResponse({"code": "ok"})
def home(request):
    return redirect("/index")

def index(request):
    books = Book.objects.filter(status=1).order_by("-star")[0:12]
    return render(request, 'index.html', locals())


def booklist(request):
    category_name = request.GET.get("category")
    category = Category.objects.all()
    if category_name is None or category_name == "":
        category_name = category.first().name
    books = Book.objects.filter(category__name=category_name).filter(status=1)
    return render(request, 'booklist.html', locals())


def searchView(request):
    keyword = request.GET.get("keyword")
    books = Book.objects.filter(title__contains=keyword).filter(status=1)
    return render(request, 'result.html', locals())


def DetailView(request):
    id = request.GET.get("id")
    book = Book.objects.filter(id=id).first()
    if book is None:
        return redirect("/book/list/")
    if request.method == "GET":

        data = {}
        data['title'] = book.title
        data['id'] = book.id
        data['star'] = book.star
        data['create_time'] = book.create_time
        data["content"] = book.content[1:-1]
        data['tags'] = json.loads(book.tags)
        data['detail'] = book.detail.split("/")
        collectBook = CollectBook.objects.filter(book_id=id).filter(user_id=request.user.id).first()

        comments = Comment.objects.filter(book__id=id).all()
        commentlist = []
        for i in comments:
            dict1 = {"main": i}
            comments2 = Comment2.objects.filter(comment=i).all()
            dict1["child"] = comments2
            commentlist.append(dict1)
        return render(request, 'booksDetail.html', locals())

    else:
        message = request.POST.get("message")
        Comment.objects.create(content=message, user=request.user, book=book, create_time=datetime.now())
        return redirect("/book/detail/?id=" + id)

@login_required
def addChildView(request):
    id = request.GET.get("id")
    message = request.POST.get("message")
    comment = Comment.objects.filter(id=id).first()
    Comment2.objects.create(user_id=request.user.id, content=message, comment_id=id, create_time=datetime.now())
    return redirect("/book/detail/?id=" + str(comment.book_id))

@login_required
def collectBookView(request):
    id = request.GET.get("id")
    back = request.GET.get("back")
    collectBook = CollectBook.objects.filter(book_id=id).first()
    if collectBook is not None:
        collectBook.delete()
    else:
        CollectBook.objects.create(book_id=id, user_id=request.user.id)
    if back == "my":
        return redirect("/collect/book/")
    return redirect("/book/detail/?id=" + id)


# 书单列表
@login_required
def collectBookList(request):
    user = User.objects.filter(id=request.user.id).first()

    collectBook = CollectBook.objects.filter(user_id=request.user.id).all()
    return render(request, 'my_collect.html', locals())


# 书评
@login_required
def mymessageList(request):
    comments = Comment.objects.filter(user_id=request.user.id).all()
    return render(request, 'my_comment.html', locals())

@login_required
def delmymessage(request):
    id = request.GET.get("id")
    comment = Comment.objects.filter(id=id).first()
    comment.delete()
    return redirect("/book/message/my/")


def artilceList(request):
    id = request.GET.get("id")
    articleList = Article.objects.filter(user_id=id).all()
    return render(request, 'my_artilce.html', locals())

@login_required
def articleDel(request):
    id = request.GET.get("id")
    Article.objects.filter(id=id).delete()
    return redirect("/artile/list/?id=" + str(request.user.id))


def articleDetailInfo(request):
    id = request.GET.get("id")
    article = Article.objects.filter(id=id).first()
    return render(request, 'artilce_detail.html', locals())


# def articleDetail(request):
#     id=request.GET.get("id")
#     article=Article.objects.filter(id=id).first()
#     return render(request,'collectBook.html',locals())


def messageList(request):
    id = request.GET.get("id")
    if request.method == "GET":
        messageList = Message.objects.filter(reply_user_id=id).all()
        print(messageList)
        return render(request, "my_message.html", locals())
    message = request.POST.get("message")
    Message.objects.create(content=message, user=id, create_time=datetime.now(), reply_user=request.user)

    return redirect("/me/message/?id=" + id)

@login_required
def addArticle(request):
    if request.method == "GET":
        return render(request, "add_artilce.html", locals())
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")
        Article.objects.create(title=title, content=content, user=request.user, create_time=datetime.now())
        return redirect("/artile/list/?id=" + str(request.user.id))
