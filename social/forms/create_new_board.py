from django import forms
from social.models import Board


class CreateNewBoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('owner', 'name')