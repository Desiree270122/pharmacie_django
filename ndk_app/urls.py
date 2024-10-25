"""
URL configuration for ndk_services project.

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
from .views import *
from django.views.generic import TemplateView
	
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', template_accueil, name='accueil'),
    path('contact', TemplateView.as_view(template_name='contact-us.html'), name='contact'),
    path('services', template_apropos, name='services'),
    # path('shop', TemplateView.as_view(template_name='shop.html'), name='shop'),
    path('shop', liste_articles, name='shop'),
    path('panier', template_panier, name='panier'),
    path('compte', TemplateView.as_view(template_name='checkout.html'), name='compte'),
    path('compte', TemplateView.as_view(template_name='checkout.html'), name='compte'),
    path('login', log, name='login'),
    path('signin', TemplateView.as_view(template_name='creer_compte.html'), name='signin'),
    path('creer_compte', creer_compte, name='creer_compte'),
    path('se_connecter', se_connecter, name='se_connecter'),
    path('logout', se_deconnecter, name='logout'),
    path('add_to_cart/<pk>', ajouter_au_panier, name='add_to_cart'),
    path('count_panier', count_panier, name='count_panier'),
    path('articles_panier', liste_articles_panier, name='articles_panier'),
    path('message_contact', message_contact, name='message_contact'),
    path('checkout', checkout, name='checkout'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
