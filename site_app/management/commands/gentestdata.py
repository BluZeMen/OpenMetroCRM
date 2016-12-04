import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from personnel.models import Contact, Location, JobType, Job, Contractor
from items.models import MeasuringInstrument, MeasuringInstrumentKind, MeasuringInstrumentType


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Contact.objects.filter(is_staff=False).delete()
        Location.objects.all().delete()
        Job.objects.all().delete()
        JobType.objects.all().delete()
        Contractor.objects.all().delete()
        MeasuringInstrumentKind.objects.all().delete()
        MeasuringInstrumentType.objects.all().delete()
        MeasuringInstrument.objects.all().delete()

        for name in ['ст. Симферополь', 'ст. Севастополь', 'ст. Бахчисарай', 'ст. Сирень', 'ст. Чистенькая',
                     'ст. Евпатория', 'ст. Почтовая', 'ст. Самохвалово', 'ст. Верхнесадовая']:
            Location.objects.create(name=name)

        locations = list(Location.objects.all())

        for name in ['Электромонтёр', 'Электромеханик', 'Старший электромеханик']:
            JobType.objects.create(name=name)

        job_types = list(JobType.objects.all())
        for l in locations:
            for p in range(random.randint(5,11)):
                job_type = random.choice(job_types)
                location = random.choice(locations)
                name = '%s %s #%i' % (job_type.name, location.name, p)
                Job.objects.create(name=name, type=job_type, location=location)

        today = datetime.today()
        jobs = list(Job.objects.all())
        for j in jobs:
            first_name = random.choice(['Василий', 'Пётр', 'Андрей', 'Денис', 'Максим', 'Николай', 'Константин'])
            patronymic = random.choice(['Васильевич', 'Пётрович', 'Андреевич', 'Денисович', 'Максимович', 'Николаевич',
                                        'Константинович'])
            last_name = random.choice(['Васильский', 'Петренко', 'Андреев', 'Денисовский', 'Максимко', 'Николаевиченко',
                                       'Константиновский'])
            year = random.choice(range(today.year - 60, today.year - 18))
            month = random.choice(range(1, 13))
            day = random.choice(range(1, 29))
            birthday = datetime(year, month, day)
            mobile_phone = '+' + str(random.randint(79780000000, 79789999999))
            username = mobile_phone;
            c = Contact.objects.create(first_name=first_name, patronymic=patronymic, last_name=last_name, gender=True,
                                       birthday=birthday, mobile_phone=mobile_phone, username=username)
            j.holder = c
            j.save()

        for c in Contact.objects.all():
            c.home_location = random.choice(locations)
            c.save()

        for name in ['ШЧ-1', 'ШЧ-2', 'ЛВЧД', 'ЭЧ', 'Крымский ЦСМ', 'Севастополь ЦСМ']:
            Contractor.objects.create(name=name)

        for name in ['Амперметр', 'Вольтметр', 'Электросекундомер', 'Осциллограф', 'Ампервольтомметр', 'Частотомер']:
            MeasuringInstrumentKind.objects.create(name=name)

        organizations = list(Contractor.objects.all())
        kinds = list(MeasuringInstrumentKind.objects.all())
        for k in kinds:
            for i in range(random.randint(4, 7)):
                name = (random.choice(['Ц', 'С', 'В', 'Ф', 'В', 'Д', 'Е'])
                        + str(random.randint(1, 7))
                        + '-'
                        + random.choice(['15', '28', '44', '25', '56', '11', '74']))
                check_periodicity = random.choice([12, 24, 36, 48])
                checking_organization = random.choice(organizations)
                MeasuringInstrumentType.objects.create(name=name, check_periodicity=check_periodicity,
                                                       kind=k, checking_organization=checking_organization)

        types = list(MeasuringInstrumentType.objects.all())
        for t in types:
            for i in range(0, random.randint(10, 30)):
                serial = (random.choice(['А', 'Б', 'В', 'Г', 'В', 'Е', 'И', 'К', 'Л', 'М', 'Н', 'П', 'Р', 'C'])
                          + str(random.randint(100000, 999999)))
                # rnd_shift = random.randint(-2, 2)
                # last_check_date = datetime.today() - timedelta(days=30 * (t.check_periodicity - rnd_shift))
                year = random.choice(range(2015, 2016))
                month = random.choice(range(1, 13))
                day = random.choice(range(1, 29))
                last_check_date = datetime(year, month, day)
                next_check_date = last_check_date + timedelta(days=30 * t.check_periodicity)
                holder = random.choice(jobs)
                MeasuringInstrument.objects.create(type=t, last_check_date=last_check_date, serial=serial,
                                                   holder=holder, next_check_date=next_check_date)
