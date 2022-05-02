from django.shortcuts import render

from .views_auth import *
from .views_listings import *
from .views_user import *

from .models import Listing, Category
from .forms import SearchForm


def index(request):
    context = {
        'listings': Listing.objects.filter(active=True)}
    return render(request, "auctions/index.html", context)


def search(request):
    listings = Listing.objects.all()
    form_vals = {}

    title = request.GET.get('title', None)
    if title:
        form_vals['title'] = title
        listings = listings.filter(title__contains=title)

    category = request.GET.get('category', None)
    if category:
        form_vals['category'] = category
        if category == 'none': category = None
        listings = listings.filter(category=category)

    status = request.GET.get('status', None)
    if status:
        form_vals['status'] = status
        listings = listings.filter(active=status)

    recency = request.GET.get('recency', None)
    if recency:
        form_vals['recency'] = recency
        if recency == 'old':
            listings = listings.order_by('id').reverse()

    context = {
        'form': SearchForm(form_vals),
        'listings': listings}
    return render(request, "auctions/search.html", context)


def category_list(request):
    context = {
        'categories': Category.objects.all()}
    return render(request, "auctions/category_list.html", context)


def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category=category)

    context = {
        'category': category,
        'listings': listings}
    return render(request, "auctions/category_view.html", context)
