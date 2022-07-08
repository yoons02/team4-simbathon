from django.shortcuts import render, redirect, get_object_or_404
from qna.models import Question, Profile, Department, Answer

def mypage(request):
   #내가 쓴 글 필터링하는 함수
   user_profile = get_object_or_404(Profile, user = request.user)
   questions=Question.objects.filter(writer=user_profile)
   user_department = user_profile.department
   user_sub_department = user_profile.sub_department
   answers=Answer.objects.filter(writer=user_profile)
   count_q = questions.count()
   count_a = answers.count()
   return render(request,'users/mypage.html',{
      'questions':questions,
      'profile':user_profile,
      'user_department':user_department,
      'user_sub_department':user_sub_department,
      'answers': answers,
      'count_q': count_q,
      'count_a': count_a,
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
   departments = Department.objects.all()
   myprofile = get_object_or_404(Profile, user=request.user)
   user_department =  myprofile.department
   user_sub_department = myprofile.sub_department
   department_list = departments
   sub_department_list = departments
   return render(request,'users/mypage_edit.html',{
      'user_department':user_department,   
      'user_sub_department':user_sub_department,
      'profile':myprofile,
      'department_list':department_list,
      'sub_department_list':sub_department_list,
      })

def mypage_update(request):
   update_mypage = get_object_or_404(Profile, user = request.user)
   update_mypage.introduction = request.POST['intro']
   update_mypage.image = request.FILES.get('profile_image')
   update_mypage.name = request.POST['name']
   if request.POST['department'] != '':
      update_mypage.department = Department.objects.get(name = request.POST['department'])
   if request.POST['sub_department'] != '':
      update_mypage.sub_department = Department.objects.get(name = request.POST['sub_department'])
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
   else :
      pass
   update_mypage.save()
   return redirect('users:mypage')
