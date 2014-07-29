from django.db import models

# Create your models here.
class PDF(models.Model):
    guid = models.CharField(max_length=38, primary_key=True) # e.g., 6B29FC40-CA47-1067-B31D-00DD010662DA
    created = models.DateTimeField(auto_now=True)
    order_tag = models.CharField(max_length=4)
    printer_id = models.TextField(blank=True,null=True)
    machine_id = models.TextField(blank=True,null=True)
    doc_name = models.TextField(blank=True,null=True)
    doc_path = models.TextField(blank=True,null=True)
    QR_url = models.TextField(blank=True,null=True)
    html = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return ' '.join([
                self.guid_id,
                self.created,
                self.order_tag,
                self.printer_id,
                self.machine_id,
                self.doc_name,
                self.doc_path,
                self.QR_url,
                self.html,
            ])