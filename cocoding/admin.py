from django.contrib import admin
from account.models import User
from django_summernote.admin import SummernoteModelAdmin
from .models import Post


admin.site.register(User)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
admin.site.register(Post, PostAdmin)
