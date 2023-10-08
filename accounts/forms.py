from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password,get_default_password_validators
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class RegistForm(forms.ModelForm):
     username = forms.CharField(label='名前')
     email = forms.EmailField(label='メールアドレス')
     password = forms.CharField(label='パスワード', widget=forms.PasswordInput)

     class Meta:
          model = Users
          fields = ['username','email','password']
    #パスワードの暗号化
     def save(self, commit=False):
        user = super().save(commit=False)
        #passwordが適切かどうかを確認する
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.is_approved = False
        user.save()
        return user
   
class AdminRegistForm(UserCreationForm):
    is_admin = forms.BooleanField(label='管理ユーザー', required=False)
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')

    def clean_password(self):
        password = self.cleaned_data["password1"]
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_admin = self.cleaned_data.get("is_admin", False)
            user.save()

            # 最初の管理者ユーザーを設定
            if user.is_admin and not Users.objects.filter(is_first_admin=True).exists():
                user.is_first_admin = True
                user.approvor = None
            else:
                user.is_first_admin = False
                user.approvor = Users.objects.filter(is_first_admin=True).first()

            user.save()

        return user

    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']

          
          



     
        
     
# class UserLoginForm(forms.Form):
#     email = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput)

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')#modelsのUserクラスでログインするためにemailを使うよう設定したためusernameはemailになる
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態を保持する', required= False)

    