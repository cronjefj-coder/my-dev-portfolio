# notes/forms.py
from django import forms
from .models import Notes


class NotesForm(forms.ModelForm):
    '''
    Form for creating and updating notes.

    Fields:
    - title: CharField for the note title.
    - content: TextField for the content of the note.

    Meta class:
    - Defines the model (Notes) to use and the fields to include in the form.

    :param forms.ModelFrom: Django's ModelForm class.
    '''


    class Meta:
        model = Notes
        fields = ["title", "content"]
