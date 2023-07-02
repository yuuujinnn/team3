
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#회원가입 폼
class UserForm(UserCreationForm):
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'last_name', 'email']
        

#사업자 회원가입 폼
class SignupForm(UserCreationForm):
    # 추가 필드 정의
    is_business = forms.BooleanField(label='사업자 여부', required=False)
    business_license = forms.FileField(label='사업자 등록증', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_business', 'business_license')