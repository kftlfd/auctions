from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import User, Listing, Bid, Comment
from .apps import N_ON_PAGE


def user_page(request, user_id):
    user = User.objects.filter(pk=user_id)
    context = {
        'header': user[0] if user else None,
        'listings': Listing.objects.filter(user_id=user[0]).order_by('-id')} if user else None
    return render(request, "auctions/listings.html", context)


@login_required
def user_listings(request):
    context = {
        'header': 'My Listings',
        'listings': Listing.objects.filter(user_id=request.user).order_by('-id')}
    return render(request, "auctions/listings.html", context)


@login_required
def user_bids(request):
    # bids = Bid.objects.filter(user_id=request.user).distinct('listing_id')
    # DISTINCT is not supported by sqlite

    bids_all = Bid.objects.filter(user_id=request.user, available=True).order_by('-listing_id', '-amount')
    bids = []
    listings = set()

    for bid in bids_all:
        if bid.listing_id not in listings:
            listings.add(bid.listing_id)
            bids.append(bid)

    p = Paginator(bids, N_ON_PAGE)
    page = p.page(request.GET.get('page', 1))

    context = {
        'bids': bids}
    if page.has_other_pages():
        context['page'] = page
    return render(request, "auctions/user_bids.html", context)


@login_required
def user_watchlist(request):
    listings = request.user.watchlist.order_by('-id')
    p = Paginator(listings, N_ON_PAGE)
    page = p.page(request.GET.get('page', 1))

    context = {
        'header': 'Watchlist',
        'listings': listings}
    if page.has_other_pages():
        context['page'] = page
    return render(request, 'auctions/listings.html', context)
