from django.template.loader_tags import register

from personnel.models import Contact


@register.inclusion_tag('personnel/tags/contact_list_youngest.html')
def top_young_contacts(limit=7):
    top = list(Contact.objects.exclude(birthday=None).order_by('-birthday')[:limit])
    return {
        'heading': '',
        'list': top
    }


@register.inclusion_tag('personnel/tags/contact_list_birthdays.html')
def upcoming_birthdays(limit=7):

    contacts = list(Contact.objects.raw("""
        SELECT id, birthday, username, first_name, last_name, patronymic, avatar
        FROM personnel_contact
        ORDER BY
           CASE date_part('doy', NOW()) > date_part('doy', birthday)
               WHEN TRUE THEN date_part('doy', birthday) + 366
               ELSE date_part('doy', birthday)
           END
        LIMIT %s
        """, [limit]))

    return {
        'heading': '',
        'list': contacts
    }
