from django.db.models import Q
from django.shortcuts import render, redirect
from django import forms
from .models import Events, Users


class SearchForm(forms.Form):
    search_content = forms.CharField(label="search_content")


class RegisterEvent(forms.Form):
    event_name = forms.CharField(label="event_name")
    event_date = forms.CharField(label="event_date")
    event_description = forms.CharField(label="event_description")


class LogIn(forms.Form):
    email = forms.CharField(label="email")
    password = forms.CharField(label="password")


class SignUp(forms.Form):
    name = forms.CharField(label="name")
    email = forms.CharField(label="email")
    address = forms.CharField(label="address")
    password = forms.CharField(label="password")


class Profile(forms.Form):
    name = forms.CharField(label="name")
    address = forms.CharField(label="address")


def searchable(func):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST" and (form := SearchForm(request.POST)).is_valid():
            return redirect("event_search", query=form.cleaned_data["search_content"])
        return func(request, *args, **kwargs)

    return wrapper


@searchable
def index(request):
    return render(request, "index.html", {"logged_in": request.session.get("logged_in", False)})


def profile(request):
    if request.method == "POST":
        if (form := Profile(request.POST)).is_valid():
            if "save" in request.POST:
                user = Users.objects.filter(email=request.session["email"])[0]
                user.name = form.cleaned_data["name"]
                user.address = form.cleaned_data["address"]
                user.save()
                return redirect("index")
            if "log_out" in request.POST:
                request.session["logged_in"] = False
                return redirect("index")
    return render(
        request,
        "profile.html",
        {
            "logged_in": request.session.get("logged_in", False),
            "name": request.session.get("name"),
            "email": request.session.get("email"),
            "address": request.session.get("address"),
        }
    )


@searchable
def event_search(request, query):
    if request.method == "POST":
        if "register" in request.POST:
            event = Events.objects.filter(name__exact=request.POST["event_name"])[0]
            if request.session["email"] not in event.drivers:
                event.drivers.append(request.session["email"])
            event.save()
        if "buddies2" in request.POST:
            drivers = Events.objects.filter(name__exact=request.POST["event_name"])[0].drivers
            users = [Users.objects.filter(email__exact=driver)[0] for driver in drivers]
            return render(request, "event_search.html", {
                "events": Events.objects.filter(
                    Q(name__contains=query) | Q(description__contains=query) | Q(date__contains=query)
                ),
                "logged_in": request.session.get("logged_in", False),
                "drivers": users,
                "show_buddies": True
            })
        if "accept" in request.POST:
            driver_name = request.POST["driver_name"]
            user = Users.objects.filter(name__exact=driver_name)[0]
            user.notifications.append({"name": request.session["name"], "address": request.session["address"]})
            user.save()

    return render(request, "event_search.html", {
        "events": Events.objects.filter(
            Q(name__contains=query) | Q(description__contains=query) | Q(date__contains=query)
        ),
        "logged_in": request.session.get("logged_in", False),
        "drivers": [],
        "show_buddies": False
    })


@searchable
def gift_shop(request):
    return render(request, "gift_shop.html", {"logged_in": request.session.get("logged_in", False)})


@searchable
def notifications(request):
    return render(
        request,
        "notifications.html",
        {
            "notifications": Users.objects.filter(email__exact=request.session["email"])[0].notifications,
            "logged_in": request.session.get("logged_in", False)
        }
    )


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
    return render(request, "add_event.html", {"logged_in": request.session.get("logged_in", False)})


@searchable
def log_in(request):
    if request.method == "POST":
        if (form := LogIn(request.POST)).is_valid() and len(matched_users := Users.objects.filter(
                Q(email__exact=form.cleaned_data["email"]) | Q(password__exact=form.cleaned_data["password"])
        )) == 1:
            request.session["logged_in"] = True
            request.session["name"] = matched_users[0].name
            request.session["email"] = matched_users[0].email
            request.session["address"] = matched_users[0].address
            return redirect("index")
    return render(request, "log_in.html", {"logged_in": request.session.get("logged_in", False)})


@searchable
def sign_up(request):
    if request.method == "POST":
        if (form := SignUp(request.POST)).is_valid():
            Users(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
                password=form.cleaned_data["password"],
                notifications=[]
            ).save()
            request.session["logged_in"] = True
            request.session["name"] = form.cleaned_data["name"]
            request.session["address"] = form.cleaned_data["address"]
            request.session["email"] = form.cleaned_data["email"]
            return redirect("index")
    return render(request, "sign_up.html", {"logged_in": request.session.get("logged_in", False)})
