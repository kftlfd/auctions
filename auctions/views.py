from django.core.paginator import Paginator
from django.shortcuts import render

from .views_auth import *
from .views_listings import *
from .views_user import *

from .models import Listing, Category
from .forms import SearchForm
from .apps import N_ON_PAGE


def index(request):
    listings = Listing.objects.filter(active=True).order_by('-id')
    p = Paginator(listings, N_ON_PAGE)
    page = p.page(request.GET.get('page', 1))

    context = {
        'header': 'Active Listings',
        'listings': page.object_list}
    if page.has_other_pages():
        context['page'] = page
    return render(request, "auctions/listings.html", context)


def category_list(request):
    context = {
        'categories': Category.objects.filter(approved=True).order_by('name')}
    return render(request, "auctions/categories.html", context)


def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category=category, active=True).order_by('-id')
    p = Paginator(listings, N_ON_PAGE)
    page = p.page(request.GET.get('page', 1))

    context = {
        'header': category.name,
        'listings': listings}
    if page.has_other_pages():
        context['page'] = page
    return render(request, "auctions/listings.html", context)


def search(request):
    listings = Listing.objects.order_by('-id')
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
            listings = listings.order_by('time')

    p = Paginator(listings, N_ON_PAGE)
    page = p.page(request.GET.get('page', 1))

    context = {
        'form': SearchForm(form_vals),
        'listings': listings}
    if page.has_other_pages():
        context['page'] = page
    return render(request, "auctions/search.html", context)
