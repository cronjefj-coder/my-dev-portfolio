# notes/urls.py
from django.urls import path
from .views import (
    notes_view,
    notes_detail,
    notes_create,
    notes_update,
    notes_delete,
)
'''
This represents the url patterns for the sticky notes app.
'''

urlpatterns = [
    path("", notes_view, name="notes_view"),
    path("note/<int:pk>/", notes_detail, name="notes_detail"),
    path("note/new/", notes_create, name="notes_create"),
    path("note/<int:pk>/edit/", notes_update, name="notes_update"),
    path("note/<int:pk>/delete", notes_delete, name="notes_delete"),
]
    
