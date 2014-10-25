# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app.models import PDF

class PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ['pdf_id', 'created', 'order_tag','printer_id', 'machine_id', 'application_name',
                  'doc_name', 'local_document', 'qr_url', 'html',
                  'remote_document', 'status', 'exception', 'pages', 'page_html',
                  'date_uploaded', 'date_stored', 'date_queued',
                  'date_process_start', 'date_process_end', 'date_exception']

class Initial_PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ['pdf_id','order_tag','application_name','doc_name','qr_url',
                  'machine_id','printer_id','doc_post_url','qr_code_x','qr_code_y','qr_code_scale']