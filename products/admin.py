from django.contrib import admin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import path, reverse
from django.utils.html import format_html
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin, DetailView

from products.models import *


class StockItemInline(admin.TabularInline):
    model = StockItem


@admin.register(RequestStock)
class RequestStockAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    inlines = [StockItemInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['title','quantity']
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "products.view_order"
    template_name = "map/map.html"
    model = Order

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'detail']
    inlines = [OrderItemInline]
    search_fields = ['user','created']

    def get_urls(self):
        return [
            path(
                "<pk>/detail",
                self.admin_site.admin_view(OrderDetailView.as_view()),
                name=f"products_order_detail",
            ),
            *super().get_urls(),
        ]

    def detail(self, obj: Order) -> str:
        url = reverse("admin:products_order_detail", args=[obj.pk])
        return format_html(f'<a href="{url}">📝 <strong>View Details</strong></a>')


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity']
#     search_fileds = ['product']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


    


