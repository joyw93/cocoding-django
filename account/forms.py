from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from account.models import User


class SignupForm(UserCreationForm):
    username = forms.CharField(label="이름")
    email = forms.EmailField(label="이메일")
    nickname = forms.CharField(label="닉네임")
    password1 = forms.CharField(label="비밀번호")
    password2 = forms.CharField(label="비밀번호확인")


    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_length = len(username)
        if not 1<=username_length<=10:
            raise forms.ValidationError('이름은 1~10자 이내로 입력해야합니다.')
        return username


    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        nickname_length = len(nickname)
        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 사용중인 닉네임입니다.')
        if not 1<=nickname_length<=10:
            raise forms.ValidationError('닉네임은 2~10자 이내로 입력해야합니다.')
        return nickname


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_length = len(email)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용중인 이메일입니다.')
        if email_length>=255:
            raise forms.ValidationError('이메일 형식이 올바르지 않습니다.')
        return email


    class Meta:
        model = User
        fields = ("username", "nickname", "email", "password1", "password2")