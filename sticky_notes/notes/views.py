# notes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notes
from .forms import NotesForm

'''
This contians the views to be handled for the sticky notes app. Available views
include, view all notes, create notes, edit notes and delete notes.
'''


def notes_view(request):
    '''
    View to display all the created notes.

    :param request: HTTP request object.
    :return: Rendered template with all the notes created.
    '''

    notes = Notes.objects.all()

    # Context dictionary to pass data
    context = {
        "notes": notes,
        "page_title": "Created Notes.",
    }

    return render(request, "notes/notes_view.html", context)


def notes_detail(request, pk):
    '''
    View to display specific note details.

    :param request: HTTP request object.
    :param pk: Primary key of the note.
    :return: Rendered template with specific note details.
    '''

    note = get_object_or_404(Notes, pk=pk)
    return render(request, "notes/notes_detail.html", {"note": note})


def notes_create(request):
    '''
    View to create a new note.

    :param request: HTTP request object.
    :return: Rendered template for creating a new note.
    '''

    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect("notes_view")
    else:
        form = NotesForm()
        
    return render(request, "notes/notes_form.html", {"form": form})


def notes_update(request, pk):
    '''
    View to update an existing, selected note.

    :param request: HTTP request object.
    :param pk: Primary key of the selected note.
    :return: Rendered template for updateting the note.
    '''

    note = get_object_or_404(Notes, pk=pk)
    if request.method == "POST":
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect("notes_view")
    else:
        form = NotesForm(instance=note)

    return render(request, "notes/notes_form.html", {"form": form})


def notes_delete(request, pk):
    '''
    View to delete a specific note.

    :param request: HTTP request object.
    :param pk: Primary key for note to be deleted.
    :return: Redirect to the notes view after deletion.
    '''

    note = get_object_or_404(Notes, pk=pk)
    note.delete()
    return redirect("notes_view")

