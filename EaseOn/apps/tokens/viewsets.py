# -*- coding: utf-8 -*-
import django_filters
from core.utils import get_ticket_model, is_in_dev_mode
from core.viewsets import BaseViewSet
from django.apps import apps
from django.db.models import Q
from django.utils import timezone
from rest_framework import decorators, permissions, response,viewsets
from tokens import models, serializers
from tokens.commands import send_token_display_call_command
from tokens.permissions import isValidCaller

TICKET = apps.get_model(*get_ticket_model().split(".", 1))


class TokenNumberFilter(django_filters.CharFilter):
    empty_value = "EMPTY"

    def filter(self, qs, value):
        if value and value.isnumeric():
            d = {"token_number": int(value)}
            qs = qs.filter(**d)
        return qs


class TokenFilter(django_filters.FilterSet):
    """Token Filter"""

    organization = django_filters.CharFilter(field_name="organization__code")
    token_number = TokenNumberFilter(field_name="token_number")
    invite_sent_on_before = django_filters.DateTimeFilter(
        field_name="invite_sent_on", lookup_expr="lte"
    )
    invite_sent_on_after = django_filters.DateTimeFilter(
        field_name="invite_sent_on", lookup_expr="gte"
    )

    class Meta:
        model = models.Token
        fields = ["token_number", "location_code","first_name","last_name","email","contact_number","category"]


class TokenModelViewSet(BaseViewSet):
    serializer_class = serializers.TokenSerializer
    filter_class = TokenFilter
    permission_classes = [permissions.AllowAny]
    search_fields = ("token_number", "location_code", "email")

    def get_queryset(self):
        history_data = self.request.query_params.get('all', None)
        if history_data:
            return models.Token.objects.all()
        return models.Token.objects.all().created_between()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.AllowAny]
        if self.action in ["create", "list", "current_customers_at_counter"]:
            permission_classes = [permissions.AllowAny]
        if self.action in ["invite_customer_to_counter", "new_tokens"]:
            permission_classes = [isValidCaller]
        return [permission() for permission in permission_classes]

    @decorators.action(
        methods=["POST"],
        detail=True,
        url_name="invite_customer_to_counter",
        serializer_class=serializers.InviteCustomerSerializer,
    )
    def invite_customer_to_counter(self, request, pk):
        token = self.get_object()
        requesting_user = request.user
        if token.can_invite(requesting_user):
            context = {"request": request}
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            counter_number = serializer.validated_data["counter_number"]
            token.invited_by = request.user
            token.counter_number = counter_number
            token.is_present = True
            models.Token.objects.filter(
                counter_number=counter_number, location_code=token.location_code
            ).update(is_present=False)
            token.invite_sent_on = timezone.now()
            token.save()
            if not is_in_dev_mode():
                send_token_display_call_command(
                    **serializers.TokenSerializer(token, context=context).data
                )
        return response.Response(
            serializers.TokenSerializer(token, context=context).data
        )

    @decorators.action(
        methods=["POST"],
        detail=True,
        url_name="invite_customer_to_counter_via_sms",
        serializer_class=serializers.InviteCustomerSerializer,
    )
    def invite_customer_to_counter_via_sms(self, request, pk):
        token = self.get_object()
        requesting_user = request.user
        if token.can_invite(requesting_user):
            context = {"request": request}
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            counter_number = serializer.validated_data["counter_number"]
            token.invited_by = request.user
            token.counter_number = counter_number
            token.is_present = True
            models.Token.objects.filter(
                counter_number=counter_number, location_code=token.location_code
            ).update(is_present=False)
            token.invite_sent_on = timezone.now()
            token.save()
            if not is_in_dev_mode():
               token.send_invite_by_sms()
        return response.Response(
            serializers.TokenSerializer(token, context=context).data
        )

    @decorators.action(
        methods=["GET"], detail=True, url_name="resend_token_number_by_sms"
    )
    def resend_token_number_by_sms(self, request, pk):
        token = self.get_object()
        token.send_token_number_by_sms()
        context = {"request": request}
        token.save()
        return response.Response(
            serializers.TokenSerializer(token, context=context).data
        )

    @decorators.action(
        methods=["get"],
        detail=False,
        url_path="current_customers_at_counter/(?P<location_code>\w+)",
        url_name="current_customers_at_counter",
    )
    def current_customers_at_counter(self, request, location_code):
        tokens = self.get_queryset().filter(
            organization__code=location_code, is_present=True
        )
        context = {"request": request}
        return response.Response(
            serializers.TokenSerializer(tokens, many=True, context=context).data
        )

    @decorators.action(
        methods=["get"],
        detail=False,
        url_path="new_tokens/(?P<location_code>\w+)",
        url_name="new_tokens",
    )
    def new_tokens(self, request, location_code):
        tokens = (
            self.get_queryset()
            .filter(organization__code=location_code, invited_by__isnull=True)
            .exclude(token_number__isnull=True)
            .exclude(token_number__exact="")
        )
        context = {"request": request}
        new_tokens_data = serializers.TokenSerializer(
            tokens, many=True, context=context
        ).data
        if request.user.is_authenticated:
            current_token = (
                self.get_queryset()
                .filter(
                    organization__code=location_code,
                    invited_by=request.user,
                    is_present=True,
                )
                .exclude(token_number__isnull=True)
                .exclude(token_number__exact="")
            )
            current_token_data = serializers.TokenSerializer(
                current_token, many=True, context=context
            ).data
            for d in current_token_data:
                d["is_current"] = True
            new_tokens_data = new_tokens_data + current_token_data
        return response.Response(new_tokens_data)

    @decorators.action(
        methods=["get"],
        detail=False,
        url_path="fetch_token_info/(?P<organization_code>\w+)/(?P<token_number>\d+)",
        url_name="fetch_token_info",
    )
    def fetch_token_info(self, request, organization_code, token_number):
        token = (
            self.get_queryset()
            .filter(organization__code=organization_code, token_number=token_number)
            .first()
        )
        context = {"request": request}
        previous_tickets_counts = {
            "email": TICKET.objects.filter(customer__email=token.email).count(),
            "contact_number": TICKET.objects.filter(
                customer__contact_number=token.contact_number
            ).count(),
        }
        data = {"previous_tickets_counts": previous_tickets_counts}
        data.update(serializers.TokenSerializer(token, context=context).data)
        return response.Response(data)