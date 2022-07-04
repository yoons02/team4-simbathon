from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
  path('mypage/', mypage, name="mypage"),
  path('mypage_new/', mypage_new, name="mypage_new"),
  path('mypage_create/', mypage_create, name="mypage_create"),
  path('mypage_edit/', mypage_edit, name="mypage_edit"),
  path('mypage_update/', mypage_update,name="mypage_update"),
  path('myprofile_set/', myprofile_set, name="myprofile_set"),
  path('myprofile_save/', myprofile_save, name="myprofile_save"),
]

# get방식 요청이 접근 > urls.py > views.py > html 순서대로 넘어가는데
# 처음에 mypage_edit, mypage_update에서 <int:id>이런식으로 인자를 넘겨줬잖아?
# 그러면 views.py 에서도 def mypage_edit(request, id): 이런식으로 인자를 받아줘야돼(변수 이름 같아야함)
# 우리 세션때 만들었던 crud에 urls.py랑 views.py 보면 인자 넘겨주는걸 확인할 수 있을거야
# 그런데 프로필은 request.user로 접속한 계정에 접근할수있으니까 따로 id를 넘겨줄 필요는 없을것같아서 지웠어
# 톡방에서 질문해준거 보면 profile 수정 아이디를 뭘 받아야될지 모르겠다고 물어봤는데
# user의 id를 받아와야 수정할 수 있는데 user의 id에 접근하려면
# get방식이나 post방식으로 html url 딴에서 id를 보내야되는데 좀 어려워서 request.user로 가져왔어
# 질문 crud 같은 경우에는 {% for question in questions %}를 돌면서 url 안에 {% url 'qna:update' question.id %} 같은 방식으로 get방식으로 보내서 가져왔었지 
# 수정사항반영
