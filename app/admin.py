from django.contrib import admin
from app.models import TourCategory, Tour, Cart, Order, New


def make_paid(modeladmin, request, queryset):
    queryset.update(status='Paid')


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_paid]
    list_display = ('id', 'last_name', 'date', 'total_price', 'status')


make_paid.short_description = 'Make orders paid'

admin.site.register(TourCategory)
admin.site.register(Tour)
admin.site.register(Cart)
admin.site.register(New)
admin.site.register(Order, OrderAdmin)
