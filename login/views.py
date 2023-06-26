from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')  # 리디렉션을 메인 페이지('/')로 변경
            else:
                form.add_error(None, "아이디 혹은 비밀번호가 틀립니다.")  # 커스텀 오류 메시지 추가
    else:
        form = LoginForm()
    return render(request, 'login/get-a-quote.html', {'form': form})

def policy(request):
    return render(request, 'login/policy.html')

