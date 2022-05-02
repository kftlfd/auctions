from django import template

register = template.Library()

@register.simple_tag
def watchlist_count(user):
    return user.watchlist.count()

@register.simple_tag
def search_category(link, category_id):
    return link + '?category=' + str(category_id)

@register.filter
def usd(value):
    return f'${value}'

@register.simple_tag
def listing_bid(listing):
    current_bid = listing.current_bid.order_by('amount').reverse()
    if current_bid:
        current_bid = current_bid[0]
        bid = current_bid.amount
    else:
        bid = listing.starting_bid
    return usd(bid)

@register.simple_tag
def user_bid(user, listing):
    bid = listing.current_bid.filter(user_id=user).order_by('-amount')
    return usd(bid[0].amount) if bid else None
