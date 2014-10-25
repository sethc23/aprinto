# from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serializers import PDF_serializer
from app.models import PDF
from aprinto.settings import BASE_QR_URL,INCL_CHARS,INCL_CHARS_LEN
from random import randrange

# import logging
# logger = logging.getLogger(__name__)

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
<<<<<<< HEAD
                    'qr_code_scale': 0.001,        # .5 == 50%# .5 == 50%
                    'tag_x' : 5,
                    'tag_y': 1,
                    'tag_scale': 0.001,            # .5 == 50%
=======
                    'qr_code_scale': 0,        # .5 == 50%# .5 == 50%
                    'tag_x' : 5,
                    'tag_y': 1,
                    'tag_scale': 0,            # .5 == 50%
>>>>>>> origin/master
                }
        x.update(**output)
        serializer = PDF_serializer(data=x,context={'request': request}) # NOTE:  only 1 data pt here
        if serializer.is_valid():
            c = serializer.save()
            return Response(output, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render_to_response
from app.forms import PDF_Form
from django.http import HttpResponse
from django.template import RequestContext

@api_view(['GET', 'POST'])
def doc_upload(request):
    if request.method == 'POST':
        x=request.POST.dict()
        doc = PDF.objects.get(pdf_id=x['pdf_id'])
        form = PDF_Form(request.DATA, request.FILES,instance=doc)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse(str({'order_tag':doc.order_tag,
                                     'QR_url':doc.QR_url}))
    else:
        form = PDF_Form()
    return render_to_response('pdf/upload.html', {'form': form}, context_instance=RequestContext(request))