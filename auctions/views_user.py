from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Listing, Bid, Comment


@login_required
def user_listings(request):
    context = {
        'header': 'Your Listings',
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

    context = {
        'bids': bids}
    return render(request, "auctions/user_bids.html", context)


@login_required
def user_comments(request):
    context = {
        'comments': Comment.objects.filter(user_id=request.user).order_by('-id')}
    return render(request, "auctions/user_comments.html", context)


@login_required
def user_watchlist(request):
    context = {
        'header': 'Watchlist',
        'listings': request.user.watchlist.order_by('-id')}
    return render(request, 'auctions/listings.html', context)
