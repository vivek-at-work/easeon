# -*- coding: utf-8 -*-
from core.serializers import PingPongSerializer
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class PingPongView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        serializer = PingPongSerializer(data=request.GET)
        if serializer.is_valid():
            if serializer.data["ping"] == "ping":
                return Response({"result": "pong"})
            else:
                return Response({"result": "What's in your head?"})
        else:
            return Response({"error": serializer.errors})
