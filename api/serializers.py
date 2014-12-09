# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from aprinto.models import PDF

class PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ['pdf_id', 'created', 'order_tag','printer_id', 'machine_id', 'application_name',
                  'doc_name', 'local_document', 'qr_url', 'doc_as_xml',
                  'vendor_id','cust_name','cust_tel','cust_addr','cust_cross_st','order_price','order_tip',
                  'remote_document', 'status', 'processing_exception',
                  'date_uploaded', 'date_queued', 'date_extracted','date_xml_saved',
                  'date_order_fwd_gg','date_completed', 'date_exception']

class Initial_PDF_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PDF
        fields = ['pdf_id','printer_id','machine_id','application_name','doc_name']