import datetime

from django.template.loader_tags import register

from personnel.models import Contact, Job
from items.models import MeasuringInstrument, MeasuringInstrumentType, MeasuringInstrumentKind

@register.inclusion_tag('personnel/tags/contact_list_debtors.html')
def top_debtors(limit=7):
    jobs = list(Job.objects.raw("""SELECT j.id, j.holder_id
                                   FROM personnel_job AS j
                                   ORDER BY 
                                   LIMIT %s
                                """, [limit]))
    contacts = [job.holder for job in jobs]
    return {
        'heading': '',
        'list': contacts
    }