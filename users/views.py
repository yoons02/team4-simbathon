from django.shortcuts import render, redirect, get_object_or_404
from qna.models import Question, Profile, Department, Answer

def mypage(request):
   #내가 쓴 글 필터링하는 함수
   user=request.user
   questions=Question.objects.filter(writer=user)
   user_profile=get_object_or_404(Profile, user=user)
   user_department = user_profile.department.all()
   edit_mypage = get_object_or_404(Profile, user = request.user)
   answers=Answer.objects.filter(writer=user)
   return render(request,'users/mypage.html',{
      'questions':questions,
      'profile':user_profile,
      'user_department':user_department,
      'mypage' : edit_mypage,
      'answers': answers,
      })


def mypage_new(request):
   return render(request, 'users/mypage_new.html')



# Mypage에 쓴 자신 정보 수정하고 생성하는 함수/수정하면 mypage로 돌아가게
def mypage_create(request):
    new_mypage = get_object_or_404(Profile, user = request.user)
    new_mypage.introduction = request.POST['intro']
    #Profile 모델에서 자기소개를 introduction으로 선언해줬으니까 .introduction으로 불러와야 돼
    new_mypage.image = request.FILES.get('profile_image')
    new_mypage.save()
    return redirect('users:mypage')

def mypage_edit(request):
   #질문 작성 crud에서는 질문의 id를 가져와서 수정했던거에 비해 프로필은 request.user로 현재 로그인된 계정을 불러올수 있으니까 따로 id를 선언해줄 필요 없어
   edit_mypage = get_object_or_404(Profile, user = request.user)
   
   departments = Department.objects.all()
   myprofile = get_object_or_404(Profile, user=request.user)
   mine =  myprofile.department.all()
   plus_result = []
   minus_result = []
   for d in departments:
      if d in mine:
         minus_result.append(d)
      else:
         plus_result.append(d)
   return render(request,'users/mypage_edit.html',{
      'mypage' : edit_mypage,
      'plus_departments':plus_result,   
      'minus_departments':minus_result,
      'profile':myprofile,
      })

def mypage_update(request):
   update_mypage = get_object_or_404(Profile, user = request.user)
   update_mypage.introduction = request.POST['intro']
   update_mypage.image = request.FILES.get('profile_image')
   update_mypage.name = request.POST['name']
   if request.POST['plus_department'] != '':
      department = Department.objects.get(name = request.POST['plus_department'])
      update_mypage.department.add(department)
   if request.POST['minus_department'] != '':
      department = Department.objects.get(name = request.POST['minus_department'])
      update_mypage.department.remove(department)
   grade = request.POST['grade']

   FRESHMAN = '1학년'
   SOPHOMORE = '2학년'
   JUNIOR = '3학년'
   SENIOR = '4학년'
   POSTGRAD = '대학원생'
   GRADUATED = '졸업생'
   if grade == "1":
      update_mypage.year_in_school = FRESHMAN
   elif grade == "2":
      update_mypage.year_in_school = SOPHOMORE
   elif grade == "3":
      update_mypage.year_in_school = JUNIOR
   elif grade == "4":
      update_mypage.year_in_school = SENIOR 
   elif grade == "pg":
      update_mypage.year_in_school = POSTGRAD 
   elif grade == "gr":
      update_mypage.year_in_school = GRADUATED
   update_mypage.save()
   return redirect('users:mypage')

def myprofile_set(request):
   departments = Department.objects.all()
   myprofile = get_object_or_404(Profile, user=request.user)
   mine =  myprofile.department.all()
   plus_result = []
   minus_result = []
   for d in departments:
      if d in mine:
         minus_result.append(d)
      else:
         plus_result.append(d)
   return render(request, 'users/myprofile_set.html',{
      'plus_departments':plus_result,   
      'minus_departments':minus_result,
      'profile':myprofile,
   })

def myprofile_save(request):
   myprofile = get_object_or_404(Profile, user=request.user)
   myprofile.name = request.POST['name']
   if request.POST['plus_department'] != '':
      department = Department.objects.get(name = request.POST['plus_department'])
      myprofile.department.add(department)
   if request.POST['minus_department'] != '':
      department = Department.objects.get(name = request.POST['minus_department'])
      myprofile.department.remove(department)
   grade = request.POST['grade']
   
   FRESHMAN = '1학년'
   SOPHOMORE = '2학년'
   JUNIOR = '3학년'
   SENIOR = '4학년'
   POSTGRAD = '대학원생'
   GRADUATED = '졸업생'
   if grade == "1":
      myprofile.year_in_school = FRESHMAN
   elif grade == "2":
      myprofile.year_in_school = SOPHOMORE
   elif grade == "3":
      myprofile.year_in_school = JUNIOR
   elif grade == "4":
      myprofile.year_in_school = SENIOR 
   elif grade == "pg":
      myprofile.year_in_school = POSTGRAD 
   elif grade == "gr":
      myprofile.year_in_school = GRADUATED
   myprofile.save()
   return redirect('users:mypage')