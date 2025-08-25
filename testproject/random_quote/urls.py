from django.urls import path
from .views import (
    QuoteCreateView,
    random_quote_view,
    like_quote,
    dislike_quote,
    Top10ByLikesView,
)

urlpatterns = [
    path("", random_quote_view, name="random_quote"),
    path("quotes/add/", QuoteCreateView.as_view(), name="quote_add"),
    path("quotes/<int:pk>/like/", like_quote, name="quote_like"),
    path("quotes/<int:pk>/dislike/", dislike_quote, name="quote_dislike"),
    path("quotes/top/", Top10ByLikesView.as_view(), name="quotes_top"),
]