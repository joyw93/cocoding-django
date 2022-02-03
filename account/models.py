from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):    
   
   use_in_migrations = True    
   
   def create_user(self, username, email, nickname, password):        
       
       if not email:            
           raise ValueError('must have user email')
       if not password:            
           raise ValueError('must have user password')

       user = self.model(            
           email=self.normalize_email(email),
           username=username,
           nickname=nickname              
       )        
       user.set_password(password)        
       user.save(using=self._db)        
       return user

   def create_superuser(self, username, email, nickname, password):        
   
       user = self.create_user(            
           email = self.normalize_email(email),
           username=username,
           nickname=nickname,                       
           password=password        
       )
       user.is_admin = True
       user.is_superuser = True
       user.save(using=self._db)
       return user 


class User(AbstractBaseUser, PermissionsMixin):    
   
   objects = UserManager()
   username = models.CharField(max_length=50, unique=False)
   nickname = models.CharField(max_length=50, unique=True)
   email = models.EmailField(max_length=255, unique=True)
   is_active = models.BooleanField(default=True)
   is_admin = models.BooleanField(default=False)

   USERNAME_FIELD = 'email'    
   REQUIRED_FIELDS = ['username', 'nickname']

   def __str__(self):
       return self.email

   @property
   def is_staff(self):
       return self.is_admin