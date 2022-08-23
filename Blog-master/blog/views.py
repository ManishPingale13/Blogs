from django.shortcuts import render,HttpResponse,redirect
from .models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras


# Create your views here.
def blogHome(request):
    allPosts =  Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html',context)


def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict={}
    for reply in replies:
        if reply.parent.serialNum not in repDict.keys():
            repDict[reply.parent.serialNum]=[reply]
        else:
            repDict[reply.parent.serialNum].append(reply)
    print(repDict)
    context = {'post': post,'comments': comments,'user':request.user,'replyDict':repDict}
    return render(request, 'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST':
        user = request.user
        comment = request.POST.get('comment')
        postSno = request.POST.get('postSno')
        post= Post.objects.get(serialNum=postSno)
        parentSno = request.POST.get('parentSerialNum')
        if parentSno == "":
            comment = BlogComment(user=user, comment=comment, post=post)
            comment.save()
            messages.success(request, "Comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(serialNum=parentSno)
            comment = BlogComment(user=user, comment=comment, post=post,parent=parent)
            comment.save()
            messages.success(request, "Reply has been posted successfully")
    return redirect(f'/blog/{post.slug}')