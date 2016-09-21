from django.forms import modelformset_factory
from icelrc.models import Lyric
from django.shortcuts import render, redirect


def lyrics_admin(request):
    LyricFormSet = modelformset_factory(Lyric, fields=('title', 'artist', 'lyrics'))
    if request.method == 'POST':
        formset = LyricFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            redirect('/')
        else:
            raise
    else:
        formset = LyricFormSet()
    return render(request, 'lyrics_admin.html', {'formset': formset})