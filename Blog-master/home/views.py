from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.

#Nav Shit
def home(request):
    allPosts =  Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'home/home.html',context)

def search(request):
    query = request.GET['query']
    if len(query) > 69:
        allPosts = []
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent =  Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle|allPostsContent
    context={'allPosts':allPosts,'query':query}
    return render(request, 'home/search.html',context)

def contact(request):
    messages.success(request,"Welcome to contact")
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')

        if len(name) < 2 or len(email) < 2 or len(phone) < 10 or len(content) < 4:
            messages.error(request,"Please fill valid details")
        else:
            contact = Contact(name=name, email=email, phoneNum=phone, content=content)
            contact.save()
            messages.success(request,"Successfully submitted")
        
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

#Auth API Shit
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>10:
            print(len(username))
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handleLogIn(request):
    if request.method == 'POST':
        username=request.POST['loginusername']
        password=request.POST['loginpass']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully Logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials.")
            return redirect('home')
    else:
        return HttpResponse("404 - Not found")

def handleLogOut(request):
    logout(request)
    messages.success(request,"Successfully Logged out")
    return redirect('home')

