from django.shortcuts import render, redirect, get_object_or_404
from .models import Professor, Department, Major, Question, Answer, Profile
from django.utils import timezone
from django.db.models import Q
# Create your views here.

def majorList(request):
    try :
        #현재 로그인한 user의 profile을 가져옵니다.
        user_profile = get_object_or_404(Profile, user = request.user)
        #profile에서 학과를 불러옵니다.(여러개일수도 있어서 all 사용)
        user_department = user_profile.department.all()
        #질문글을 담을 리스트
        questions_list = []
        #학과의 전공들을 가져옵니다.
        for d in user_department:
            user_majors = Major.objects.filter(department=d)
            #전공의 질문들을 가져옵니다.
            for m in user_majors: 
                questions = Question.objects.filter(major = m)
                #질문들을 리스트에 반복문으로 집어넣습니다.
                for q in questions:
                    questions_list.append(q)
        #질문들이 들어있는 리스트를 시간순으로 정렬합니다.(order_by는 queryset형태가 아니라 쓸 수 없음)
        questions_list = sorted(questions_list, key=lambda x: x.pub_date)

        done_wait = False

        questions_result = []
        #post 요청(답변을 기다리는 질문/채택 완료된 질문)이 들어오면
        if request.method == 'POST':
            #채택완료된 질문만 보여준다
            if request.POST['selection'] == "done":
                done_wait = True
                for q in questions_list:
                    #한 질문의 모든 답변 불러오기
                    answers = q.answers.all()
                    #답변에 채택 완료된게 있으면, 최종 리스트에 질문을 추가한다.
                    for a in answers:
                        if a.selection == True:
                            questions_result.append(q)

            #답변을 기다리는 질문만 보여준다
            elif request.POST['selection'] == "wait":
                for q in questions_list:
                    questions_result.append(q)
                for q in questions_list:
                    answers = q.answers.all()
                    for a in answers:
                        if a.selection == True:
                            questions_result.remove(q)
        #get요청 > 채택 여부 상관없이 전부 보여줌 > questions가 최종 결과물
        else :
            questions_result = questions_list

        return render(request, 'qna/majorList.html', {
            'questions':questions_result,
            'departments':user_department,
            'majors':user_majors,
            'if_done_wait': done_wait,
        })
    except :
        return render(request, 'qna/majorList.html')

def nonmajorList(request):
    #전공이 없는 질문들을 시간순 정렬
    questions = Question.objects.filter(major = None).order_by('-pub_date')
    #최종 질문들을 넣을 리스트 생성
    questions_result = []
    #post 요청(답변을 기다리는 질문/채택 완료된 질문)이 들어오면
    done_wait = False
    if request.method == 'POST':
        #채택완료된 질문만 보여준다
        if request.POST['selection'] == "done":
            done_wait = True
            for q in questions:
                #한 질문의 모든 답변 불러오기
                answers = q.answers.all()
                #답변에 채택 완료된게 있으면, 최종 리스트에 질문을 추가한다.
                for a in answers:
                    if a.selection == True:
                        questions_result.append(q)
        #답변을 기다리는 질문만 보여준다
        elif request.POST['selection'] == "wait":
            for q in questions:
                questions_result.append(q)
            for q in questions:
                answers = q.answers.all()
                for a in answers:
                    if a.selection == True:
                        questions_result.remove(q)
    #get요청 > 채택 여부 상관없이 전부 보여줌 > questions가 최종 결과물
    else :
        questions_result = questions

    return render(request, 'qna/nonmajorList.html', {
        'questions':questions_result,
        'if_done_wait': done_wait,
    })

def detail(request, id):
    question = get_object_or_404(Question, pk = id)
    all_answers = question.answers.all().order_by('created_at')
    if_q_solved = False
    comments_count = question.answers.count()
    user_profile = get_object_or_404(Profile, user = request.user)
    
    for a in all_answers:
        if a.selection == True:
            if_q_solved = True
    question_writer = question.writer
    
    return render(request, 'qna/detail.html', {
        'question':question, 
        'answers':all_answers,
        'if_q_solved':if_q_solved,
        'question_writer': question_writer,
        'user_profile':user_profile,
        'comments_count' : comments_count,
        })

def major_new(request):
    #현재 로그인한 user의 profile을 가져옵니다.
    user_profile = get_object_or_404(Profile, user = request.user)
    #profile에서 학과를 불러옵니다.(여러개일수도 있어서 all 사용)
    user_department = user_profile.department.all()
    user_major_list = []
    for d in user_department:
        user_majors = Major.objects.filter(department=d)
        for m in user_majors: 
            user_major_list.append(m)
    return render(request, 'qna/major_new.html', {
        'majors': user_major_list,
    })


def nonmajor_new(request):
    #현재 로그인한 user의 profile을 가져옵니다.
    user_profile = get_object_or_404(Profile, user = request.user)
    #profile에서 학과를 불러옵니다.(여러개일수도 있어서 all 사용)
    user_department = user_profile.department.all()
    user_major_list = []
    for d in user_department:
        user_majors = Major.objects.filter(department=d)
        for m in user_majors: 
            user_major_list.append(m)
    return render(request, 'qna/nonmajor_new.html', {
        'majors': user_major_list,
    })

def major_create(request):
    new_question = Question()
    new_question.title = request.POST['title']
    user_profile = get_object_or_404(Profile, user = request.user)
    new_question.writer = user_profile
    new_question.pub_date = timezone.now()
    new_question.body = request.POST['body']
    new_question.image = request.FILES.get('image')
    new_question.major = get_object_or_404(Major, id = request.POST['major'])
    new_question.save()
    return redirect('qna:detail', new_question.id)

def nonmajor_create(request):
    new_question = Question()
    new_question.title = request.POST['title']
    user_profile = get_object_or_404(Profile, user = request.user)
    new_question.writer = user_profile
    new_question.pub_date = timezone.now()
    new_question.body = request.POST['body']
    new_question.image = request.FILES.get('image')
    new_question.major = None
    new_question.save()
    return redirect('qna:detail', new_question.id)

def edit(request, id):
    edit_question = Question.objects.get(id = id)
    #현재 로그인한 user의 profile을 가져옵니다.
    user_profile = get_object_or_404(Profile, user = request.user)
    #profile에서 학과를 불러옵니다.(여러개일수도 있어서 all 사용)
    user_department = user_profile.department.all()
    user_major_list = []
    for d in user_department:
        user_majors = Major.objects.filter(department=d)
        for m in user_majors: 
            user_major_list.append(m)
    return render(request, 'qna/edit.html', {
        'question' : edit_question,
        'majors': user_major_list,
        })

def update(request, id):
    update_question = Question.objects.get(id=id)
    update_question.title = request.POST['title']
    user_profile = get_object_or_404(Profile, user = request.user)
    update_question.writer = user_profile
    update_question.pub_date = timezone.now()
    update_question.body = request.POST['body']
    update_question.image = request.FILES.get('image')
    if request.POST['major'] == 'nothing':
        update_question.major = None
    else:
        update_question.major = get_object_or_404(Major, name = request.POST['major'])
    update_question.save()
    return redirect('qna:detail', update_question.id)

def delete(request , id):
    delete_question = Question.objects.get(id = id)
    delete_question.delete()
    return redirect('main:landing')

def create_answer(request, question_id):
    new_answer = Answer()
    user_profile = get_object_or_404(Profile, user = request.user)
    new_answer.writer = user_profile
    new_answer.content = request.POST['content']
    new_answer.created_at = timezone.now()
    new_answer.question = get_object_or_404(Question, pk=question_id)
    new_answer.image = request.FILES.get('image')
    new_answer.save()
    return redirect('qna:detail', question_id)

def edit_answer(request, question_id, answer_id):
    target_question = Question.objects.get(id = question_id)
    edit_answer = Answer.objects.get(id = answer_id)
    return render(request, 'qna/edit_answer.html', {'question':target_question, 'answer' : edit_answer})

def update_answer(request, question_id, answer_id):
    target_question = Question.objects.get(id = question_id)
    update_answer = Answer.objects.get(id = answer_id)
    update_answer.content = request.POST['content']
    user_profile = get_object_or_404(Profile, user = request.user)
    update_answer.writer = user_profile
    update_answer.image = request.FILES.get('image')
    update_answer.save()
    return redirect('qna:detail', target_question.id)
  
def delete_answer(request , question_id, answer_id):
    target_question = Question.objects.get(id = question_id)
    delete_answer = Answer.objects.get(id = answer_id)
    delete_answer.delete()
    return redirect('qna:detail', target_question.id)

def likes(request, id):
    if request.user.is_authenticated:
        question = get_object_or_404(Question, pk=id)

        if question.like_users.filter(pk=request.user.pk).exists():
            question.like_users.remove(request.user)
        else:
            question.like_users.add(request.user)
        return redirect('qna:detail', question.id)
    return redirect('accouts:login')

def search(request):
    question_list = Question.objects.all()
    search = request.GET.get('search', '')
    if search:
        question_list = question_list.filter(
        Q(title__icontains = search) | #제목
        Q(body__icontains = search) | #내용
        Q(writer__username__icontains = search) | #글쓴이
        Q(major__name__icontains = search) | #전공
        Q(major__professor__name__icontains = search) #교수
        )
    return render(request, 'qna/searchList.html', {
        'questions':question_list, 'search':search
        })

def select(request, question_id, answer_id):
    question = Question.objects.get(id = question_id)
    target_answer = Answer.objects.get(id = answer_id)
    if request.POST['select'] == "True":
        target_answer.selection = True
    else:
        target_answer.selection = False
    target_answer.save()
    return redirect('qna:detail', question.id)