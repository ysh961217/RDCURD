from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import BlogPost

from .models import Blog

# Create your views here.

def index(request):
    blogs = Blog.objects
    return render(request, 'index.html', {'blogs': blogs})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id))

def delete(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('/')

def edit(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = BlogPost(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            blog.title = form.cleaned_data['title']
            blog.body = form.cleaned_data['body']
            blog.save()
            return redirect('/blog/'+str(blog.pk))
        
    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = BlogPost(instance = blog)
        context={
            'form':form,
            'writing':True,
            'now':'edit',
        }
        return render(request, 'edit.html',context)