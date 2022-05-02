from django import forms
from .models import Category


def categories_all():
    return [ (c.id,c.name) for c in Category.objects.all() ]

def categories_edit():
    return [ (None, '-None-'), ('+', '-New-') ] + categories_all()

def categories_search():
    return [ (None, 'Any'), ('none', 'None') ] + categories_all()

def status_search():
    return [ (None, 'All'), (True, 'Active'), (False, 'Closed') ]

def recency_search():
    return [ ('new', 'New'), ('old', 'Old') ]


class SearchForm(forms.Form):
    title = forms.CharField(max_length=140, strip=True, required=False)
    category = forms.ChoiceField(choices=categories_search, required=False)
    status = forms.ChoiceField(choices=status_search, required=False)
    recency = forms.ChoiceField(choices=recency_search, required=False)


class EditListingForm(forms.Form):
    title = forms.CharField(max_length=140, strip=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    img_url = forms.URLField(label='Image URL', required=False)
    category = forms.ChoiceField(choices=categories_edit, required=False)
    category_new = forms.CharField(required=False)


class AddListingForm(EditListingForm):
    starting_bid = forms.DecimalField(min_value=0, max_digits=11, decimal_places=2)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class BidForm(forms.Form):
    amount = forms.DecimalField(min_value=0, max_digits=11, decimal_places=2)
