
from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea( attrs={
        'class':"w-full resize-none outline-none appearance-none border-bottom", 'aria-label':"Agrega un comentario...", 'placeholder':"Agrega un comentario..."  ,'autocomplete':"off", 'autocorrect':"off", 'style':"height: 36px;"
    } ))

    class Meta:
        model = Comment
        fields = ['body']