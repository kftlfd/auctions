from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField('Listing')


class Listing(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.TextField()
    img_url = models.URLField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    starting_bid = models.DecimalField(max_digits=11, decimal_places=2)
    current_bid = models.ManyToManyField('Bid')
    active = models.BooleanField(default=True)
    closed = models.DateTimeField(null=True)

    def edit_form_data(self):
        return {
            "title": self.title,
            "description": self.description,
            "img_url": self.img_url,
            "category": self.category.id if self.category else None}


class Category(models.Model):
    name = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Bid(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    listing_id = models.ForeignKey('Listing', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    available = models.BooleanField(default=True)


class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    listing_id = models.ForeignKey('Listing', on_delete=models.CASCADE)
    content = models.TextField()
