from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("gift_shop/", views.gift_shop, name="gift_shop"),
    path("notifications/", views.notifications, name="notifications"),
    path("event_search/<query>/", views.event_search, name="event_search"),
    path("add_event/", views.add_event, name="add_event")
]
