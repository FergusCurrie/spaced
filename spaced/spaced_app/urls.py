from django.urls import path
from . import views 


urlpatterns = [
    path("", views.home, name="home_view_name"),
    path("review_cards", views.review_cards, name="review_cards_name"),
    path("add_cards", views.add_cards, name="add_cards_name")
]