from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .serializers import *
from .models import *

# Create your views here.

def liste_articles(request):
    pk = request.GET.get('pk')
    etiq = request.GET.get('etiq')
    panier = []
    if request.user and not request.user.is_anonymous :
        panier = Panier.objects.filter(user=request.user)
    # print(panier)
    articles_etiq_value = []
    if pk:
        article = Article.objects.filter(pk=pk).first()
        articles = Article.objects.all()
        return render(request, "shop-detail.html", {"article":article, "articles":articles, "panier":panier})
    else:
        etiquettes = Etiquette.objects.all()
        if etiq:
            articles = Article.objects.filter(etiquette__in = [etiq])
        else:
            articles = Article.objects.all()
            for article in articles:
                etiquettes_value = [etiquette.value for etiquette in article.etiquette.all()]
                etiquettes_value_str = ' '.join(etiquettes_value)
                articles_etiq_value.append({"article":article, "etiquettes_value_str":etiquettes_value_str})
        # print("=======================", articles, articles_etiq_value)
        return render(request, "shop.html", {"articles":articles, "articles_etiq":articles_etiq_value, "panier":panier, "etiquettes":etiquettes, "etiq":etiq})
    
def template_accueil(request):
    articles = Article.objects.all()
    articles_etiq_value = []
    for article in articles:
        etiquettes_value = [etiquette.value for etiquette in article.etiquette.all()]
        etiquettes_value_str = ' '.join(etiquettes_value)
        articles_etiq_value.append({"article":article, "etiquettes_value_str":etiquettes_value_str})
    panier = []
    etiquettes = Etiquette.objects.all()
    if request.user and not request.user.is_anonymous :
        panier = Panier.objects.filter(user=request.user)
    return render(request, "index.html", {"articles":articles, "articles_etiq_value":articles_etiq_value, "panier":panier, "etiquettes":etiquettes})

def template_panier(request):
    panier = []
    articles = Article.objects.all()
    if request.user and not request.user.is_anonymous:
        panier = Panier.objects.filter(user=request.user)
    return render(request, "cart.html", {"panier":panier, "articles":articles})

def template_apropos(request):
    articles = Article.objects.all()
    panier = []
    if request.user and not request.user.is_anonymous:
        panier = Panier.objects.filter(user=request.user)
    return render(request, "about.html", {"articles":articles, "panier":panier})

def se_connecter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # try:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('accueil', message='success')
        else:
            messages.error(request, 'Echec de connexxion')
        # except Exception as e:
        #     messages.error(request, 'Erreur: Vérifiez vos identifiants')
    return redirect('login')


def log(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'login.html', {'messages': messages_to_display})



def creer_compte(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == request.POST.get('password1'):
            user = CustomUser(
                nom = request.POST.get('nom'),
                prenom = request.POST.get('prenom'),
                email = request.POST.get('email'),
                username = request.POST.get('email'),
                phone = request.POST.get('phone'),
                password = password
            )
            user.save()
            user.password = user.set_password(password)
            user.save()
            login(request, user)
            return redirect('accueil')
    return redirect('creer_compte')

@login_required(login_url='login')
def ajouter_au_panier(request, pk):
    status = 0
    if request.method == 'POST':
        if request.user and not request.user.is_anonymous:
            qte = int(request.POST.get('qte'))
            if request.POST.get('update'):
                panier = Panier.objects.filter(pk = pk).first()
                panier.qte = qte
                panier.save()
                status = 1
            else:
                article = Article.objects.filter(pk=pk).first()
                if article:
                    panier = Panier.objects.filter(user=request.user, article=article).first()
                    if panier:
                        panier.qte += qte
                        panier.save()
                    else:
                        Panier.objects.create(user=request.user, article=article, qte=qte)
                status = 1
                return JsonResponse({"status":status})
        return JsonResponse({"status":status})
    elif request.method == 'GET':
        panier = Panier.objects.filter(pk=pk).delete()
        status = 1
        return JsonResponse({"status":status})
    return JsonResponse({"status":status})

def count_panier(request):
    status = 0
    count = 0
    if request.method == 'GET': 
        if request.user and not request.user.is_anonymous :
            count = Panier.objects.filter(user=request.user).count()
            status = 1
            return JsonResponse({"count":count, "status":status})
    return JsonResponse({"status":status})

def liste_articles_panier(request):
    status = 0
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous :
            panier = Panier.objects.filter(user=request.user)
            serializer = PanierSerializer(panier, many=True)
            status = 1
            return JsonResponse({"panier":serializer.data, "status":status})
    return JsonResponse({"status":status})

def se_deconnecter(request):
    logout(request)
    return redirect('login')

def load_and_save_file(file_path):
    with open(file_path, 'rb') as f:
        file = File(f)
        article = Article()
        article.image.save('my_file.jpg', file)
        article.save()
        
def message_contact(request):
    status = 1
    Message.objects.create(
        noms_complet = request.POST.get('noms_complet'),
        telephone = request.POST.get('telephone'),
        email = request.POST.get('email'),
        message = request.POST.get('message'),
    )
    return JsonResponse({"status":status})

# views.py
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    paniers = []
    amount = 0 if not calculate_cart_total(request.user)  else calculate_cart_total(request.user)
    tva = amount*17/100
    gd_total = amount + tva
    if request.user and not request.user.is_anonymous :
        paniers = Panier.objects.filter(user=request.user)
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
         
        try:
            charge = stripe.Charge.create(
                amount=gd_total*100,
                currency='eur',
                description='Achat sur votre site e-commerce',
                source=token,
            )
            
            commande, created = Commande.objects.get_or_create(
                pays = request.POST.get('pays'),
                region = request.POST.get('region'),
                code_postal = request.POST.get('code_postal'),
                adresse = request.POST.get('adresse'),
                user = request.user
            )
            
            for panier in paniers: 
                detail_commande = Detail_commande.objects.create(
                    article = panier.article,
                    commande = commande,
                    qte = panier.qte
                )
                panier.delete()
            
        except stripe.error.CardError as e:
            # Gestion des erreurs liées à la carte
            return render(request, 'error.html', {'error': e.error.message})

        return render(request, 'success.html')
    STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY 
    return render(request, 'checkout1.html', {"STRIPE_PUBLIC_KEY":STRIPE_PUBLIC_KEY, "panier":paniers, "amount":amount, "tva":tva, "gd_total":gd_total, "montant":gd_total*100})

def calculate_cart_total(user):
    paniers = Panier.objects.filter(user=user)
    somme = 0
    for panier in paniers:
        somme += panier.article.prix * panier.qte
    return somme