from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from product.models import Product
from product import serializers


class CustomPageNumberPagination(PageNumberPagination):
    """ Personalización de la clase para paginación """

    def get_paginated_response(self, data):
        """ Agregar la cantidad de páginas disponibles """
        response = super().get_paginated_response(data)
        response.data['pageCount'] = self.page.paginator.num_pages
        return response


class ProductViewSet(viewsets.ModelViewSet):
    """ Manejar las productos en la base de datos """
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def _get_product_by_pk(self, pk):
        """ Obtener producto por su id """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return product

    def _get_product_by_slug(self, slug):
        """ Obtener producto por su slug """
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return product

    def get_permissions(self):
        """ Retirar la autenticación para los métodos GET o listados """
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'list_top_5':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        """ Método para crear un nuevo producto """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """ Método para listar todos los productos y con paginación """
        # limit = request.query_params.get('limit')
        # offset = request.query_params.get('offset')
        # products = Product.objects.order_by(
        #     '-created').all()[offset:offset+limit]
        # serializer = self.serializer_class(products, many=True)
        # return Response(serializer.data)
        queryset = Product.objects.order_by('-rating').all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ Método para obtener un producto en particular """
        product = self._get_product_by_slug(pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path="top")
    def list_top_5(self, request):
        """ Listar el top 5 de productos mejor calificados """
        products = Product.objects.order_by('-rating').order_by('-created')[:5]
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """ Método para actualizar un producto en particular """
        product = self._get_product_by_pk(pk)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """ Actualización parcial de los productos """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """ Método para eliminar un producto en particular """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        """ Obtener el serializador dependiendo del método """
        if self.action == 'retrieve':
            return self.serializer_class
        elif self.action == 'upload_image':
            return serializers.ProductImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ Crear nuevo producto """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Subir una imagen al producto """
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
