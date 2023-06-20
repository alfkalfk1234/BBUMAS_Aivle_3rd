from django.contrib.auth import get_user_model

def sign_up(username, password, email,phone):
    User = get_user_model()
    user = User.objects.create_user(username=username, password=password, email=email,phone=phone)
    # 추가 필요한 정보를 저장하거나 추가 동작을 수행할 수 있음
    user.save()
    return user