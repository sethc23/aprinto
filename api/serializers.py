# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app.models import PDF

class PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
