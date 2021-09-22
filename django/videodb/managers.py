from django.db import models

class ProductQuerySet(models.query.QuerySet):
  def get_by_category(self, category_name):
    return self.filter(category__name=category_name)

  def get_by_price(self):
    return self.order_by('price')


class ProductManager(models.Manager):
  def get_queryset(self):
    return ProductQuerySet(self.model, using=self._db)

  def get_by_category(self, category_name):
    return self.get_queryset().get_by_category(category_name)

  def get_by_price(self):
    return self.get_queryset().get_by_price()