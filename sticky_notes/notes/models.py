from django.db import models


class Notes(models.Model):
    '''
    Model representing the notes for the sticky notes app.

    Fields:
    - title: CharField for notes title max length of 255 characters.
    - content: TextField for the content of the notes.

    Methods:
    - __str__: Returns a string representation of the title of the note.
    '''

    title = models.CharField(max_length=255)
    content = models.TextField()


    def __str__(self):
        return self.title
