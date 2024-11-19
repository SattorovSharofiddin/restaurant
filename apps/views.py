import httpx
import random
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.models import Product, Customer
from apps.serializers import ProductModelSerializer, UserRegisterSerializer, SendVerificationEmailSerializer, \
    VerifyEmailSerializer, SendPasswordResetLinkSerializer, PasswordResetSerializer, CheckPasswordResetTokenSerializer
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


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
