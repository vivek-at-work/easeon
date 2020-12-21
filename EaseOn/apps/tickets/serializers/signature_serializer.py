# -*- coding: utf-8 -*-
from rest_framework import serializers
from tickets.models import UploadContent
import base64
from tickets import models
from django.core.files.base import ContentFile
from core.serializers import BaseMeta, BaseSerializer, UserSerializer


class Base64ImageField(serializers.ImageField):
    def __init__(self,file_name_prefix, *args, **kwargs):
        self.file_name_prefix = file_name_prefix
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = self.file_name_prefix + str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class TicketSignatureSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TicketSignatureSerializer, self).__init__(*args, **kwargs)
        self.fields['customer_signature'] = Base64ImageField("new"+str(self.instance))

    class Meta(BaseMeta):
        model = models.Ticket

class DeliverySignatureSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DeliverySignatureSerializer, self).__init__(*args, **kwargs)
        self.fields['customer_signature'] = Base64ImageField("new"+str(self.instance.ticket))

    class Meta(BaseMeta):
        model = models.Delivery

class VoucherSignatureSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(VoucherSignatureSerializer, self).__init__(*args, **kwargs)
        self.fields['customer_signature'] = Base64ImageField("new"+str(self.instance))

    class Meta(BaseMeta):
        model = models.Voucher

class LoanerRecordSignatureSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(LoanerRecordSignatureSerializer, self).__init__(*args, **kwargs)
        self.fields['customer_signature'] = Base64ImageField("new"+str(self.instance)+str(self.instance.ticket))

    class Meta(BaseMeta):
        model = models.LoanerRecord