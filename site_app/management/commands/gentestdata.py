import random
from datetime import datetime, timedelta

import elizabeth
from django.core.management.base import BaseCommand

from items.models import MeasuringInstrument, MeasuringInstrumentKind, MeasuringInstrumentType
from personnel.models import Contact, Location, JobType, Job, Contractor


class Command(BaseCommand):
    help = 'Creates test data'

    persons = {
        'first_name': ['Василий', 'Пётр', 'Андрей', 'Денис', 'Максим', 'Николай', 'Константин', 'Руслан', 'Артём',
                       'Семён'],
        'patronymic': ['Васильевич', 'Пётрович', 'Андреевич', 'Денисович', 'Максимович', 'Николаевич',
                       'Константинович', 'Русланович', 'Артёмович', 'Семёнович'],
        'last_name': ['Васильев', 'Петренко', 'Андреев', 'Денисовский', 'Максименко', 'Николаевиченко',
                      'Константинов', 'Русланов', 'Артёменко', 'Семенченко']
    }

    locations = ['ст. Симферополь', 'ст. Севастополь', 'ст. Бахчисарай', 'ст. Сирень', 'ст. Чистенькая',
                     'ст. Евпатория', 'ст. Почтовая', 'ст. Самохвалово', 'ст. Верхнесадовая']
    jobs = ['Электромонтёр', 'Электромеханик', 'Старший электромеханик']
    contractors = ['ШЧ-1', 'ШЧ-2', 'ЛВЧД', 'ЭЧ', 'Крымский ЦСМ', 'Севастополь ЦСМ']
    mi_kinds = ['Амперметр', 'Вольтметр', 'Электросекундомер', 'Осциллограф', 'Ампервольтомметр', 'Частотомер']

    def handle(self, *args, **options):
        Contact.objects.filter(is_staff=False).delete()
        Location.objects.all().delete()
        Job.objects.all().delete()
        JobType.objects.all().delete()
        Contractor.objects.all().delete()
        MeasuringInstrumentKind.objects.all().delete()
        MeasuringInstrumentType.objects.all().delete()
        MeasuringInstrument.objects.all().delete()

        for name in self.locations:
            Location.objects.create(name=name)

        locations = list(Location.objects.all())

        for name in self.jobs:
            JobType.objects.create(name=name)

        for name in self.contractors:
            Contractor.objects.create(name=name, full_name=name, location=random.choice(locations))

        contractors = list(Contractor.objects.all())

        job_types = list(JobType.objects.all())
        for l in locations:
            for p in range(random.randint(7, 15)):
                job_type = random.choice(job_types)
                location = random.choice(locations)
                contractor = random.choice(contractors)
                name = '%s %s #%i' % (job_type.name, location.name, p)
                Job.objects.create(name=name, type=job_type, location=location, contractor=contractor)

        today = datetime.today()
        jobs = list(Job.objects.all())
        for j in jobs:
            first_name = random.choice(self.persons['first_name'])
            patronymic = random.choice(self.persons['patronymic'])
            last_name = random.choice(self.persons['last_name'])
            year = random.choice(range(today.year - 60, today.year - 19))
            month = random.choice(range(1, 13))
            day = random.choice(range(1, 29))
            birthday = datetime(year, month, day)
            mobile_phone_numbers = str(random.randint(79780000000, 79789999999))
            mobile_phone = '+' + mobile_phone_numbers
            email = mobile_phone_numbers + '@workmail.ru'
            username = mobile_phone_numbers
            c = Contact.objects.create(first_name=first_name, patronymic=patronymic, last_name=last_name, gender=True,
                                       birthday=birthday, mobile_phone=mobile_phone, username=username, email=email)
            j.holder = c
            j.save()

        for c in Contact.objects.all():
            c.home_location = random.choice(locations)
            c.save()

        for name in self.mi_kinds:
            MeasuringInstrumentKind.objects.create(name=name)

        organizations = list(Contractor.objects.all())
        kinds = list(MeasuringInstrumentKind.objects.all())
        for k in kinds:
            for i in range(random.randint(6, 9)):
                name = (random.choice(['Ц', 'С', 'В', 'Ф', 'В', 'Д', 'Е'])
                        + str(random.randint(1, 7))
                        + '-'
                        + random.choice(['15', '28', '44', '25', '56', '11', '74']))
                check_periodicity = timedelta(days=int(365 * random.choice([0.5, 1, 2, 3, 4])))
                checking_organization = random.choice(organizations)
                MeasuringInstrumentType.objects.create(name=name, check_periodicity=check_periodicity,
                                                       kind=k, checking_organization=checking_organization)

        start = datetime.today() - timedelta(days=12 * 30)
        end = datetime.today()
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds

        types = list(MeasuringInstrumentType.objects.all())
        for t in types:
            last_check_date = start + timedelta(seconds=random.randrange(int_delta))
            for i in range(0, random.randint(10, 40)):
                serial = (random.choice(['А', 'Б', 'В', 'Г', 'В', 'Е', 'И', 'К', 'Л', 'М', 'Н', 'П', 'Р', 'C'])
                          + str(random.randint(100000, 999999)))
                holder = random.choice(jobs)
                MeasuringInstrument.objects.create(type=t, last_check_date=last_check_date, serial=serial,
                                                   holder=holder)
