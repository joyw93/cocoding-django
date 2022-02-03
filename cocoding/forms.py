from django import forms 
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags',)
        widgets = {
            'content': SummernoteWidget(),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        title_length = len(title)
        if title_length>50:
            raise forms.ValidationError('제목은 50자를 넘을 수 없습니다.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        content_length = len(content)
        if content_length>5000:
            raise forms.ValidationError('내용은 5,000자를 넘을 수 없습니다.')
        return content

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', [])
        if len(tags) > 4:
            raise forms.ValidationError('태그는 최대 4개까지 가능합니다.', code='invalid')
        return tags


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)