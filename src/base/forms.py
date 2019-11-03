from django import forms
from acctmang.models import User
from .models import Note


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {'username': 'Username',
                  'email': 'Email', 'password': 'Password'}


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'notetype', 'note', 'links', 'public')
    
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs['placeholder'] = 'To embed code in a General Note, add code in  <code></code>. '
