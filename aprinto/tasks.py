from __future__ import absolute_import
from os import system as os_cmd
from os import path as os_path
from datetime import datetime as dt
from celery import shared_task
from aprinto.settings import FWD_ORDER
import requests
from json import dumps as j_dumps
from aprinto.models import vendor,admin
from bs4 import BeautifulSoup as soup
from re import findall as re_findall
from re import sub as re_sub
from pandas import DataFrame as pd_DataFrame
from sqlalchemy import create_engine
engine = create_engine(r'postgresql://postgres:postgres@192.168.3.52:8800/aprinto',
                       encoding='utf-8',
                       echo=False)
from codecs import encode as codecs_encode
import sys
reload(sys)
sys.setdefaultencoding('UTF8')


def parse_xml(pdf):
    x = soup(codecs_encode(pdf,'utf8','ignore')).findAll('page')
    cols = ['page','font','top','left','width','height','text']
    g = pd_DataFrame(columns=cols)
    for pg in x:
        idx = x.index(pg)+1
        pg = str(pg)
        line_iter = re_findall(r'(<text.*?</text>)',pg)

        for it in line_iter:
            a = ['page']+re_findall('([a-zA-Z]+)+\=', it)+['text']
            text_attrs = it[5:it.find('>')].strip()
            text_contents = str(soup(it).text)
            b = [idx]+map(lambda s: int(s),re_findall('[0-9]+', text_attrs))+[text_contents]
            if text_contents.strip() != '':
                g = g.append(dict(zip(a,b)),ignore_index=True)
    return g
def parse_order(xml):
    pass

@shared_task
def cleanup_uploads(doc,f_pdf,new_folder='processed',end_status='C'):
    new_file_name       = doc.order_tag+'_'+doc.pdf_id+'.pdf'
    new_f_pdf           = os_path.dirname(os_path.dirname(f_pdf))+'/'+new_folder+'/'+new_file_name
    os_cmd('mv '+f_pdf+' '+new_f_pdf)
    doc.local_document  = new_f_pdf
    doc.status          = end_status
    doc.date_completed  = dt.utcnow()
    doc.save()
    return True
@shared_task
def fwd_order_to_gnamgnam(doc,vend,f_pdf):
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
        cleanup_uploads.delay(doc,f_pdf)
        return True

    else:
        # TODO: SEND EMAIL IF PROCESSING ERROR
        doc.processing_exception = True
        doc.status = 'E'
        doc.date_exception = dt.utcnow()
        doc.save()
        return False
@shared_task
def read_order_into_db(doc,f_pdf):

    #doc = parse_order(doc.doc_as_xml)

    ### -->>  SAMPLE DATA:
    doc.vendor_id       = 1
    doc.cust_name       = doc.application_name
    doc.cust_tel        = '555-555-5555'
    doc.cust_addr       = '121 Madison Ave., New York, NY 10016'
    doc.cust_cross_st   = '30th & Madison.'
    doc.order_price     = 20.00
    doc.order_tip       = 5.00
    ### <<--

    v = vendor.objects.get(vendor_id=doc.vendor_id)


    doc.status = 'P'
    doc.date_xml_parsed = dt.utcnow()
    doc.save()

    if FWD_ORDER:   fwd_order_to_gnamgnam.delay(doc,v,f_pdf)
    else:           cleanup_uploads.delay(doc,f_pdf)

    return True
@shared_task
def read_xml_into_db(doc,f_pdf,cred):
    f_xml = f_pdf.replace('.pdf','.xml')
    f = open(f_xml,'r')
    doc.doc_as_xml = f.read()
    f.close()
    doc.status = 'S'
    doc.date_xml_saved = dt.utcnow()
    doc.save()
    os_cmd('rm '+f_xml)

    if cred=='vendor':  read_order_into_db.delay(doc,f_pdf)
    elif cred=='admin': admin_req.delay(doc,f_pdf)

    return True
@shared_task
def extract_text(doc,f_pdf,cred='credentials'):
    f_xml = f_pdf.replace('.pdf','.xml')
    os_cmd('/usr/bin/pdftohtml -i -c -xml '+f_pdf+' '+f_xml)
    doc.status = 'X'
    doc.date_extracted = dt.utcnow()
    doc.save()
    read_xml_into_db.delay(doc,f_pdf,cred)
    return True
@shared_task
def add_new_vendor_info(doc,f_pdf,g='Parsed PDF'):
    p = parties     = g[ ((115<=g.top)&(g.top<=200)) ]
    c = client      = p[ ((520<=p.left)&(p.left<=530)) ].sort('top')
    c = c.text.map(lambda s: unicode(s, errors='ignore')).tolist()
    v_tel           = re_sub(r'[\W_]+', '', c[3])
    if not vendor.objects.filter(vend_tel=v_tel):
        v,v_created = vendor.objects.get_or_create(created=dt.utcnow(),
                                                   vend_name=c[0].strip(),
                                                   vend_addr=c[1].strip()+', '+c[2].strip(),
                                                   vend_tel=v_tel)
        v.save()
        doc.vendor_id = v.vendor_id
        doc.status      = 'NV'
        cleanup_uploads(doc,f_pdf,new_folder='contracts',end_status='NV')
    else:
        cleanup_uploads(doc,f_pdf,new_folder='to_review',end_status='AR')
    doc.save()
    return True
@shared_task
def admin_req(doc,f_pdf):
    g               = parse_xml(doc.doc_as_xml)
    trial_k         = g.sort('top').text.str.contains(r'SERVICE AGREEMENT.*Trial Period').tolist().count(True)!=0
    if trial_k:     add_new_vendor_info.delay(doc,f_pdf,g)
    doc.status      = 'AR'
    doc.save()
    return True
@shared_task
def unknown_req(doc,f_pdf):
    # TODO: aprinto/tasks   add function for handling UNKNOWN requests
    cleanup_uploads(doc,f_pdf,new_folder='unknown',end_status='UKN')
    return True
@shared_task
def queue_file(doc):
    """
    Vendor PDF Workflow:                         Document State:
        .. (default state on upload)                    U
        1. add doc to queue for processing          --> Q
        2. generate XML from PDF,                   --> X
        3. save XML contents to DB                  --> S
        4. parse contents and update DB             --> P
        5. forward order to gnamgnam                --> F
        6. [ if exception/error ... ]               --> E
        7. [ if completed ... ]                     --> C

    Admin Workflow:                          Document State:
        .. (default state on upload)                    U
        1. request directed to admin                --> AR
        2. new vendor added                         --> NV

    """
    f_pdf = doc.local_document.path
    doc.status = 'Q'
    doc.date_queued = dt.utcnow()
    doc.save()

    # # Check Credentials and Queue Files Accordingly
    vendor_chk          = vendor.objects.filter(machine_id=doc.machine_id).exists()
    admin_chk           = admin.objects.filter(machine_id=doc.machine_id).exists()
    if vendor_chk:      extract_text.delay(doc,f_pdf,cred='vendor')
    elif admin_chk:     extract_text.delay(doc,f_pdf,cred='admin')
    else:               unknown_req.delay(doc,f_pdf)

    return True

# TODO: aprinto/tasks   add periodic function to clean up uploads (add email notification)

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
