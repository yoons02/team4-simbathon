from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#교수
class Professor(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

#학과
class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


#전공(수업)
class Major(models.Model):
    name = models.CharField(max_length=20)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='majors')
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name


#개인프로필, auth의 User를 일대일 필드로 가짐
class Profile(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    image = models.ImageField(upload_to = "image/", blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, related_name="department")
    sub_department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, related_name="sub_department")
    introduction = models.TextField(max_length=300, blank=True, null=True)

    FRESHMAN = '1학년'
    SOPHOMORE = '2학년'
    JUNIOR = '3학년'
    SENIOR = '4학년'
    POSTGRAD = '대학원생'
    GRADUATED = '졸업생'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, '1학년'),
        (SOPHOMORE, '2학년'),
        (JUNIOR, '3학년'),
        (SENIOR, '4학년'),
        (POSTGRAD, '대학원생'),
        (GRADUATED, '졸업생'),
    ]
    year_in_school = models.CharField(
        max_length=10,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )


    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)

    def __str__(self):
        return self.name


#질문
class Question(models.Model):
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    body = models.TextField()
    major = models.ForeignKey(Major, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to = "question/", blank=True, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='like_questions')
    
    def __str__(self):
        return self.title

    def title_short(self):
        return f"{self.title[:12]}..."
    
    def summary_short(self):
        return f"{self.body[:40]}..."

    def summary_long(self):
        return f"{self.body[:240]}..."

    def like_counts(self):
        return self.like_users.count()

#질문에 업로드하는 이미지(미완성)
class QuestionImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(default='media/diary/default_image.jpeg', upload_to='diary', blank=True, null=True)      

#답변
class Answer(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField()
    image = models.ImageField(upload_to = "answer/", blank=True, null=True)
    selection = models.BooleanField(default = False)

    def __str__(self):
        return self.content[:20]
