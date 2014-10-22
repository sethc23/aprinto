# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app.models import PDF

class PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF

class Initial_PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ['pdf_id','order_tag','application_name','doc_name','QR_url','machine_id','printer_id','doc_post_url','qr_code_x','qr_code_y','qr_code_scale']