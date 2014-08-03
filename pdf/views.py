from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from pdf.forms import DocumentForm,PDF_Form
from pdf.tasks import process_file,extract_text
from pdf.models import Document
from app.models import PDF

from django.contrib.auth.models import User
from aprinto.settings import BASE_QR_URL,INCL_CHARS,INCL_CHARS_LEN
from uuid import uuid4 as get_guid
from random import randrange

#@login_required
def doc_upload(request):
    if request.method == 'POST':
        form = PDF_Form(request.POST, request.FILES)
        if form.is_valid():
            doc = PDF.objects.get(pdf_id=form.data.get('pdf_id'))
            doc.local_document = form.files.get('local_document')
            doc.save()
            process_file.delay(doc)
            return HttpResponse(str({'order_tag':doc.order_tag,
                                     'QR_url':doc.QR_url}))
    else:
        # form = DocumentForm()
        form = PDF_Form()
    return render_to_response('pdf/upload.html', {'form': form}, context_instance=RequestContext(request))


#@login_required
def doc_list(request):
    # u = User.objects.get(username='seth')
    # u.set_password('seth')
    # u.save()
    # context = {'pdfs': Document.objects.filter(user=request.user)}
    # context = {'pdfs': Document.objects.all()}
    context = {'PDFS': PDF.objects.all()}
    return render_to_response('app/list.html', context, context_instance=RequestContext(request))


#@login_required
def doc_detail(request, pdf_id):
    # context = {'pdf': Document.objects.get(uuid=uuid)}
    context = {'PDFS': PDF.objects.get(pdf_id=str(pdf_id))}
    return render_to_response('app/detail.html', context, context_instance=RequestContext(request))

