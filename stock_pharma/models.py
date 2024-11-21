from django.db import models

from pharma_app.models import Article


# Create your models here.

class Stock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, blank=True, null=True)
    # item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    # receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    # received_by = models.CharField(max_length=50, blank=True, null=True)
    # issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    # issued_by = models.CharField(max_length=50, blank=True, null=True)
    # issued_to = models.CharField(max_length=50, blank=True, null=True)
    # phone_number = models.CharField(max_length=50, blank=True, null=True)
    # created_by = models.CharField(max_length=50, blank=True, null=True)
    # re_order = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    date = models.DateTimeField(auto_now_add=False, auto_now=False)
    # export_to_csv = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='stock/static/images', null=True, blank=True)


