# -*- coding: utf-8 -*-
import json
import logging
import django_filters
from core import serializers
from gsx.core import GSXRequest
from core.permissions import SuperUserOrReadOnly
from django.contrib.auth import get_user_model
from django.utils import timezone
from organizations.models import Organization , OrganizationRights
from organizations.serializers import (
    OrganizationRightsSerializer,
    OrganizationSerializer,
)
from rest_framework import decorators, response, status


from .base import BaseViewSet
from core.filters import FullNameFilter


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    is_admin = django_filters.BooleanFilter()
    full_name = FullNameFilter(field_name=None)
    date_joined_before = django_filters.DateTimeFilter(
        field_name='date_joined', lookup_expr='lte'
    )
    date_joined_after = django_filters.DateTimeFilter(
        field_name='date_joined', lookup_expr='gte'
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'city',
            'is_admin',
            'contact_number',
            'gsx_technician_id',
            'gsx_user_name',
        ]


class UserViewSet(BaseViewSet):
    serializer_class = serializers.UserSerializer
    retrieve_serializer_class = serializers.UserSerializer
    permission_classes = (SuperUserOrReadOnly,)
    search_fields = ('first_name', 'email', 'contact_number', 'last_name')
    filter_class = UserFilter

    @decorators.action(
        methods=['get'], detail=True, url_name='rights',
    )
    def rights(self, request, pk=None):
        from lists.models import get_list_choices
        user = self.get_object()
        #GET Organization Based Or Rights
        right_type = self.request.query_params.get('right_type', None)
        rights = []
        if user.is_superuser or user.is_privileged:
            organizations = Organization.objects.all()
            for organization in organizations:
                organization_right = OrganizationRights.get_allow_all_object(request,organization,right_type)
                rights.append(organization_right)
        else:
            organizations = user.managed_locations.filter(is_deleted=False)
            for organization in organizations:
                organization_right = OrganizationRights.get_allow_all_object(request,organization,right_type)
                rights.append(organization_right)
            for location in user.locations.filter(is_deleted=False):
                location_right = OrganizationRightsSerializer(
                    location, context={'request': request}
                ).data
                if right_type is not None and right_type.strip("'") in get_list_choices('REPORT_TYPES'):
                    location_right[right_type] = False
                rights.append(location_right)
        return response.Response({'results': rights})

    @decorators.action(
        methods=['get'], detail=True, url_name='dashboard',
    )
    def dashboard(self, request, pk=None):
        user = self.get_object()
        dashboard_data = {}
        count = [
            {
                'order': 1,
                'heading': 'Tickets Created Today',
                'value': user.created_ticket.all().created_between().count(),
            },
            {
                'order': 2,
                'heading': 'Tickets Closed Today',
                'value': user.closed_tickets.all().closed_between().count(),
            },
            {
                'order': 3,
                'heading': 'Vouchers Created Today',
                'value': user.created_voucher.all().created_between().count(),
            },
            {
                'order': 4,
                'heading': 'Due Tickets For Today',
                'value': user.subscribed_tickets.all().due_between().count(),
            },
        ]
        dashboard_data['counts'] = count
        return response.Response({'result': dashboard_data})

    @decorators.action(
        methods=['post'],
        detail=True,
        serializer_class=serializers.PasswordChangeSerializer,
        url_name='change_password',
    )
    def change_password(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return response.Response({'detail': 'New password has been saved.'})

    @decorators.action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        user = self.get_object()
        user.toggle_activation(True)
        user.save()
        logging.info(
            'user {} has been activated '.format(
                user.email
            )
        )
        context = {'request': request}
        return response.Response(
            self.serializer_class(user, context=context).data
        )
    
    @decorators.action(methods=['get'], detail=False)
    def me(self, request):
        user = request.user
        context = {'request': request}
        return response.Response(
            self.serializer_class(user, context=context).data
        )
    
    @decorators.action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.toggle_activation(False)
        user.save()
        logging.info(
            'user {} has been deactivated '.format(
                user.email
            )
        )
        return response.Response(
            self.serializer_class(user, context={'request': request}).data
        )

    @decorators.action(methods=['get'], detail=False)
    def check_gsx_connectivity(self, request):
        req = GSXRequest('authenticate', 'check',None,None,None)
        return response.Response(req.get(), status=status.HTTP_200_OK)

    def _get_gsx_token(self, request):
        gsx_token = None
        query_params = request.query_params
        if 'gsx_token' in query_params:
            gsx_token = query_params.get('gsx_token')
        return gsx_token

    @decorators.action(methods=['post', 'get'], detail=True)
    def refresh_gsx_token(self, request, pk=None):
        user = self.get_object()
        gsx_token = self._get_gsx_token(request)
        result = user.refresh_gsx_token(gsx_token, user.gsx_ship_to)
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=True)
    def logout(self, request, pk=None):
        user = self.get_object()
        gsx_token = self._get_gsx_token(request, user)
        req = GSXRequest(
            'authenticate', 'end-session', user.gsx_user_name, gsx_token
        )
        result = req.post(userAppleId=user.gsx_user_name, authToken=gsx_token)
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=False)
    def technician_lookup(self, request):
        gsx_token = self._get_gsx_token(request, request.user)
        user = request.user
        req = GSXRequest('technician', 'lookup', user.gsx_user_name, gsx_token)
        data = [{'condition': 'equals', 'field': 'firstName', 'value': 'GSX'}]
        result = req.post(payload=data)
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=False)
    def serializer_lookup(self, request):
        gsx_token = self._get_gsx_token(request, request.user)
        user = request.user
        req = GSXRequest(
            'repair/product',
            'serializer/lookup',
            user.gsx_user_name,
            gsx_token,
        )
        data = {}
        result = req.post(payload=data)
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=True)
    def document_download(self, request, pk=None):
        user = self.get_object()
        gsx_token = self._get_gsx_token(request, user)
        req = GSXRequest(
            'document-download', None, user.gsx_user_name, gsx_token
        )

        result = req.get()
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(
        methods=['post'],
        detail=True,
        serializer_class=serializers.GSXPayloadSerializer,
    )
    def send_GSX_request(self, request, pk=None):
        user = self.get_object()
        gsx_token = self._get_gsx_token(request, user)
        # /attachment/upload-access
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = request.data.get('payload')
        method = request.data.get('method')
        resource_name = request.data.get('resource_name')
        req = GSXRequest(resource_name, None, user.gsx_user_name, gsx_token)
        result = None
        if method == 'GET':
            result = req.get(**json.loads(payload))
        else:
            result = req.post(payload=json.loads(payload))
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=True)
    def document_upload_access(self, request, pk=None):
        user = self.get_object()
        gsx_token = self._get_gsx_token(request, user)
        # /attachment/upload-access
        req = GSXRequest(
            'attachment', 'upload-access', user.gsx_user_name, gsx_token
        )
        data = {
            'attachments': [{'sizeInBytes': 10, 'name': 'WarrantyClaim.pdf'}],
            'device': {'id': 'FCGT24E5HFM2'},
        }
        result = req.post(payload=data)
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=True)
    def content_article_lookup(self, request, pk=None):
        user = self.get_object()
        gsx_token = self._get_gsx_token(request, user)
        req = GSXRequest(
            'content', 'article/lookup', user.gsx_user_name, gsx_token
        )
        data = {'articleType': 'PRODUCT_HELP'}
        result = req.post(payload=data)
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(methods=['post', 'get'], detail=False)
    def get_article_content(self, request):
        query_params = request.query_params
        article_id = query_params.get('article_id')
        gsx_token = self._get_gsx_token(request, request.user)
        a = 'article?articleId={0}'.format(article_id)
        user = request.user
        req = GSXRequest('content', a, user.gsx_user_name, gsx_token)
        result = req.get()
        return response.Response(result, status=status.HTTP_200_OK)

    @decorators.action(
        methods=['POST'],
        detail=True,
        serializer_class=serializers.ChangeUserRoleSerializer,
    )
    def change_user_role(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.change_role(int(serializer.validated_data['user_type']))
        user.save()
        logging.info(
            'user {} admin status changed to {}'.format(
                user.email, user.is_admin
            )
        )
        return response.Response(
            serializers.UserSerializer(
                user, context={'request': request}
            ).data,
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=['GET'], detail=False)
    def available_user_roles(self, request):
        roles = get_user_model().USER_TYPE_CHOICES
        roles_list = []
        for x, y in roles:
            roles_list.append({'value':x,'label':y})
        return response.Response(roles_list, status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_user_model().objects.all()
