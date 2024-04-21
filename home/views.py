from django.db.models import Q
from django.shortcuts import render, redirect
from django import forms
from .models import Events


class SearchForm(forms.Form):
    search_content = forms.CharField(label="search_content")


class RegisterEvent(forms.Form):
    event_name = forms.CharField(label="event_name")
    event_date = forms.CharField(label="event_date")
    event_description = forms.CharField(label="event_description")


def searchable(func):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST" and (form := SearchForm(request.POST)).is_valid():
            return redirect("event_search", query=form.cleaned_data["search_content"])
        return func(request, *args, **kwargs)

    return wrapper


@searchable
def index(request):
    return render(request, "index.html")


def profile(request):
    return render(request, "profile.html")


@searchable
def event_search(request, query):
    return render(request, "event_search.html", {
        "events": Events.objects.filter(
            Q(name__contains=query) | Q(description__contains=query) | Q(date__contains=query)
        )
    })


@searchable
def gift_shop(request):
    return render(request, "gift_shop.html")


@searchable
def notifications(request):
    return render(request, "notifications.html")


@searchable
def add_event(request):
    if request.method == "POST":
        if (form := RegisterEvent(request.POST)).is_valid():
            Events(
                name=form.cleaned_data["event_name"],
                date=form.cleaned_data["event_date"],
                description=form.cleaned_data["event_description"],
                drivers=[]
            ).save()
        return render(request, "add_event.html", {"event_added": True})
    return render(request, "add_event.html")
