
from django.db import models

# from django.conf import settings
from os import path as os_path

from uuid import uuid4

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

DOCUMENT_STATES = (
    ('U', _('Uploaded')),
    ('Q', _('Queued')),
    ('X', _('XML Created from PDF')),
    ('S', _('XML Saved to DB')),
    ('P', _('XML Parsed and DB Updated')),
    ('F', _('Order Forwarded to GnamGnam')),
    ('E', _('Processing Error')),
    ('C', _('Processing Complete')),
    ('AR', _('Admin Request')),
    ('NV',_('New Vendor Added')),
    ('UKN',_('Unknown Sources')))


def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pdf_id:
            filename = '{a}.{b}'.format(a=instance.pdf_id, b=ext)
        else:
            # set filename as random string
            filename = '{a}.{b}'.format(a=uuid4().hex, b=ext)
        # return the whole path to the file
        return os_path.join(path, filename)
    return wrapper

class PDF(models.Model):
    pdf_id          = models.CharField(max_length=38, primary_key=True) # e.g., 6B29FC40-CA47-1067-B31D-00DD010662DA
    created         = models.DateTimeField(auto_now=True)
    order_tag       = models.CharField(max_length=4,blank=True,null=True)
    printer_id      = models.TextField(blank=True,null=True)
    machine_id      = models.TextField(blank=True,null=True)
    application_name= models.TextField(blank=True,null=True)
    doc_name        = models.CharField(_("Title"), blank=True, null=True, max_length=100)
    # local_document = models.FileField(_("Local Document"), null=True, blank=True,
    #                                   upload_to=path_and_rename(settings.PDF_UPLOAD_PATH),
    #                                   max_length=255)
    local_document  = models.FileField(_("Local Document"), null=True, blank=True,
                                      upload_to='uploads/',
                                      max_length=255)
    qr_url          = models.TextField(blank=True,null=True)
    doc_as_xml      = models.TextField(blank=True,null=True)

    vendor_id       = models.IntegerField(blank=True,null=True)
    cust_name       = models.TextField(blank=True,null=True)
    cust_tel        = models.TextField(blank=True,null=True)
    cust_addr       = models.TextField(blank=True,null=True)
    cust_cross_st   = models.TextField(blank=True,null=True)
    order_price     = models.FloatField(blank=True,null=True)
    order_tip       = models.FloatField(blank=True,null=True)

    remote_document = models.URLField(_("Remote Document"), null=True, blank=True)
    status          = models.CharField(_("Remote Processing Status"), default='U', max_length=3, choices=DOCUMENT_STATES)
    processing_exception = models.TextField(_("Processing Exception"), null=True, blank=True)
    #pages           = models.IntegerField(_("Number of Pages in Document"), null=True, blank=True)

    # page_html = models.TextField(null=True, blank=True)

    date_uploaded   = models.DateTimeField(_("Date Uploaded"),auto_now=True)
    date_queued     = models.DateTimeField(_("Date Queued"), null=True, blank=True)
    date_extracted  = models.DateTimeField(_("Date Extracted"), null=True, blank=True)
    date_xml_saved  = models.DateTimeField(_("Date XML Saved"), null=True, blank=True)
    date_order_fwd_gg = models.DateTimeField(_("Date Order Forwarded"), null=True, blank=True)
    date_completed  = models.DateTimeField(_("Date Processing Completed"), null=True, blank=True)
    date_exception  = models.DateTimeField(_("Date of Exception"), null=True, blank=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __unicode__(self):
        value_list = [  self.pdf_id,
                        self.created,
                        self.order_tag,
                        self.printer_id,
                        self.machine_id,
                        self.application_name,
                        self.doc_name,
                        self.local_document,
                        self.qr_url,
                        self.doc_as_xml ]
        return ','.join(str(v) for v in value_list)
        # return ' '.join(value_list)

    def get_detail_url(self):
        return reverse("pdf_detail", kwargs={'pdf_id': self.pdf_id})

    def save(self, **kwargs):
        super(PDF, self).save(**kwargs)

class vendor(models.Model):
    vendor_id       = models.AutoField(max_length=11, primary_key=True)
    created         = models.DateTimeField(auto_now=True)
    machine_id      = models.TextField(blank=True,null=True)
    vend_name       = models.TextField(blank=True,null=True)
    vend_addr       = models.TextField(blank=True,null=True)
    vend_tel        = models.CharField(max_length=10,blank=True,null=True)
    recipient_emails= models.TextField(blank=True,null=True)

class admin(models.Model):
    admin_id        = models.AutoField(max_length=11, primary_key=True)
    created         = models.DateTimeField(auto_now=True)
    machine_id      = models.TextField(blank=True,null=True)
    admin_name      = models.TextField(blank=True,null=True)
    admin_tel       = models.CharField(max_length=10,blank=True,null=True)
    admin_email     = models.EmailField(blank=True,null=True)