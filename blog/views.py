from blog.models import Post, BlogComment
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from blog.templatetags import extras
import math

# Create your views here.


def blogHome(request):
    '''
        Pagination Design and logic.  < -- can ask me
        check my Logic book TimeStamp : 1557-070721 < -- I will check here
    '''

    no_of_posts = 2
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    allPosts = Post.objects.all()
    length = len(allPosts)
    allPosts = allPosts[(page-1)*no_of_posts: page*no_of_posts]
    if page > 1:
        prev = page - 1
    else:
        prev = None
    if page < math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None
    
    context = {'allPosts': allPosts, 'prev': prev, 'nxt': nxt}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()

    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    print(replyDict)
    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "your comment has been posted succesfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "your reply has been posted succesfully")

    return redirect(f"/blog/{post.slug}")
