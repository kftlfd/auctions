from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("categories", views.category_list, name="category_list"),
    path("category/<int:category_id>", views.category_view, name="category_view"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("listing/add", views.listing_add, name="listing_add"),
    path("listing/<str:listing_id>", views.listing_view, name="listing_view"),
    path("listing/<str:listing_id>/edit", views.listing_edit, name="listing_edit"),
    path("listing/<str:listing_id>/bid", views.listing_bid, name="listing_bid"),
    path("listing/<str:listing_id>/bids", views.listing_bids, name="listing_bids"),
    path("listing/<str:listing_id>/comment", views.listing_comment, name="listing_comment"),
    path("listing/<str:listing_id>/watch", views.listing_watch, name="listing_watch"),
    path("listing/<str:listing_id>/status", views.listing_status, name="listing_status"),
    
    path("me/listings", views.user_listings, name="user_listings"),
    path("me/watchlist", views.user_watchlist, name="user_watchlist"),
    path("me/bids", views.user_bids, name="user_bids")
]
