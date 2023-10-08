from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser,PermissionsMixin    
)
from django.urls import reverse_lazy

# Create your models here.

#Managerの作成
class UserManager(BaseUserManager):
    #userの作成
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username = username,
            email = email
        )
        user.set_password(password)#passwordを引数にとってdbに保存する
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        #userを作成
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username = username,
            email = email,
        )
        #password設定
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self.db)
        return user
    

#カスタマイズ用のユーザー作成 
class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    user = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_pending_approval = models.BooleanField(default=False)
    is_first_admin =models.BooleanField(default=False)

    #このテーブルを一位に識別するためのフィールドでemailでログインする
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']#superuserを作成するために必要

    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if self.is_admin:
            if not self.is_first_admin:
                self.is_pending_approval = True
            else:
                self.is_pending_approval = False
        super().save(*args, **kwargs)
    

    def get_absolute_url(self):
        return reverse_lazy('accounts:user_login')
    
    
    
 