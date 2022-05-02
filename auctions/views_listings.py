from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Listing, Bid, Comment, Category
from .forms import EditListingForm, AddListingForm, CommentForm, BidForm


def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing_id=listing)
    
    current_bid = listing.current_bid.order_by('amount').reverse()
    if current_bid:
        current_bid = current_bid[0]
        bid = current_bid.amount
    else:
        bid = listing.starting_bid

    form_bid = BidForm({'amount': bid})
    
    form_comment = CommentForm()

    watching = False
    if request.user.is_authenticated:
        if request.user.watchlist.filter(id=listing.id):
            watching = True
    
    context = {
        'form_bid': form_bid,
        'form_comment': form_comment,
        'listing': listing,
        'current_bid': current_bid,
        'comments': comments,
        'watching': watching}
    return render(request, "auctions/listing_view.html", context)


@login_required
def listing_add(request):
    form = AddListingForm()

    if request.method == 'POST':
        form = AddListingForm(request.POST)
        
        if form.is_valid():

            new_listing = Listing(
                user_id=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                img_url=form.cleaned_data['img_url'],
                starting_bid=form.cleaned_data['starting_bid'])
            if form.cleaned_data['category'] == '+' and form.cleaned_data['category_new']:
                category_new = Category(name=form.cleaned_data['category_new'])
                category_new.save()
                new_listing.category = category_new
            elif form.cleaned_data['category'] not in ['', '+']:
                category = Category.objects.get(pk=form.cleaned_data['category'])
                new_listing.category = category
            else:
                new_listing.category = None
            new_listing.save()

            messages.add_message(request, messages.SUCCESS, 'Listing added')
            return redirect(reverse('user_listings'))
        
        else:
            messages.add_message(request, messages.ERROR, 'Invalid form')

    context = {
        'form': form}
    return render(request, "auctions/listing_add.html", context)


@login_required
def listing_edit(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)
    if not listing or listing.user_id != request.user:
        return redirect(reverse('user_listings'))
    form = EditListingForm(listing.edit_form_data())

    if request.method == 'POST':
        form = EditListingForm(request.POST)

        if request.POST.get('delete'):
            listing.delete()
            messages.add_message(request, messages.SUCCESS, 'Listing deleted')
            return redirect(reverse('user_listings'))

        elif form.is_valid():
            listing.title = form.cleaned_data['title']
            listing.description = form.cleaned_data['description']
            listing.img_url = form.cleaned_data['img_url']
            if form.cleaned_data['category'] == '+' and form.cleaned_data['category_new']:
                category_new = Category(name=form.cleaned_data['category_new'])
                category_new.save()
                listing.category = category_new
            elif form.cleaned_data['category'] not in ['+', '']:
                category = Category.objects.get(pk=form.cleaned_data['category'])
                listing.category = category
            elif form.cleaned_data['category'] == '':
                listing.category = None
            listing.save()
            messages.add_message(request, messages.SUCCESS, 'Listing modified')
            return redirect(reverse('listing_view', kwargs={'listing_id': listing_id}))

        else:
            messages.add_message(request, messages.ERROR, 'Invalid form')

    context = {
        'listing': listing,
        'form': form}
    return render(request, "auctions/listing_edit.html", context)


@login_required
def listing_comment(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    if not listing:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = Comment(
                user_id=request.user,
                listing_id=listing,
                content=form.cleaned_data['content'])
            new_comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
        
        else:
            messages.add_message(request, messages.ERROR, 'Comment fail')
    
    return redirect('listing_view', listing_id=listing_id)
    

@login_required
def listing_bid(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)
    if not listing:
        return redirect('index')

    if request.method == 'POST':

        if request.POST.get('remove', None):
            bids = Bid.objects.filter(user_id=request.user, listing_id=listing)
            for bid in bids:
                bid.available = False
                bid.save()
            revoke = listing.current_bid.filter(user_id=request.user)
            listing.current_bid.remove(*revoke)
            listing.save()
            messages.add_message(request, messages.SUCCESS, 'Bid removed')
            return redirect('listing_view', listing_id=listing_id)

        form = BidForm(request.POST)
        
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Bid fail')
            return redirect('listing_view', listing_id=listing_id)

        amount = form.cleaned_data['amount']
        
        valid_bid = True
        if amount <= listing.starting_bid:
            valid_bid = False

        curr = listing.current_bid.order_by('amount').reverse()
        if valid_bid and curr and amount <= curr[0].amount:
            valid_bid = False

        if valid_bid:
            new_bid = Bid(
                user_id=request.user,
                listing_id=listing,
                amount=amount)
            new_bid.save()
            listing.current_bid.add(new_bid)
            listing.save()
            messages.add_message(request, messages.SUCCESS, 'Bid added')
        else:
            messages.add_message(request, messages.ERROR, 'Bid needs to be higher than the current one')

    return redirect('listing_view', listing_id=listing_id)


@login_required
def listing_bids(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    if not listing or listing.user_id != request.user:
        return redirect('listing_view', listing_id=listing_id)

    bids = Bid.objects.filter(listing_id=listing).order_by('id').reverse()
    
    context = {
        'listing': listing,
        'bids': bids}
    return render(request, "auctions/listing_bids.html", context)


@login_required
def listing_watch(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    if not listing:
        return redirect('index')
    
    if request.method == 'POST':
        
        if request.POST.get('add'):
            request.user.watchlist.add(listing)
            request.user.save()
            messages.add_message(request, messages.SUCCESS, 'Added to Watchlist')

        elif request.POST.get('remove'):
            request.user.watchlist.remove(listing)
            request.user.save()
            messages.add_message(request, messages.SUCCESS, 'Removed from Watchlist')

    return redirect('listing_view', listing_id=listing_id)


@login_required
def listing_status(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)
    if not listing or listing.user_id != request.user:
        return redirect('listing_view', listing_id=listing_id)

    if request.method == 'POST':
        form = EditListingForm(request.POST)

        if request.POST.get('close'):
            listing.active = False
            listing.save()
            messages.add_message(request, messages.SUCCESS, 'Listing closed')

        elif request.POST.get('open'):
            listing.active = True
            listing.save()
            messages.add_message(request, messages.SUCCESS, 'Listing opened')

    context = {
        'listing': listing}
    return redirect('listing_view', listing_id=listing_id)
