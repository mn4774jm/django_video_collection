from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower


def home(request):
    app_name = 'Exercise Videos'
    return render(request, 'video_collection/home.html', {'app_name':app_name})
# Create your views here.


def add(request):
    if request.method == 'POST':    # adding new video
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()   # creates new Video object and saves
                return redirect('video_list')
            # todo redirect to list of videos
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video')
        messages.warning(request, 'Check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})


def video_list(request):

    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))

    else:
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})

