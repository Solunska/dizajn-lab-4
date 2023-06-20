from django import forms
from .models import Post, UserProfile
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Post
        exclude = ("author", "created_at",)
        labels = {
            "title": "Title of post",
            "content": "Content",
            "files": "Add Files",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter Title For The Post"}),
            "content": forms.Textarea(attrs={"placeholder": "Write some content for the post"}),
            "files": forms.FileInput(attrs={"placeholder": "Select files"})
        }


class BlockedUsersForm(forms.ModelForm):
    blocked_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['blocked_users']

