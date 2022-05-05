from django import forms
from .models import Category


def categories_all():
    return [ (c.id,c.name) for c in Category.objects.filter(approved=True).order_by('name') ]

def categories_edit():
    return [ (None, '-- None --'), ('+', '-- Suggest New --') ] + categories_all() + [ ('-', '-- Unevaluated suggestion --') ]

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

    title.widget.attrs.update({'class': 'form-control'})
    category.widget.attrs.update({'class': 'form-select form-select-sm'})
    status.widget.attrs.update({'class': 'form-select form-select-sm'})
    recency.widget.attrs.update({'class': 'form-select form-select-sm'})


class EditListingForm(forms.Form):
    title = forms.CharField(max_length=140, strip=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    img_url = forms.URLField(label='Image URL', required=False)
    category = forms.ChoiceField(choices=categories_edit, required=False)
    category_new = forms.CharField(required=False)

    title.widget.attrs.update({'class': 'form-control'})
    description.widget.attrs.update({'class': 'form-control', 'rows': 3})
    img_url.widget.attrs.update({'class': 'form-control'})
    category.widget.attrs.update({'class': 'form-select'})
    category_new.widget.attrs.update({'class': 'form-control'})


class AddListingForm(EditListingForm):
    starting_bid = forms.DecimalField(min_value=0, max_digits=11, decimal_places=2)

    starting_bid.widget.attrs.update({'class': 'form-control'})


class CommentForm(forms.Form):
    content = forms.CharField(label='Add new comment:', widget=forms.Textarea)

    content.widget.attrs.update({'class': 'form-control', 'rows': 3})


class BidForm(forms.Form):
    amount = forms.DecimalField(min_value=0, max_digits=11, decimal_places=2)

    amount.widget.attrs.update({'class': 'form-control'})
