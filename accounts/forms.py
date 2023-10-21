from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password,get_default_password_validators
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class RegistForm(UserCreationForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    #  password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    
    def clean_password(self):
        password = self.cleaned_data["password1"]
        validate_password(password)
        return password
    
    class Meta:
            model = Users
            fields = ['username', 'email', 'password1', 'password2']
   
class AdminRegistForm(UserCreationForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')

    def clean_password(self):
        password = self.cleaned_data["password1"]
        validate_password(password)
        return password

    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']

          
          

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')#modelsのUserクラスでログインするためにemailを使うよう設定したためusernameはemailになる
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態を保持する', required= False)

    