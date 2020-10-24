# -*- coding: utf-8 -*-
import django_filters
from core.viewsets import BaseViewSet
from django.db.models import Q
from tokens import models, serializers
from rest_framework import decorators, permissions, response
from django.utils import timezone
from tokens.permissions import isValidCaller


class TokenNumberFilter(django_filters.CharFilter):
    empty_value = 'EMPTY'

    def filter(self, qs, value):
        if value:
            d = {'token_number': int(value)}
            qs = qs.filter(**d)
        return qs


class TokenFilter(django_filters.FilterSet):
    """Token Filter"""

    organization = django_filters.CharFilter(field_name='organization__code')
    token_number = TokenNumberFilter(field_name='token_number')

    class Meta:
        model = models.Token
        fields = ['token_number', 'location_code']


class TokenModelViewSet(BaseViewSet):
    serializer_class = serializers.TokenSerializer
    filter_class = TokenFilter
    permission_classes = [permissions.AllowAny]
    search_fields = ('token_number', 'location_code', 'email')

    def get_queryset(self):
        return models.Token.objects.all().created_between()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.AllowAny]
        print(self.action)
        if self.action in ['create', 'list', 'current_customers_at_counter']:
            permission_classes = [permissions.AllowAny]
        if self.action in ['invite_customer_to_counter', 'new_tokens']:
            permission_classes = [isValidCaller]
        return [permission() for permission in permission_classes]

    @decorators.action(
        methods=['POST'],
        detail=True,
        url_name='invite_customer_to_counter',
        serializer_class=serializers.InviteCustomerSerilizer,
    )
    def invite_customer_to_counter(self, request, pk):
        token = self.get_object()
        requesting_user = request.user
        if token.can_invite(requesting_user):
            context = {'request': request}
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            counter_number = serializer.validated_data['counter_number']
            token.invited_by = request.user
            token.counter_number = counter_number
            token.is_present = True
            models.Token.objects.filter(
                counter_number=counter_number,
                location_code=token.location_code,
            ).update(is_present=False)
            token.invite_sent_on = timezone.now()
            token.save()
        return response.Response(
            serializers.TokenSerializer(token, context=context).data
        )

    @decorators.action(
        methods=['GET'], detail=True, url_name='resend_token_number_by_sms'
    )
    def resend_token_number_by_sms(self, request, pk):
        token = self.get_object()
        token.send_token_number_by_sms()
        context = {'request': request}
        token.save()
        return response.Response(
            serializers.TokenSerializer(token, context=context).data
        )

    @decorators.action(
        methods=['get'],
        detail=False,
        url_path='current_customers_at_counter/(?P<location_code>\w+)',
        url_name='current_customers_at_counter',
    )
    def current_customers_at_counter(self, request, location_code):
        tokens = models.Token.objects.filter(
            organization__code=location_code, is_present=True
        )
        context = {'request': request}
        return response.Response(
            serializers.TokenSerializer(
                tokens, many=True, context=context
            ).data
        )

    @decorators.action(
        methods=['get'],
        detail=False,
        url_path='new_tokens/(?P<location_code>\w+)',
        url_name='new_tokens',
    )
    def new_tokens(self, request, location_code):
        tokens = (
            models.Token.objects.filter(
                organization__code=location_code, invited_by__isnull=True
            )
            .exclude(token_number__isnull=True)
            .exclude(token_number__exact='')
        )
        context = {'request': request}
        new_tokens_data = serializers.TokenSerializer(
            tokens, many=True, context=context
        ).data
        current_token = (
            models.Token.objects.filter(
                organization__code=location_code,
                invited_by=request.user,
                is_present=True,
            )
            .exclude(token_number__isnull=True)
            .exclude(token_number__exact='')
        )
        current_token_data = serializers.TokenSerializer(
            current_token, many=True, context=context
        ).data
        for d in current_token_data:
            d['is_current'] = True
        new_tokens_data = new_tokens_data + current_token_data
        return response.Response(new_tokens_data)
