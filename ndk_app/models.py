from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError(_("The username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES =(
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, default='client')
    username = models.CharField(_("username"), unique=True, max_length=50)
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now) 

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
      verbose_name = "user"

    def __str__(self):
        return f"{self.username}"

class Etiquette(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom}"

class Article(models.Model):
    choix_categorie = (("top-featured","Alimentaire"),("best-seller","Médicamenteux"))
    choix_devise = (("euro","Є"),("dollar","$"))
    designation = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='images/')
    prix = models.FloatField(null=True, blank=True)
    devise = models.CharField(choices=choix_devise, max_length=255, null=True, blank=True)
    etiquette = models.ManyToManyField(Etiquette)
    lien_paiement = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.designation}"
    
class Commande(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    pays = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    code_postal = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
class Detail_commande(models.Model):
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    commande = models.ForeignKey(Commande, null=True, blank=True, on_delete=models.SET_NULL)
    qte = models.IntegerField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.article}"
    
class Panier(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    qte = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.article}"
    
class Message(models.Model):
    noms_complet = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.article}"
    