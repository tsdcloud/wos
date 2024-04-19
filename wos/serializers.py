from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from wos.models import ProductCategory


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'wording', 'billing_type']

        def validate_libelle(self, value):
            """
            Méthode de validation pour le champ 'libelle'.
            Vérifie si le libellé n'est pas déjà utilisé par une autre catégorie produit.
            """
            # Vérifie s'il existe une autre catégorie produit avec le même libellé
            if ProductCategory.objects.filter(wording=value).exists():
                raise serializers.ValidationError("Ce libellé est déjà utilisé par une autre catégorie produit.")
            return value
