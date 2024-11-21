from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import BooleanField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True

    def _create_user(
            self, username, first_login, email, phone, password, **extra_fields
    ):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError("The email field must be defined")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_login=first_login,
            email=email,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
            self, username, first_login, email, phone, password=None, **extra_fields
    ):
        """Create and save a regular User with the given email and password."""

        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        return self._create_user(
            username, first_login, email, password, phone, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # question: do we need to handle the phone as for a normal user?
        return self._create_user(
            username=email,
            first_login=False,
            email=email,
            password=password,
            phone="",
            **extra_fields,
        )


class CustomUser(AbstractUser, PermissionsMixin):
    CLIENT = 'client'
    ROLE_CHOICES =(
        ('admin', 'Admin'),
        (CLIENT, 'Client'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, default='client')
    # username = models.CharField(_("username"), unique=True, max_length=50)
    first_login = BooleanField()
    #nom = models.CharField(max_length=50, null=True, blank=True)
    #prenom = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now) 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Etiquette(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom}"

class Article(models.Model):
    choix_categorie = (("top-featured","Produits"),("best-seller","Médicaments"))
    choix_devise = (("dong","VND"),("dollar","$"))
    designation = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='images/')
    prix = models.FloatField(null=True, blank=True)
    quantite_en_stock = models.PositiveIntegerField(default=0)  # Ajout de la quantité en stock
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
    panier = models.JSONField(blank=True, null=True)
    total = models.FloatField(null=True, blank=True)
    
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

