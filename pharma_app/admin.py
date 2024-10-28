from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.html import mark_safe

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('designation', 'image_tag', 'prix_vente', 'etiquettes', 'active', 'create_date')
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150" />')
    
    def prix_vente(self, obj):
        if obj.devise=='dollar':
            return f"{obj.prix} $"
        elif obj.devise=='euro':
            return f"{obj.prix} Є"
    
    def etiquettes(self, obj):
        return list(obj.etiquette.all())

class CommandeAdmin(admin.ModelAdmin):
    list_display = ('user', 'pays', 'region', 'code_postal', 'adresse', 'create_date')
    
class Detail_commandeAdmin(admin.ModelAdmin):
    list_display = ('article', 'commande', 'qte')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'phone', 'role', 'date_joined')

class EtiquetteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'value', 'create_date')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('noms_complet', 'email', 'telephone', 'message')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Detail_commande, Detail_commandeAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Panier)
admin.site.register(Message, MessageAdmin)
admin.site.register(Etiquette, EtiquetteAdmin)


admin.sites.AdminSite.site_header = 'PHARMA-SERVICES'
admin.sites.AdminSite.site_title = 'PHARMA-SERVICES'
# admin.sites.AdminSite.index_title = 'pharma-SERVICES'