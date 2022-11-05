from django.contrib import admin
from BMS.models import BookKeep
from django.contrib.admin import SimpleListFilter
# Register your models here.

class PageFilter(admin.SimpleListFilter):
    title = 'Page'
    parameter_name = 'Page'
    def lookups(self, request, model_admin):
        return (('htol','High to Low Pages'),('ltoh','Low to High Pages'))
    def queryset(self, request, queryset):
        if (self.value() == 'htol'):
            return queryset.order_by('-pages')
        elif (self.value() == 'ltoh'):
            return queryset.order_by('pages')

class PriceFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'Price'
    def lookups(self, request, model_admin):
        return (('htol','High to Low Pages'),('ltoh','Low to High Pages'))
    def queryset(self, request, queryset):
        if (self.value() == 'htol'):
            return queryset.order_by('-price')
        elif (self.value() == 'ltoh'):
            return queryset.order_by('price')

class AuthorFilter(admin.SimpleListFilter):
    title = 'Author'
    parameter_name = 'Author'
    def lookups(self, request, model_admin):
        return (('ltoh','A-Z'),('htol','Z-A'))
    def queryset(self, request, queryset):
        if (self.value() == 'htol'):
            return queryset.order_by('-author')
        elif (self.value() == 'ltoh'):
            return queryset.order_by('author')



class BookAdmin(admin.ModelAdmin):
        list_display = ['id', 'book', 'author', 'price', 'pages', 'tbook', 'is_deleted']
        list_filter = [PageFilter, PriceFilter, AuthorFilter]

admin.site.register(BookKeep, BookAdmin)
