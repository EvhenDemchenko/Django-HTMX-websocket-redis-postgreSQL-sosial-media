from django.contrib.auth.models import User
from django import forms
from z_users.models import Profile
from cloudinary.forms import CloudinaryFileField


class ProfileForm(forms.ModelForm):
    displayname = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Display Name', 'class':'form-control mb-2  mt-2  p-2'}))

    info = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':3, 'placeholder': 'Info', 'class':'form-control mb-2  mt-2  p-2'}))

    # image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'form-control mb-2  mt-2  p-2 '}))
    image = CloudinaryFileField()
    class Meta:
        model = Profile
        fields = ['displayname' , 'image' , 'info' ]


class EmailForm(forms.ModelForm):
    email = forms.EmailField( widget=forms.EmailInput(attrs={ 'name':'email', 'id':'id_email', 'placeholder': 'Email', 'class':'form-control mb-2  mt-2  p-2'}))

    class Meta:
        model = User
        fields = ['email']