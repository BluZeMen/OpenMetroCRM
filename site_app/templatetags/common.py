from django.template.loader_tags import register

from personnel.models import Contractor


@register.inclusion_tag('tags/contractor_list.html')
def top_contractor_debtors(limit=7):
    contractors = list(Contractor.objects.raw("""
        SELECT debt.contractor_id AS id, name, COUNT(debt.id) AS debts_count FROM (
            SELECT
                mi.id,
                mi.holder_id,
                mi.last_check_date,
                mit.check_periodicity,
                job.contractor_id,
                contr.name
            FROM
                items_measuringinstrument AS mi,
                items_measuringinstrumenttype AS mit,
                personnel_job AS job,
                personnel_contractor AS contr
            WHERE
                mi.holder_id = job.id
                AND job.contractor_id = contr.id
                AND mi.type_id = mit.id
                AND (mi.last_check_date + (mit.check_periodicity::text||' month')::interval) < current_date
            ORDER BY
                mi.last_check_date + (mit.check_periodicity::text||' month')::interval
            ) AS debt
        GROUP BY debt.contractor_id, debt.name
        ORDER BY debts_count DESC
        LIMIT %s
    """, [limit]))
    return {
        'heading': '',
        'list': contractors
    }
