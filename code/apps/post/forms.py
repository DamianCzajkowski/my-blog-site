from django import forms
from apps.post.models import Tag, Category, Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    banner_image = forms.ImageField()
    thumb_image = forms.ImageField()
    is_public = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"style": "width: unset; height: unset"})
    )
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image",
            "banner_image",
            "thumb_image",
            "is_public",
            "tags",
            "category",
        )
