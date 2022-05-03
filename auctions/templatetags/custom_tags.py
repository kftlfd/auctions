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
    return f'${value:02,}'

@register.simple_tag
def listing_price(listing):
    top_bid = listing.current_bid.order_by('amount').reverse()
    price = top_bid[0].amount if top_bid else listing.starting_bid
    return usd(price)

@register.simple_tag
def listing_top_bidder(listing):
    top_bid = listing.current_bid.order_by('amount').reverse()
    return top_bid[0].user_id if top_bid else None

@register.simple_tag
def user_bid(user, listing):
    bid = listing.current_bid.filter(user_id=user).order_by('-amount')
    return usd(bid[0].amount) if bid else False


@register.simple_tag
def bid_count(listing):
    return listing.current_bid.count()
