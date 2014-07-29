# from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serializers import PDF_serializer
from app.models import PDF

class PDF_ViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDF_serializer

@api_view(['GET', 'POST'])
def pdf(request):

    x = request.DATA[0]

    if request.method == 'GET':
        x = PDF.objects.all()
        serializer = PDF_serializer(x, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # serializer = App_UserSerializer(data=x) # NOTE:  only 1 data pt here
        # if serializer.is_valid():
        #     c = serializer.save()
        #     this_user_type = c.app_user_type
        #
        #     if this_user_type == 'dg' or this_user_type == 'vend_mgr':
        #         this_user_id = c.app_user_id
        #         x.update({'app_user_id':this_user_id})
        #
        #         if this_user_type == 'dg':
        #             n = Currier(app_user_id=this_user_id)
        #             n.save()
        #             this_dg_id = n.currier_id
        #             x.update({'currier_id':this_dg_id})
        #
        #     # if this_user_type == 'vend_empl': no action needed
        #
        #     return Response(x, status=status.HTTP_201_CREATED)
        return Response(request.DATA, status=status.HTTP_400_BAD_REQUEST)

