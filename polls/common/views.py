from django.contrib.auth.models import User
from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import UserForm, SignupForm

from django.contrib.auth import authenticate, login, logout

import pytesseract
from PIL import Image


# 회원 가입
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            is_business = form.cleaned_data.get('is_business')

            if is_business:
                business_license = form.cleaned_data.get('business_license')
                # 사업자 등록증 파일 처리
                user.business_license = business_license

            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password, last_name=last_name, email=email)
            login(request, user)
            return redirect('/')  # index 페이지로 이동
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'common/signup.html', context)

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #로그인
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = "아이디와 비밀번호를 확인해 주세요"
            return render(request, 'common/login.html', {'error': error})
    else:
        return render(request, 'common/login.html')

def signout(request):
    logout(request)
    return redirect('/')

def extract_text_from_image(image_file):
    # 이미지 열기
    image = Image.open(image_file)

    # 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(image, lang="kor+eng")

    # 추출된 텍스트 반환
    return text

# 마이 페이지
def mypage(request):
    req = request.user.username
    user = User.objects.get(username=req)

    context = {
        'user': user,
    }

    return render(request, 'common/mypage.html', context)