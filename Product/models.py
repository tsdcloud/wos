import json
from enum import Enum
from sqlite3 import DatabaseError

from django.db import models, transaction

import Product
from wos.models import ProductCategory


# Create your models here.

class Product(models.Model):
    class TypePackaging(Enum):
        ContainerizedProduct = 'produit conteneurisé'
        NoneContainerizedProduct = 'produit en vrac'

    ArticleReference = models.CharField(max_length=255)
    ProductCategoryId = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    Designation = models.CharField(max_length=255)
    UnitPriceHT = models.FloatField()
    Quantity = models.IntegerField()
    Packaging = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in TypePackaging])
    Discount = models.FloatField
    NetPU = models.IntegerField
    Amount = models.FloatField()

    @classmethod
    def create_product(cls, ArticleReference, ProductCategoryId, Designation, UnitPriceHT, Quantity, Packaging,
                       Discount, NetPU, Amount):
        """
        Crée une famille d'article.
        """

        product = Product()

        product.ArticleReference = ArticleReference
        product.ProductCategoryId = ProductCategoryId
        product.Designation = Designation
        product.UnitPriceHT = UnitPriceHT
        product.Quantity = Quantity
        product.Packaging = Packaging
        product.Discount = Discount
        product.NetPU = NetPU
        product.Amount = Amount

        try:
            with transaction.atomic():
                product._change_reason = json.dumps({"reason": "CREATE"})

                product.save()

            return product

        except DatabaseError as e:

            print(f"Error when creating the product : {e}")

            return None

    @classmethod
    def update_product(cls, product_id, ProductCategoryId, Designation, UnitPriceHT, Quantity, Packaging,
                       Discount, NetPU, Amount):
        """
        Met à jour les produits avec les données fournies.

        Parameters:
            data (dict): Dictionnaire contenant les champs à mettre à jour.
            :param Amount:
            :param NetPU:
            :param Discount:
            :param Packaging:
            :param Quantity:
            :param UnitPriceHT:
            :param Designation:
            :param ProductCategoryId:
            :param product_id:
        """
        product = ProductCategory.objects.get(id=product_id)
        product.ProductCategoryId = ProductCategoryId
        product.Designation = Designation
        product.UnitPriceHT = UnitPriceHT
        product.Quantity = Quantity
        product.Packaging = Packaging
        product.Discount = Discount
        product.NetPU = NetPU
        product.Amount = Amount
        try:
            with transaction.atomic():

                product._change_reason = json.dumps({"reason": "UPDATED"})

                product.save()

            return product

        except DatabaseError as e:

            print(f"Error while updating the product : {e}")

            return None

    @classmethod
    def delete_article(cls, product_id: str):
        """ delete product """

        try:
            with transaction.atomic():

                product_instance = cls.objects.get(
                    id=product_id)  # Remplacez ... par votre logique pour récupérer l'objet ExpenseSheet
                product_instance.is_active = False
                product_instance._change_reason = json.dumps({"reason": "DELETE"})
                product_instance.save()

            return product_instance

        except cls.DoesNotExist:

            return None

        except DatabaseError:

            return None

    @classmethod
    def restore_product(cls, user: str, product_id: str):
        """ Restore expense_sheet """

        try:
            with transaction.atomic():
                product_instance = cls.objects.get(
                    id=product_id)  # Remplacez ... par votre logique pour récupérer l'objet ExpenseSheet
                product_instance.is_active = True
                product_instance._change_reason = json.dumps({"reason": "RESTORE"})
                product_instance.save()

            return product_instance

        except cls.DoesNotExist:
            return None

        except DatabaseError:
            return None

    def __str__(self):
        return self.ArticleReference
