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
from aprinto.settings import BASE_QR_URL,INCL_CHARS
from uuid import uuid4 as get_guid

#@login_required
def doc_upload(request):
    if request.method == 'POST':
        form = PDF_Form(request.POST, request.FILES)
        if form.is_valid():
            # u = User.objects.get(username='seth')
            # u.set_password('seth')
            # u.save()

            doc = form.save(commit=False)
            x=request.POST.dict()
            # doc.user = request.user
            guid = x['pdf_id']
            order_tag = ''.join(c for c in guid if c in INCL_CHARS)[:4]
            QR_url = BASE_QR_URL+guid
            output = {'order_tag':order_tag,
                      'QR_url':QR_url}

            doc.pdf_id = guid
            doc.doc_name = x['name']
            doc.order_tag = order_tag
            doc.QR_url = QR_url

            #doc.user = u
            #doc.date_uploaded = datetime.utcnow()
            doc.save()
            process_file.delay(doc)
            # return HttpResponseRedirect(reverse('pdf_list'))
            return HttpResponse(str(output))
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
    context = {'PDF': PDF.objects.get(pdf_id=str(pdf_id))}
    return render_to_response('app/detail.html', context, context_instance=RequestContext(request))


from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)