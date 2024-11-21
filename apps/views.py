import os
import random

import httpx
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.models import Product, Customer, Order, Category
from apps.serializers import ProductModelSerializer, UserRegisterSerializer, SendVerificationEmailSerializer, \
    VerifyEmailSerializer, SendPasswordResetLinkSerializer, PasswordResetSerializer, CheckPasswordResetTokenSerializer, \
    OrderModelSerializer, CategoryModelSerializer
from apps.tasks import send_email


class RegisterView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = UserRegisterSerializer
    parser_classes = FormParser, MultiPartParser


class SendVerificationAPIView(GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = SendVerificationEmailSerializer
    parser_classes = FormParser, MultiPartParser

    def post(self, request):  # noqa
        email = request.data.get('email')
        try:
            user = get_object_or_404(Customer, email=email)
            if user.is_active:
                return Response({'message': "Email already verified."}, status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        send_email.delay(
            user.full_name, user.email, user.pk, random.randint(100_000, 999_999)
        )
        return Response({'message': 'Email sent successfully'})


class CheckVerifyEmailView(GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = VerifyEmailSerializer
    parser_classes = FormParser,

    def post(self, request):  # noqa
        try:
            obj = self.serializer_class(data=request.data)
            obj.is_valid(raise_exception=True)
            obj.save()
        except ValidationError:
            return Response({'message': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)


class PasswordResetView(GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = VerifyEmailSerializer
    parser_classes = FormParser,

    @action(['POST'], detail=False, serializer_class=SendPasswordResetLinkSerializer)
    # TODO: add url to all actions in this class with - instead of _
    def send_email(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.save()
        validated_data['host'] = request.get_host()
        send_email.delay(**validated_data)
        return Response({'message': 'reset password link sent successfully'})

    @action(['PATCH'], detail=False, serializer_class=PasswordResetSerializer)
    def reset_password(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.save()
        return Response({'message': 'password reset successfully'})

    @action(['POST'], detail=False, serializer_class=CheckPasswordResetTokenSerializer)
    def check_token(self, request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        return Response({'message': 'token is valid'})


class QRCodeView(GenericAPIView):
    serializer_class = None

    def get(self, request):
        url = 'http://localhost:8000/api/products/'
        if not url:
            return Response({'message': 'URL is required'}, status.HTTP_400_BAD_REQUEST)
        qr_code = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}'
        return Response({'qr_code': qr_code})


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class OrderModelViewSet(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False)
    def checkout(self, request):
        customer = request.user
        products = request.data.get('products')
        if not products:
            return Response(
                {'error': 'Products are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product_instances = Product.objects.filter(id__in=products)
            if product_instances.count() != len(products):
                return Response(
                    {'error': 'One or more products do not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Product.DoesNotExist:
            return Response(
                {'error': 'Invalid product IDs'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(customer_id=customer)
        order.products.set(product_instances)

        # bot_token = f"{os.getenv('BOT_TOKEN')}"
        bot_token = "7243224143:AAEDkoA3rwfpZycRd2Croyh2R9xzd_Oiyt8"

        # chat_id = f"{os.getenv('CHAT_ID')}"
        chat_id = "-4520930282"

        message = (
            f"New Order Created!\n"
            f"Customer: {customer.username}\n"
            f"Order ID: {order.id}\n"
            f"Products: {[product.name for product in product_instances]}\n"
            f"Total Price: {sum([product.price for product in product_instances])}\n"
            f"Created At: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        try:
            with httpx.Client() as client:
                response = client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": message}
                )
                response.raise_for_status()
        except httpx.RequestError as exc:
            return Response(
                {'error': 'Failed to send notification to bot', 'details': str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def get_orders(self, request):
        customer = request.user
        orders = Order.objects.filter(customer_id=customer)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class CategoryApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
