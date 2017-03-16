# Create your tests here.
from datetime import date, timedelta

from django.test import TestCase

from personnel.models import Contractor
from .models import MeasuringInstrument, MeasuringInstrumentKind, MeasuringInstrumentType
from .templatetags.items_charts import mi_operative_check_series


class OperativeCheckWidgetSeriesTestCase(TestCase):
    def setUp(self):
        self.period = 30  # days of checking perspective

        contractor_1 = Contractor.objects.create(name='Contractor 1')
        contractor_2 = Contractor.objects.create(name='Contractor 2')
        contractor_3 = Contractor.objects.create(name='Contractor 3')

        test_kind = MeasuringInstrumentKind.objects.create(name='Test kind')

        test_type_1 = MeasuringInstrumentType.objects.create(name='Test type 1', kind=test_kind,
                                                             checking_organization=contractor_1)
        test_type_2 = MeasuringInstrumentType.objects.create(name='Test type 2', kind=test_kind,
                                                             checking_organization=contractor_2)
        test_type_3 = MeasuringInstrumentType.objects.create(name='Test type 3', kind=test_kind,
                                                             checking_organization=contractor_2)
        test_type_4 = MeasuringInstrumentType.objects.create(name='Test type 4', kind=test_kind,
                                                             checking_organization=contractor_3)

        self.instrument_prestart = MeasuringInstrument.objects.create(type=test_type_1,
                                                                 last_check_date=date.today() - timedelta(days=1))
        self.instrument_start = MeasuringInstrument.objects.create(type=test_type_2,
                                                              last_check_date=date.today())
        self.instrument_poststart = MeasuringInstrument.objects.create(type=test_type_2,
                                                                  last_check_date=date.today() + timedelta(days=1))

        self.instrument_prestop = MeasuringInstrument.objects.create(type=test_type_3,
                                                                last_check_date=date.today() - timedelta(
                                                                    days=1) + timedelta(days=self.period))
        self.instrument_stop = MeasuringInstrument.objects.create(type=test_type_4,
                                                             last_check_date=date.today() + timedelta(days=self.period))
        self.instrument_poststop = MeasuringInstrument.objects.create(type=test_type_1,
                                                                 last_check_date=date.today() + timedelta(
                                                                     days=1) + timedelta(days=self.period))

    def test_mi_operative_check_series(self):
        """Animals that can speak are correctly identified"""
        res = mi_operative_check_series()
