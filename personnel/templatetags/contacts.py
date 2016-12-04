import datetime

from django.template.loader_tags import register
from django.db.models import F

from personnel.models import Contact, Job


@register.inclusion_tag('personnel/tags/contact_list_youngest.html')
def top_young_contacts(limit=7):
    top = list(Contact.objects.all().order_by('-birthday')[:limit])
    return {
        'heading': '',
        'list': top
    }


@register.inclusion_tag('personnel/tags/contact_list.html')
def work_near_home(limit=7):
    jobs = list(Job.objects.raw("""SELECT j.id, j.location_id, j.holder_id
                                   FROM personnel_job AS j
                                   LEFT OUTER JOIN personnel_contact AS c ON j.holder_id = c.id
                                   WHERE j.location_id = c.home_location_id
                                   LIMIT %s
                                """, [limit]))
    contacts = [job.holder for job in jobs]
    return {
        'heading': '',
        'list': contacts
    }


@register.inclusion_tag('personnel/tags/contact_list_birthdays.html')
def upcoming_birthdays(limit=7):
    contacts = list(Contact.objects.raw("""
        SELECT c.id, c.birthday, c.username, c.first_name, c.last_name, c.patronymic
        FROM personnel_contact AS c
        WHERE date_part('doy', birthday) >= date_part('doy', current_date)
        ORDER BY date_part('doy', birthday)
        LIMIT %s
        """, [limit]))

    return {
        'heading': '',
        'list': contacts
    }
