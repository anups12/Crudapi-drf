from django.shortcuts import redirect, render
from . models import *
from . forms import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CourseSerializer, RegisterSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
# Create your views here.

def Home(request):
    courses= Course.objects.all()
    try:
        if request.user.reader:
            enroll = Enrolled.objects.filter(user=request.user.reader)
    except:
        enroll = {}
    context={'courses':courses, 'enroll':enroll}
    return render(request, 'index.html', context)


def SigninPage(request):
    form = CreatorRegister()
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            print(request.POST)
            form = CreatorRegister(request.POST)
            usertype = request.POST.get('radio')
            if form.is_valid():
                user = form.save()
                if usertype =='creator':
                    Creator.objects.create(username=user, name=user.username)
                elif usertype=='reader':
                    Reader.objects.create(username=user, name=user.username)
                messages.success(request, 'User created Successfully '+ user.username)
                return redirect('/')
    context={'form':form}
    return render(request, 'signin.html', context)

def LoginView(request): 
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                messages.success(request, 'You are  logged in as '+ request.user.username)
                try:
                    if request.user.creator:
                        return redirect('/')
                except:
                    return redirect('/login/')
            else:
                messages.warning(request, "Either your username or password is wrong")
    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    messages.warning(request, 'Your have logged out  ')
    return redirect('/')

def CreateCourse(request):
    form = CourseCreateForm()
    if request.method=='POST':
        form = CourseCreateForm(request.POST, request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.user = request.user.creator
            course.save()
            return redirect('/')
    context={'form':form}
    return render(request, 'create_course.html', context)

def CourseDetails(request, pk):
    course = Course.objects.get(id=pk)
    users_enrolled =course.enrolled_set.all()
    try:
        if request.user.reader:
            enroll = Enrolled.objects.filter(courses=course, user=request.user.reader).exists()
    except:
        enroll = {}
    context={'course':course, 'enroll':enroll, 'users_enrolled':users_enrolled}
    return render(request, 'course.html', context)


def EnrollCourse(request, pk):
    if request.method=='POST':
        user= request.user.reader
        course= Course.objects.get(id=pk)
        if Enrolled.objects.filter(courses=course, user=user).exists():
            return redirect('/')
        else:
            enroll = Enrolled.objects.create(courses=course, user=user)
            enroll.save()
            return redirect('/')
    
def EditCourse(request, pk):
    course = Course.objects.get(id=pk)
    form =CourseCreateForm(instance = course)
    if request.method=='POST':
        form = CourseCreateForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course=form.save(commit=False)
            course.user = request.user.creator
            course.save()
            messages.success(request, 'You have enrolled to ' + course + 'successfully')
            return redirect('/')
    context = {'form':form}
    return render(request, 'editpost.html', context )




# <-------------------API views -------------------->

class TaskApi(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, pk=None, format=None):
# <----------------------GET DATA FROM THE DATABASE --------------->
        if pk is not None:
            try:
                course = Course.objects.get(id=pk)
                serializer = CourseSerializer(course)
                return Response(serializer.data)
            except:
                return Response({'message': "The data you are requesting is not available or deleted "})
        else:       
            task = Course.objects.all()
            serializer=CourseSerializer(task, many=True)
            return Response(serializer.data )

# <----------------------To add data  (POST request) --------------->
    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response({'message':'Your data has been added successfully '})
        return Response(serializer.errors)

# <----------------------FOR COMPLETE DATA UPDATE --------------->
    def put(self, request,pk, format=None):
        try:
            task = Course.objects.get(id=pk)
            serializer = CourseSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Your data has been Updated successfully '})
        except:
            return Response({"Error message": "Check the id of the post you are trying to update "})
        return Response(serializer.errors)


# <----------------------FOR  PARTIAL DATA UPDATE --------------->
    def patch(self, request,pk, format=None):
        try:
            task = Course.objects.get(id=pk)
            serializer = CourseSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Your data has been Updated successfully '})
        except:
            return Response({"Error message": "Check the id of the post you are trying to update "})
        return Response(serializer.errors)

    def delete(self, request,pk, format=None):
        try:
            task = Course.objects.get(id=pk)
            task.delete()
            return Response({'message':'Your data has been Deleted  '})
        except:
            return Response({'message': "The data you are requesting is not available or deleted "})
        
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)