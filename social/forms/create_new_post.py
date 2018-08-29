from django import forms
from social.models.posts import Posts

class CreateNewPost(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('owner','picture','caption')