
from django.db import models

from django.conf import settings
from os import path as os_path

from uuid import uuid4

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

DOCUMENT_STATES = (
    ('U', _('Uploaded')),
    ('S', _('Stored Remotely')),
    ('Q', _('Queued')),
    ('P', _('Processing')),
    ('F', _('Finished')),
    ('E', _('Processing Error')))


DEFAULT_PATH = os_path.join(settings.MEDIA_ROOT, "uploads")
UPLOAD_PATH = getattr(settings, "PDF_UPLOAD_PATH", DEFAULT_PATH)



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
    pdf_id = models.CharField(max_length=38, primary_key=True) # e.g., 6B29FC40-CA47-1067-B31D-00DD010662DA
    created = models.DateTimeField(auto_now=True)
    order_tag = models.CharField(max_length=4)
    printer_id = models.TextField(blank=True,null=True)
    machine_id = models.TextField(blank=True,null=True)
    application_name  = models.TextField(blank=True,null=True)
    doc_name = models.CharField(_("Title"), blank=True, null=True, max_length=100)
    local_document = models.FileField(_("Local Document"), null=True, blank=True,
                                      upload_to=path_and_rename(UPLOAD_PATH),
                                      max_length=255)
    QR_url = models.TextField(blank=True,null=True)
    html = models.TextField(blank=True,null=True)

    remote_document = models.URLField(_("Remote Document"), null=True, blank=True)
    status = models.CharField(_("Remote Processing Status"), default='U', max_length=1, choices=DOCUMENT_STATES)
    exception = models.TextField(_("Processing Exception"), null=True, blank=True)
    pages = models.IntegerField(_("Number of Pages in Document"), null=True, blank=True)

    page_html = models.TextField(null=True, blank=True)

    date_uploaded = models.DateTimeField(_("Date Uploaded"),auto_now=True)
    date_stored = models.DateTimeField(_("Date Stored Remotely"), null=True, blank=True)
    date_queued = models.DateTimeField(_("Date Queued"), null=True, blank=True)
    date_process_start = models.DateTimeField(_("Date Process Started"), null=True, blank=True)
    date_process_end = models.DateTimeField(_("Date Process Completed"), null=True, blank=True)
    date_exception = models.DateTimeField(_("Date of Exception"), null=True, blank=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __unicode__(self):
        return ' '.join([
                self.pdf_id,
                self.created,
                self.order_tag,
                self.printer_id,
                self.machine_id,
                self.application_name,
                self.doc_name,
                self.local_document,
                self.QR_url,
                self.html,
            ])

    def get_detail_url(self):
        return reverse("pdf_detail", kwargs={'pdf_id': self.pdf_id})

    def save(self, **kwargs):
        super(PDF, self).save(**kwargs)