from sqlite3 import DatabaseError

from django.db import transaction
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from Product.models import Product
from Product.serializers import ProductListingSerializer


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request, *args, **kwargs):
        """create an object"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    product = Product.create_product(
                        ArticleReference=serializer.validated_data['article_reference'],
                        ProductCategoryId=serializer.validated_data['id'],
                        Discount=serializer.validated_data['Discount'],
                        Quantity=serializer.validated_data['Quantity'],
                        Packaging=serializer.validated_data['Packaging'],
                        Designation=serializer.validated_data['Designation'],
                        UnitPriceHT=serializer.validated_data['UnitPriceHT'],
                        NetPU=serializer.validated_data['NetPU'],

                    )
            except DatabaseError:
                product = None

            headers = self.get_success_headers(serializer.data)

            return Response(
                ProductListingSerializer.data(product),
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                {"detail": "Erreur lors de la création de produit"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def retrieve(self, request, pk=None, *args, **kwargs):
        """get an object"""

        try:
            # Récupérer l'objet individuel de la base de données en utilisant l'identifiant fourni dans l'URL
            obj = self.get_object()

            # Sérialiser l'objet récupéré en utilisant le sérialiseur approprié pour la réponse détaillée
            serializer = self.get_serializer(obj)

            # Retourner la réponse avec le statut HTTP 200 OK et les données sérialisées
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            # Gérer le cas où l'objet n'est pas trouvé dans la base de données
            return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Gérer les exceptions génériques et renvoyer une réponse d'erreur avec le statut HTTP 500 Internal Server Error
            return Response({"detail": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        # Logique pour mettre à jour un objet complet
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    product= Product.update_product(
                        cls=self,
                        product_id=pk,
                        Discount=serializer.validated_data['Discount'],
                        Quantity=serializer.validated_data['Quantity'],
                        Packaging=serializer.validated_data['Packaging'],
                        Designation=serializer.validated_data['Designation'],
                        UnitPriceHT=serializer.validated_data['UnitPriceHT'],
                        NetPU=serializer.validated_data['NetPU'],


                    )
            except DatabaseError:
                product = None

            headers = self.get_success_headers(serializer.data)
            return Response(
                ProductListingSerializer(product).data,
                status=status.HTTP_200_OK,
                headers=headers
            )
        else:
            return Response(
                {"detail": "Error when creating product"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        """ Action pour supprimer un produit"""
        product = self.get_object()
        user_qs = request.infoUser.get('id')
        print(f"{user_qs}")
        product.delete_article(user=user_qs, product_id = pk)
        product = self.get_object()
        return Response(
            ProductListingSerializer(
                product,
                context={"request": request, "product": product}
            ).data,
            status=status.HTTP_200_OK
        )
