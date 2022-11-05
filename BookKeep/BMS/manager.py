from django.db import models

class CustomManager(models.Manager):
    def all_records_filter(request):
        return super().filter(is_deleted='n')

    def records_by_id(request, bid):
        return super().filter(id = bid)

    def desc_by_price_pub(request, tbook_filter):
        return super().filter(is_deleted='n').filter(tbook = tbook_filter).order_by('-price')

    def asc_by_price_pub(request, tbook_filter):
        return super().filter(is_deleted='n').filter(tbook = tbook_filter).order_by('price')

    def desc_by_pages_pub(request, tbook_filter):
        return super().filter(is_deleted='n').filter(tbook = tbook_filter).order_by('-pages')

    def asc_by_pages_pub(request, tbook_filter):
        return super().filter(is_deleted='n').filter(tbook = tbook_filter).order_by('pages')

    def desc_by_price(request):
        return super().filter(is_deleted='n').order_by('-price')

    def asc_by_price(request):
        return super().filter(is_deleted='n').order_by('price')

    def desc_by_pages(request):
        return super().filter(is_deleted='n').order_by('-pages')

    def asc_by_pages(request):
        return super().filter(is_deleted='n').order_by('pages')

    def desc_by_author(request):
        return super().filter(is_deleted='n').order_by('-author')

    def asc_by_author(request):
        return super().filter(is_deleted='n').order_by('author')

    def duplicate_tbook(request):
        return super().values_list('tbook').distinct()

    def tbook_name(request, tbook_filter):
        return super().filter(is_deleted='n').filter(tbook = tbook_filter)

    def muulti_filter(request, tbook_filter):
        return super().filter(is_deleted='n').filter(tbook = tbook_filter).order_by('-price')
