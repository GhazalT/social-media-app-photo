from django import forms
from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ("title", "image", "caption")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "field-input",
                "placeholder": "Give your photo a title",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "field-input field-input--file",
                "data-image-input": "",
            }),
            "caption": forms.Textarea(attrs={
                "class": "field-input",
                "placeholder": "Add a short caption",
                "rows": 4,
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={
                "class": "comment-input",
                "placeholder": "Add a comment...",
                "rows": 1,
                "data-autogrow": "",
            }),
        }
