# -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import decorators, response, status, viewsets

BaseReadOnlyViewSet = viewsets.ReadOnlyModelViewSet


class BaseViewSet(viewsets.ModelViewSet):
    retrieve_serializer_class = None
    ordering = ['-id']
    rights_for = 'tickets'

    def get_user_organizations_filter_by_right(self):
        return {self.rights_for: True, 'is_active': True}

    def get_user_organizations(self):
        organizations = self.request.user.locations.filter(
            **self.get_user_organizations_filter_by_right()
        ).values_list('organization', flat=True)
        managed_organizations = self.request.user.managed_locations.filter(
            is_deleted=False
        ).values_list('id', flat=True)
        return organizations, managed_organizations

    def create(self, request, *args, **kwargs):
        if self.retrieve_serializer_class is not None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instanse = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            result = self.retrieve_serializer_class(
                instanse, context={'request': request}
            ).data
            return response.Response(
                result, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return super(BaseViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

    def get_serializer_class(self):

        if self.action == 'list':
            if getattr(self, 'list_serializer_class', None) is not None:
                return self.list_serializer_class
            else:
                return self.serializer_class
        if self.action == 'retrieve':
            if getattr(self, 'retrieve_serializer_class', None) is not None:
                return self.retrieve_serializer_class
            else:
                return self.serializer_class
        if (
            self.action == 'destroy'
            and getattr(self, 'delete_serializer_class', None) is not None
        ):
            return self.delete_serializer_class
        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        with transaction.atomic():
            record.delete()
            if getattr(self, 'delete_serializer_class', None) is not None:
                serializer = self.delete_serializer_class(
                    record, context={'request': request}
                )
                return response.Response(serializer.data)

            serializer = self.serializer_class(
                record, context={'request': request}
            )
            return response.Response(serializer.data)

    def update(self, request, pk=None):
        if self.retrieve_serializer_class is not None:
            super(BaseViewSet, self).update(request, pk)
            ticket = self.get_object()
            context = {'request': request}
            serializer = self.retrieve_serializer_class(
                ticket, context=context
            )
            return response.Response(serializer.data)
        else:
            return super(BaseViewSet, self).update(request, pk)

    def partial_update(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer_class()(
            obj, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        obj = self.get_object()
        data = self.retrieve_serializer_class(
            obj, context={'request': request}
        ).data
        return response.Response(
            data, status=status.HTTP_200_OK, headers=headers
        )


class BaseBulkCreateViewSet(BaseViewSet):
    """docstring for BaseBulkCreateViewSet"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
