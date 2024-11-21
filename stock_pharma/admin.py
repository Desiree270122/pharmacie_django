from django.contrib import admin

from stock_pharma.models import Stock


# Register your models here.


class StockAdmin(admin.ModelAdmin):
    list_display = (
    'article', 'quantity',)

    # def image_tag(self, obj):
    #     return mark_safe(f'<img src="{obj.image.url}" width="150" />')
    #
    # def prix_vente(self, obj):
    #     if obj.devise == 'dong':
    #         return f"{obj.prix} VND"
    #
    # def etiquettes(self, obj):
    #     return list(obj.etiquette.all())

admin.site.register(Stock, StockAdmin)