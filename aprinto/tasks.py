from __future__ import absolute_import
from os import system as os_cmd
from os import path as os_path
from datetime import timedelta
from datetime import datetime as dt
from celery import shared_task
#from uuid import uuid4
#from django.conf import settings
#from celery.decorators import task
#from celery.task import PeriodicTask
#from pdf.models import Document
import requests
from json import dumps as j_dumps
from app.models import vendor

@shared_task
def cleanup_uploads(doc,f_pdf,f_xml):
    os_cmd('rm '+f_xml)
    new_f_pdf = os_path.dirname(os_path.dirname(f_pdf))+'/processed/'+f_pdf[f_pdf.rfind('/')+1:]
    if os_path.isfile(new_f_pdf):
        new_f_pdf = new_f_pdf.replace('.pdf','_dupe.pdf')
    # TODO: SEND EMAIL IF DUPE FILE
    os_cmd('mv '+f_pdf+' '+new_f_pdf)
    doc.local_document = new_f_pdf
    doc.status = 'C'
    doc.date_completed = dt.utcnow()
    doc.save()
    return True
@shared_task
def fwd_order_to_gnamgnam(doc,f_pdf,f_xml):
    user_id         = '544963fce4b00f942bc97027'
    satellite_id    = '544963fce4b00f942bc9702e'

    post_url        = 'http://admin.gnamgnamapp.com/ws/v2/'+user_id+'/aporoOrders'
    # post_url = 'http://93.148.124.46:9000/ws/v2/'+user_id+'/aporoOrders'

    vend = vendor.objects.get(vendor_id=doc.vendor_id)
    data = [{
                'satellite_id'      : satellite_id,
                'cust_name'         : doc.cust_name,
                'cust_tel'          : doc.cust_tel,
                'cust_addr'         : doc.cust_addr,
                'cust_cross_st'     : doc.cust_cross_st,
                'price'             : doc.order_price,
                'tip'               : doc.order_tip,
                'order_uuid'        : doc.pdf_id,
                'order_time'        : dt.strftime(doc.created,'%Y%m%d%H:%M:%S')+'-0000',
                'order_tag'         : doc.order_tag,
                'vend_name'         : vend.biz_name,
                'vend_addr'         : vend.addr,
                'recipient_emails'  : vend.recipient_emails,
                }
            ]

    json_data = j_dumps(data).encode('utf-8')
    headers = {'Content-type': 'application/json'}
    response = requests.post(post_url, data=json_data, headers=headers)

    if response.status_code==200:
        doc.status = 'F'
        doc.date_order_fwd_gg = dt.utcnow()
        doc.save()
        cleanup_uploads.delay(doc,f_pdf,f_xml)
        return True

    else:
        # TODO: SEND EMAIL IF PROCESSING ERROR
        doc.processing_exception = True
        doc.status = 'E'
        doc.date_exception = dt.utcnow()
        doc.save()
        return False
@shared_task
def parse_xml_and_update_db(doc,f_pdf,f_xml):

    # SET CUSTOMER NAME TO: doc.application_name+': ' + doc first line

    # sample data:
    doc.vendor_id       = 1
    doc.cust_name       = doc.application_name
    doc.cust_tel        = '555-555-5555'
    doc.cust_addr       = '121 Madison Ave., New York, NY 10016'
    doc.cust_cross_st   = '30th & Madison.'
    doc.order_price     = 20.00
    doc.order_tip       = 5.00


    doc.status = 'D'
    doc.date_xml_parsed = dt.utcnow()
    doc.save()

    fwd_order_to_gnamgnam.delay(doc,f_pdf,f_xml)

    return True
@shared_task
def read_xml_and_update_db(doc,f_pdf,f_xml):
    f = open(f_xml,'r')
    doc.doc_as_xml = f.read()
    f.close()
    doc.status = 'S'
    doc.date_xml_saved = dt.utcnow()
    doc.save()

    parse_xml_and_update_db.delay(doc,f_pdf,f_xml)

    return True
@shared_task
def extract_text(doc,f_pdf):
    f_xml = f_pdf.replace('.pdf','.xml')
    os_cmd('/opt/local/bin/pdftohtml -i -c -xml '+f_pdf+' '+f_xml)
    doc.status = 'X'
    doc.date_extracted = dt.utcnow()
    doc.save()
    read_xml_and_update_db.delay(doc,f_pdf,f_xml)

    return True
@shared_task
def process_file(doc):
    """
    Workflow:                                   Document State:
        .. (file previously uploaded)                   U
        1. add doc to queue for processing          --> Q
        1. generate XML from PDF,                   --> X
        2. save XML contents to DB                  --> S
        3. parse contents and update DB             --> D
        4. forward order to gnamgnam                --> F
        5. [ if exception/error ... ]               --> E
        6. [ if completed ... ]                     --> C
    """
    f_pdf = doc.local_document.path
    doc.status = 'Q'
    doc.date_queued = dt.utcnow()
    doc.save()

    extract_text.delay(doc,f_pdf)

    return True

#
# class CheckResponseQueueTask(PeriodicTask):
#     """
#     Checks response queue for messages returned from running processes in the
#     cloud.  The messages are read and corresponding `pdf.models.Document`
#     records are updated.
#     """
#     run_every = timedelta(seconds=30)
#
#     # def _dequeue_json_message(self):
#     #     sqs = boto.connect_sqs(settings.PDF_AWS_KEY, settings.PDF_AWS_SECRET)
#     #     queue = sqs.create_queue(RESPONSE_QUEUE)
#     #     msg = queue.read()
#     #     if msg is not None:
#     #         data = simplejson.loads(msg.get_body())
#     #         bucket = data.get('bucket', None)
#     #         key = data.get("key", None)
#     #         queue.delete_message(msg)
#     #         if bucket is not None and key is not None:
#     #             return data
#
#     def run(self, **kwargs):
#         logger = self.get_logger(**kwargs)
#         logger.info("Running periodic task!")
#         data = self._dequeue_json_message()
#         if data is not None:
#             Document.process_response(data)
#             return True
#         return False
#
#
# class CheckQueueLevelsTask(PeriodicTask):
#     """
#     Checks the number of messages in the queue and compares it with the number
#     of instances running, only booting nodes if the number of queued messages
#     exceed the number of nodes running.
#     """
#     run_every = timedelta(seconds=60)
#
#     # def run(self, **kwargs):
#     #     ec2 = boto.connect_ec2(settings.PDF_AWS_KEY, settings.PDF_AWS_SECRET)
#     #     sqs = boto.connect_sqs(settings.PDF_AWS_KEY, settings.PDF_AWS_SECRET)
#     #
#     #     queue = sqs.create_queue(REQUEST_QUEUE)
#     #     num = queue.count()
#     #     launched = 0
#     #     icount = 0
#     #
#     #     reservations = ec2.get_all_instances()
#     #     for reservation in reservations:
#     #         for instance in reservation.instances:
#     #             if instance.state == "running" and instance.image_id == AMI_ID:
#     #                 icount += 1
#     #     to_boot = min(num - icount, MAX_INSTANCES)
#     #
#     #     if to_boot > 0:
#     #         startup = BOOTSTRAP_SCRIPT % {
#     #             'KEY': settings.PDF_AWS_KEY,
#     #             'SECRET': settings.PDF_AWS_SECRET,
#     #             'RESPONSE_QUEUE': RESPONSE_QUEUE,
#     #             'REQUEST_QUEUE': REQUEST_QUEUE}
#     #         r = ec2.run_instances(
#     #             image_id=AMI_ID,
#     #             min_count=to_boot,
#     #             max_count=to_boot,
#     #             key_name=KEYPAIR,
#     #             security_groups=SECURITY_GROUPS,
#     #             user_data=startup)
#     #         launched = len(r.instances)
#     #     return launched
