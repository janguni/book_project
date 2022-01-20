from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignupForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username', 'password', 'password2', 'email', 'nickname']

    # widgets = {
    #         'username' : forms.TextInput(attrs={'placeholder': '아이디'}),
    #         'password' : forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
    #         'email' : forms.TextInput(attrs={'placeholder': '이메일 주소'}),
    #         'nickname' : forms.TextInput(attrs={'placeholder': '닉네임'}),       
    #     }

    # labels = {
    #         'username': 'ID',
    #         'password': '비밀번호',
    #         'email': 'EMAIL',
    #         'nickname' : '닉네임',
    #     }

    def save(self, commit=True) :
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit :
            user.save()
        return user

    # id 중복 검사 
    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('아이디가 이미 사용중입니다')
        return username

    # password와 password2의 값이 일치하는지 유효성 검사
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다')
        return password2
    
    def signup(self):
        if self.is_valid():
            return CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password2']
            )