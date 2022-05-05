from django.apps import AppConfig


class AuctionsConfig(AppConfig):
    name = 'auctions'
    default_auto_field = 'django.db.models.AutoField'


# number of listings on one page
N_ON_PAGE = 5
