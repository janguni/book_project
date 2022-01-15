from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms
from django.core.exceptions import ValidationError

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(self.error_messages["duplicate_username"])

class SignUpForm(django_forms.ModelForm) :
    class Meta :
        model = User
        fields = ['username', 'email', 'nickname', 'password', 'password2']

        widgets = {
            'username' : django_forms.TextInput(attrs={'placeholder': '아이디'}),
            'email' : django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'nickname' : django_forms.TextInput(attrs={'placeholder': '닉네임'}),            
            'password' : django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
            'password2' : django_forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}),
        }

    def save(self, commit=True) :
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit :
            user.save()
        return user