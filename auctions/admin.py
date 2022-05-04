from django.contrib import admin
from .models import User, Listing, Category, Bid, Comment


def user_id(obj):
    return obj.user_id.id

def user_name(obj):
    return obj.user_id.username

def listing_id(obj):
    return obj.listing_id.id

def listing_title(obj):
    return obj.listing_id.title


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "created")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", user_id, user_name, "time")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "approved")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", listing_id, listing_title, user_id, user_name, "amount", "available")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", listing_id, listing_title, user_id, user_name, "content")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
