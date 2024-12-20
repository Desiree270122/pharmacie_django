from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, OuterRef, Exists
from django.template.loader import render_to_string
from django.urls import reverse

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from stock_pharma.models import Stock
from .forms import RegisterForm, LoginForm
from .serializers import *
from .models import *
from .utils import generate_username

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Panier, Commande, Detail_commande
# Create your views here.

def liste_articles(request):
    print(" ")
    pk = request.GET.get('pk')
    etiq = request.GET.get('etiq')
    panier = []
    if request.user and not request.user.is_anonymous :
        panier = Panier.objects.filter(user=request.user)
    # print(panier)
    articles_etiq_value = []
    if pk:
        article = Article.objects.filter(pk=pk).first()
        stocks_with_quantity = Stock.objects.filter(
            article=OuterRef('pk'),
            quantity__gt=0
        )

        # Requête principale pour obtenir les articles
        articles = Article.objects.annotate(
            has_positive_stock=Exists(stocks_with_quantity)
        ).filter(has_positive_stock=True)
        context = {
            "segment": "shop",
            "article": article,
            "articles": articles,
            "panier": panier
        }
        return render(request, "shop-detail.html", context)
    else:
        etiquettes = Etiquette.objects.all()
        if etiq:
            articles = Article.objects.filter(etiquette__in = [etiq])
        else:
            print(" ")
            stocks_with_quantity = Stock.objects.filter(
                article=OuterRef('pk'),
                quantity__gt=0
            )

            # Requête principale pour obtenir les articles
            articles = Article.objects.annotate(
                has_positive_stock=Exists(stocks_with_quantity)
            ).filter(has_positive_stock=True)
            for article in articles:
                etiquettes_value = [etiquette.value for etiquette in article.etiquette.all()]
                etiquettes_value_str = ' '.join(etiquettes_value)
                articles_etiq_value.append({"article":article, "etiquettes_value_str":etiquettes_value_str})
        # print("=======================", articles, articles_etiq_value)
        context = {
            "segment": "shop",
            "articles": articles,
            "articles_etiq": articles_etiq_value,
            "panier": panier,
            "etiquettes": etiquettes,
            "etiq": etiq
        }
        return render(request, "shop.html", context)
    
def template_accueil(request):
    # stocks = Stock.objects.filter(quantity__gt=0)
    # print(stocks)
    # articles = Article.objects.all()
    # print(articles.count())
    # for stock in stocks:
    #     articles = Article.objects.get(pk=stock.article.id)
    # Sous-requête pour vérifier l'existence d'un stock positif pour un article
    stocks_with_quantity = Stock.objects.filter(
        article=OuterRef('pk'),
        quantity__gt=0
    )

    # Requête principale pour obtenir les articles
    articles = Article.objects.annotate(
        has_positive_stock=Exists(stocks_with_quantity)
    ).filter(has_positive_stock=True)

    # Utilisation des résultats
    # for article in articles:
    #     print(article.name)
    print(articles.count())

    # print(articles)
    articles_etiq_value = []
    for article in articles:
        etiquettes_value = [etiquette.value for etiquette in article.etiquette.all()]
        etiquettes_value_str = ' '.join(etiquettes_value)
        articles_etiq_value.append({"article":article, "etiquettes_value_str":etiquettes_value_str})
    panier = []
    etiquettes = Etiquette.objects.all()
    if request.user and not request.user.is_anonymous :
        panier = Panier.objects.filter(user=request.user)

    context = {
        "articles":articles,
        "articles_etiq_value":articles_etiq_value,
        "panier":panier,
        "etiquettes":etiquettes,
        "segment": "accueil",
    }
    return render(request, "index.html", context)

def template_panier(request):
    panier = []
    stocks_with_quantity = Stock.objects.filter(
        article=OuterRef('pk'),
        quantity__gt=0
    )

    # Requête principale pour obtenir les articles
    articles = Article.objects.annotate(
        has_positive_stock=Exists(stocks_with_quantity)
    ).filter(has_positive_stock=True)
    if request.user and not request.user.is_anonymous:
        panier = Panier.objects.filter(user=request.user)

    context = {
        'segment': 'panier',
        "panier": panier,
        "articles": articles
    }
    return render(request, "cart.html", context)

def template_apropos(request):
    articles = Article.objects.all()
    panier = []
    if request.user and not request.user.is_anonymous:
        panier = Panier.objects.filter(user=request.user)
    return render(request, "about.html", {"articles":articles, "panier":panier})

def se_connecter(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('accueil')
        else:
            messages.error(request, 'Echec de connexxion')
    else:
        print(form.errors)
    """if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # try:
            user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('accueil')
        else:
            messages.error(request, 'Echec de connexxion')
        # except Exception as e:
        #     messages.error(request, 'Erreur: Vérifiez vos identifiants')
    """
    context = {
        "form": form,
    }
    return render(request, 'login.html', context)


def log(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'login.html', {'messages': messages_to_display})



def creer_compte(request):
    print('je suis ici')
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = user.CLIENT
            email = request.POST.get('email')
            user.username = generate_username(email)
            user.is_active = True
            user.first_login = True
            user.save()

            login(request, user)

            # Send verification mail. Handle any exception that could occur.
            try:
                verify_email(user, request)

                return redirect('login')
            except Exception as e:
                print(e)
                # msg = settings.ERROR_COULD_NOT_SEND_VERIF_EMAIL
                # messages.error(request, msg)

            return redirect('accueil')

            # password = request.POST.get('password')

            """if password == request.POST.get('password1'):
                user = CustomUser(
                    nom = request.POST.get('nom'),
                    prenom = request.POST.get('prenom'),
                    email = email,
                    username = username,
                    phone = request.POST.get('phone'),
                    password = password
                )
                
                user.password = user.set_password(password)
                user.save()
                login(request, user)

            """
        else:
            print(form.errors)

    else:
        form = RegisterForm()

    context = {
        "form": form
    }
    return render(request, 'creer_compte.html', context)


def verify_email(user, request):
    """Send verification mail"""
    # from apps.authentication.views.utils import get_site_scheme_and_domain


    from_email = settings.DEFAULT_FROM_EMAIL
    mail_subject = "Account Registration Confirmation"
    to_email = user.email

    msge = render_to_string(
      "email/acc_active_email.txt",
      {
        "username": user.username,
      },
    )

    msge_html = render_to_string(
      "email/acc_active_email.html",
      {
        "username": user.username,
      },
    )
    send_mail(
      mail_subject,
      msge,
      from_email,
      [to_email, ],
      fail_silently=False,
      html_message=msge_html,
    )


# @login_required(login_url='login')
def ajouter_au_panier(request, pk):
    if request.user and not request.user.is_anonymous:
        referer = request.META.get('HTTP_REFERER')

        qte =1
        article = Article.objects.get(id=pk)

        try:
            panier = Panier.objects.get(user=request.user, article=article)
            print(" mis a jour ")
        # if request.POST.get('update'):
        #     panier = Panier.objects.filter(pk=pk).first()
            panier.qte += qte
            panier.save()
            status = 1
            if referer:
                return redirect(referer)
            else:
                return JsonResponse({"status": status})
        except:
            print("creation du panier ")
            # article = Article.objects.filter(pk=pk).first()
            # if article:
            # panier = Panier.objects.filter(user=request.user, article=article).first()
            Panier.objects.create(user=request.user, article=article, qte=qte)
            # if panier:
            #     panier.qte += qte
            #     panier.save()
            # else:
            #     Panier.objects.create(user=request.user, article=article, qte=qte)
            status = 1
            if referer:
                return redirect(referer)
            else:
                return JsonResponse({"status": status})
    else:
        print("login requred")
        # return JsonResponse({"status": "Failed"})
        return redirect('login')

    # status = 0
    # article = Article.objects.get(id=pk)
    # panier = Panier.objects.get(user=request.user, article=article)
    # if panier:
    #     # panier.qte += 1
    #     # pani
    #     pass
    # if request.method == 'POST':
    #     if request.user and not request.user.is_anonymous:
    #         qte = int(request.POST.get('qte'))
    #         if request.POST.get('update'):
    #             panier = Panier.objects.filter(pk = pk).first()
    #             panier.qte = qte
    #             panier.save()
    #             status = 1
    #         else:
    #             article = Article.objects.filter(pk=pk).first()
    #             if article:
    #                 panier = Panier.objects.filter(user=request.user, article=article).first()
    #                 if panier:
    #                     panier.qte += qte
    #                     panier.save()
    #                 else:
    #                     Panier.objects.create(user=request.user, article=article, qte=qte)
    #             status = 1
    #             referer = request.META.get('HTTP_REFERER')
    #             if referer:
    #                 return redirect(referer)
    #             else:
    #                  return JsonResponse({"status":status})
    #
    #     return JsonResponse({"status":status})
    # elif request.method == 'GET':
    #     panier = Panier.objects.filter(pk=pk).delete()
    #     status = 1
    #     if referer:
    #         return redirect(referer)
    #     else:
    #         return JsonResponse({"status": status})
    # return JsonResponse({"status":status})



def delete_from_cart(request, pk):
    if request.user and not request.user.is_anonymous:
        # qte = int(request.POST.get('qte'))
        print(pk)
        qte =1
        article = Article.objects.get(id=pk)

        try:

            panier = Panier.objects.filter(user=request.user, article=article)
            print(" suppression ")
        # if request.POST.get('update'):
        #     if panier.length >
            panier = panier.first()
            if panier.qte > 1:
                panier.qte -= qte
                panier.save()
                status = 1
            else:
                panier.delete()
                panier.qte = 0
            status = 1

            return JsonResponse({"status": status})
        except Exception as e:
            print("erreur lors de la suppression  ")
            print(e)
            # article = Article.objects.filter(pk=pk).first()
            # if article:
            # panier = Panier.objects.filter(user=request.user, article=article).first()
            # Panier.objects.create(user=request.user, article=article, qte=qte)
            # if panier:
            #     panier.qte += qte
            #     panier.save()
            # else:
            #     Panier.objects.create(user=request.user, article=article, qte=qte)
            status = 0

            return JsonResponse({"status": status})
    else:
        print("login requred")
        # return JsonResponse({"status": "Failed"})
        return redirect('login')

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
#    if
    print("je suis venu ici")
    paniers = []
    total_product = 0
    amount = 0 if not calculate_cart_total(request.user) else calculate_cart_total(request.user)
    print("2")
    tva = amount*17/100
    gd_total = amount + tva
    if request.user and not request.user.is_anonymous:
        paniers = Panier.objects.filter(user=request.user)
        if paniers.count() == 0:
            print("panier vide")

            return redirect('accueil')
        total_product = paniers.count()

    if request.method == 'POST':
        # token = request.POST.get('stripeToken')

        try:
            print("je suis venu ici")
            """charge = stripe.Charge.create(
                amount=gd_total*100,
                currency='vnd',
                description='Achat sur votre site e-commerce',
                source=token,
            )"""

            # Calculer le total du panier
            # total = sum(item.article.prix * item.qte for item in paniers)

            commande = Commande()
            commande.user = request.user
            commande.pays = request.POST.get('pays')
            commande.region = request.POST.get('region')
            commande.code_postal = request.POST.get('code_zip')
            commande.adresse = request.POST.get('adresse')
            commande.total = gd_total
            commande.sub_total = amount
            commande.tva = tva
            # commande.panier = paniers
            commande.save()
            
            # commande = Commande.objects.get_or_create(
            #     pays =
            #     region =
            #     code_postal = ,
            #     adresse = ,
            #     user = request.user
            # )

            nbr_article = 0
            
            for panier in paniers: 
                detail_commande = Detail_commande.objects.create(
                    article = panier.article,
                    commande = commande,
                    qte = panier.qte
                )
                nbr_article+=1
                # panier.delete()

            commande.nbr_article = nbr_article
            # commande.panier = paniers
            commande.save()

            request.session['commande_id'] = commande.id

            return redirect(
                reverse(
                    "confpaye",
                    kwargs={
                        "commande_id": commande.id
                    }
                )
            )

            # return redirect("confpaye")
            
        except Exception as e:
            print('erreur lors du traitement')
            print(e)
            # Gestion des erreurs liées à la carte
            #return render(request, 'error.html', {'error': e.message})
    STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
    context = {
        'segment': 'panier',
        "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY,
        "panier": paniers,
        "amount": amount,
        "tva": tva,
        "gd_total": gd_total,
        "montant": gd_total*100,
        "total_product": total_product,
    }
    return render(request, 'checkout1.html', context)

def calculate_cart_total(user):
    paniers = Panier.objects.filter(user=user)
    somme = 0
    for panier in paniers:
        print(panier)
        somme += panier.article.prix * panier.qte
    return somme

def process_payment(request):
    context={

    }
    return render(request,"order_complete.html",context)



class PaymentView(View):
    def get(self, request):
        # Logique de paiement ici (intégration Stripe, PayPal, etc.)
        # Simuler un paiement réussi
        # Si le paiement est réussi
        messages.success(request, "Paiement effectué avec succès.")
        return redirect('success_page')




# def confirmation_order(request):
#     if not request.user.is_authenticated:
#         # Rediriger l'utilisateur vers la page de connexion ou autre
#         return redirect('login')
#
#     paniers = Panier.objects.filter(user=request.user)  # Obtenez le panier pour l'utilisateur connecté
#     total = sum(item.article.prix * item.qte for item in paniers)  # Calculez le total
#
#     # Si vous avez des données supplémentaires à passer, ajoutez-les ici
#     context = {
#         'panier': paniers,
#         'total': total,
#         'stripe_public_key': 'VotreCléPubliqueStripe',
#         'user_info': request.user
#     }
#     return render(request, 'confpaye.html', context)


def confirmation_order(request, commande_id):

    print('ehbfznfbhezusy')
    if not request.user.is_authenticated:
        # Rediriger l'utilisateur vers la page de connexion ou autre
        return redirect('login')

    # Récupérer le panier de l'utilisateur
    paniers = Panier.objects.filter(user=request.user)

    commande = Commande.objects.get(pk=commande_id)

    if not paniers:
        # Rediriger si le panier est vide
        messages.error(request, "Votre panier est vide.")
        return redirect('template_panier')

    # Calculer le total du panier
    total = sum(item.article.prix * item.qte for item in paniers)

    # commande = Commande()
    # commande.user = request.user
    # commande.pays =
    # commande.region =
    # commande.code_postal =
    # commande.adresse =

    # Créer la commande
    # , created = Commande.objects.get_or_create(
    #     user=request.user,
    # )

    # Créer les détails de la commande s'ils n'existent pas déjà
    if request.method == 'POST':
        for panier in paniers:
            # Créer le détail de la commande
            detail_commande = Detail_commande.objects.create(
                commande=commande,
                article=panier.article,
                qte=panier.qte
            )

            # Mettre à jour le stock de l'article
            # if Stock.objects.get(article=panier.article).exists():
            stock = Stock.objects.get(article=panier.article)
            if stock.quantity >= panier.qte:
                stock.quantity -= panier.qte
                stock.save()
            else:
                # Annuler la commande si la quantité demandée est supérieure au stock disponible
                messages.error(request, f"Le produit {panier.article.nom} n'a pas assez de stock disponible.")
            # return redirect('panier')

            # Supprimer les articles du panier après la création de la commande
        paniers.delete()

        print('Je suis venu ici maintenant')

        return redirect(
            reverse(
                "order_complete",
                kwargs={
                    "commande_id": commande.id
                }
            )
        )


    # Récupérer les détails de la commande
    details_commande = Detail_commande.objects.filter(commande=commande)

    # Passer les données à la vue
    context = {
        'commande': commande,
        'details_commande': details_commande,
        'total': total,
        'stripe_public_key': 'VotreCléPubliqueStripe',
        'user_info': request.user,
        "panier": paniers
    }

    return render(request, 'confpaye.html', context)


def order_complete(request, commande_id):
    if not request.user.is_authenticated:
        # Rediriger l'utilisateur vers la page de connexion ou autre
        return redirect('login')

    total = calculate_cart_total(request.user)

    commande = Commande.objects.get(pk=commande_id)

    if request.method == 'POST':
        to_email = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        mail_subject = "Order completed"
        msge = "Order completed"

        try:
            send_mail(
                mail_subject,
                msge,
                from_email,
                [to_email, ],
                fail_silently=False,
            )
        except Exception as e:
            print(e)
        return redirect('accueil')

    # Récupérer le panier de l'utilisateur
    # paniers = Panier.objects.filter(user=request.user)

    detail_commande = Detail_commande.objects.filter(commande=commande)

    panier = detail_commande

    print(detail_commande)

    #
    # if not paniers:
    #     # Rediriger si le panier est vide
    #     messages.error(request, "Votre panier est vide.")
    #     return redirect('panier')



    # for panier in paniers:
    #     # Créer le détail de la commande
    #     detail_commande = Detail_commande.objects.create(
    #         commande=commande,
    #         article=panier.article,
    #         qte=panier.qte
    #     )
    #
    #     # Mettre à jour le stock de l'article
    #     stock = Stock.objects.get(article=panier.article)
    #     if stock.quantity >= panier.qte:
    #         stock.quantity -= panier.qte
    #         stock.save()
    #     else:
    #         # Annuler la commande si la quantité demandée est supérieure au stock disponible
    #         messages.error(request, f"Le produit {panier.article.nom} n'a pas assez de stock disponible.")
    #         return redirect('template_panier')
    #
    # # Supprimer les articles du panier après la création de la commande
    # paniers.delete()

    context = {
        'total': total,
        'commande': commande,
        "panier": panier,
    }
    return render(request, 'order_complete.html', context)
