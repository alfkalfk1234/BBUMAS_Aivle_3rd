from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .utils import sign_up
def signup_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            user = sign_up(username, password, email,phone)
            return redirect('login:login')
    else:
        form = UserForm()
    return render(request, 'join/join.html', {'form': form})
    