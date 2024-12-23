from django import forms
from django.forms import widgets
from .models import Post
from django_ckeditor_5.widgets import CKEditor5Widget
from cloudinary.forms import CloudinaryFileField


class PostForm(forms.ModelForm):
    # image = forms.ImageField( required=False )
    image = CloudinaryFileField( required=False )

    class Meta:
        model = Post
        fields = ['body' , 'image']
        widgets= {
            'body': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              )
          }
        