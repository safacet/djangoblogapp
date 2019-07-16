from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def articles(request):
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles": articles})


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url = 'user:login')
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url = '/user/login')
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()
        id = article.id
        messages.success(request, "<strong>Teşekkürler!</strong> Makaleniz Başarıyla Eklendi")
        return redirect(reverse("article:detail", kwargs={"id": id})) 
    return render(request, "addarticle.html", {"form": form})

def detail(request, id):
    article = get_object_or_404(Article, id = id)
    comment_name = request.POST.get("name")
    comment_content =request.POST.get("comment")
    if comment_name and comment_content:
        comment = Comment(article = article, comment_author = comment_name, comment_content = comment_content)
        comment.save()
    elif comment_name or comment_content:
        messages.error(request, "<strong>Opps!</strong> Yorum yaparken tüm alanları doldurmanız gerekiyor")
    comments = Comment.objects.filter(article = id).all()
    return render(request, "detail.html", {"article": article, "comments":comments})

@login_required(login_url = '/user/login')
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance= article)
    if form.is_valid():
        form.save()
        messages.success(request, "<strong>Teşekkürler!</strong> Makaleniz Başarıyla Güncellendi")
        return redirect(reverse("article:detail", kwargs= {"id": id}))
    return render(request, "update.html", {"form": form})

@login_required(login_url = '/user/login')
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.warning(request, "<strong>Silindi!</strong> Artık böyle bir makale yok")
    return redirect("dashboard")

def searchArticle(request):
    keyWord = request.POST.get("keyword")
    articles_title = Article.objects.filter(title__icontains = keyWord).all()
    articles_content = Article.objects.filter(content__icontains = keyWord).all()
    context = {
        "titles": articles_title,
        "contents": articles_content
    }
    return render(request, "search.html", context)