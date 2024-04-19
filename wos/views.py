from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response

from wos.models import ProductCategory
from wos.serializers import ProductCategorySerializer


class CategoryProductViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class CategoryProductDetail(viewsets.ModelViewSet):
#
#     """
#     Get CategoryProduct by Id, Update or Delete CategoryProduct
#     """
#     model = ProductCategory
#     queryset = ProductCategory.objects.all()
#     serializer_class = ProductCategorySerializer
#
#     def get_object(self, pk):
#         try:
#             category = ProductCategory.objects.get(id=pk)
#             return category
#         except ProductCategory.DoesNotExist:
#             raise Http404
#
#     def put(self, request, pk, format = None):
#         category = self.get_object(pk)
#         serializer = ProductCategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)