"""
URL configuration for service_pharma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from setuptools.extern import names

from .views import *
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', se_connecter, name='login'),
    path('acceuil', template_accueil, name='accueil'),
    path('contact', TemplateView.as_view(template_name='contact-us.html'), name='contact'),
    path('services', template_apropos, name='services'),
    # path('shop', TemplateView.as_view(template_name='shop.html'), name='shop'),
    path('shop', liste_articles, name='shop'),
    path('panier', template_panier, name='panier'),
    path('compte', TemplateView.as_view(template_name='checkout.html'), name='compte'),
    path('compte', TemplateView.as_view(template_name='checkout.html'), name='compte'),

    #path('signin', TemplateView.as_view(template_name='creer_compte.html'), name='signin'),
    path('signin/', creer_compte, name='signin'),
    #path('se_connecter', se_connecter, name='se_connecter'),
    path('logout', se_deconnecter, name='logout'),
    path('add_to_cart/<int:pk>', ajouter_au_panier, name='add_to_cart'),
    path('delete_from_cart/<int:pk>', delete_from_cart, name='delete_from_cart'),
    path('count_panier', count_panier, name='count_panier'),
    path('articles_panier', liste_articles_panier, name='articles_panier'),
    path('message_contact', message_contact, name='message_contact'),
    path('checkout', checkout, name='checkout'),
    path('confpaye/<int:commande_id>', confirmation_order, name='confpaye'),
    # path('order_complete', order_complete, name='order_complete'),
    path('process_payment', process_payment, name='process_payment'),
    path('order_complete/<int:commande_id>', order_complete, name='order_complete'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



