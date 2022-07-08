from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from qna.models import Profile

def login(request):
    if request.method == 'POST':
        usr = request.POST['username']
        pwd = request.POST['password']

        user = auth.authenticate(request,username=usr,password=pwd)

        if user is not None:
            auth.login(request,user)
            return redirect('main:landing')

        else:
            return render(request,'login.html')

    elif request.method == 'GET':
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        # password와 confirm에 입력된 값이 같다면
        if request.POST['password'] == request.POST['confirm']:
            # user 객체를 새로 생성
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            # 로그인 한다
            auth.login(request, user)
                        
            profile = Profile()
            profile.user = user
            profile.save()

            return redirect('users:mypage_edit')
    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다
    return render(request, 'signup.html')
# Create your views here.
