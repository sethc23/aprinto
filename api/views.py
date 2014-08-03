# from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serializers import Initial_PDF_serializer,PDF_serializer
from app.models import PDF
from aprinto.settings import BASE_QR_URL,INCL_CHARS,INCL_CHARS_LEN
from random import randrange

class PDF_ViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDF_serializer

@api_view(['GET', 'POST'])
def check(request):

    if request.method == 'GET':
        x = PDF.objects.all()
        serializer = PDF_serializer(x, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        x = request.DATA[0]
        order_tag = ''.join(INCL_CHARS[randrange(0,INCL_CHARS_LEN)] for i in range(0,4))
        QR_url = BASE_QR_URL + x['pdf_id']
        output = {  'order_tag'   :   order_tag,
                    'QR_url'      :   QR_url,
                    'doc_post_url': 'http://printer.aporodelivery.com',
                    'qr_code_x' : 5,
                    'qr_code_y': 1,
                    'qr_code_scale': .5,        # .5 == 50%
                }            # .5 == 50%
        x.update(**output)
        serializer = Initial_PDF_serializer(data=x)#,context={'request': request}) # NOTE:  only 1 data pt here
        if serializer.is_valid():
            c = serializer.save()
            return Response(output, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

