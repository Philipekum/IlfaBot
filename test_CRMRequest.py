from unittest import TestCase, skip
from CRMRequest import CRMRequest, ElementNotFoundError
from datetime import datetime, date


class TestCRMRequest(TestCase):
    def setUp(self) -> None:
        self.req = CRMRequest()


class TestGetCategories(TestCRMRequest):
    def test_get_categories(self):
        self.req.get_categories()


class TestGetServices(TestCRMRequest):
    def test_get_all_services(self):
        self.req.get_services()

    def test_get_service(self):
        self.req.get_services('Хирургия')

    def test_get_service_wrong_name(self):
        try:
            self.req.get_services('aboba')

        except ElementNotFoundError:
            pass


class TestGetEmployees(TestCRMRequest):
    def test_get_all_employees(self):
        self.req.get_employees()

    def test_get_employee(self):
        self.req.get_employees('Консультация врача-ортодонта кандидата медицинских наук')

    def test_get_employee_wrong_name(self):
        try:
            self.req.get_employees('aboba')

        except ElementNotFoundError:
            pass


class TestGetDates(TestCRMRequest):
    def test_get_dates(self):
        self.req.get_raw_dates('Османов Ильяс Нариманович')

    def test_get_dates_wrong_name(self):
        try:
            self.req.get_raw_dates('aboba')

        except ElementNotFoundError:
            pass


class TestGetTimes(TestCRMRequest):
    def test_get_times(self):
        self.req.get_times(datetime.now(), 'Османов Ильяс Нариманович')

    def test_get_times_wrong_name(self):
        try:
            self.req.get_times(datetime.now(), 'aboba')

        except ElementNotFoundError:
            pass

    @skip('Нужно сделать проверку в теле get_times на то, что все таки дата свободна')
    def test_get_times_too_old_date(self):
        try:
            self.req.get_times(datetime(1900, 1, 1), 'Османов Ильяс Нариманович')

        except ElementNotFoundError:
            pass

    @skip('Нужно сделать проверку в теле get_times на то, что все таки дата свободна')
    def test_get_times_far_future_date(self):
        self.req.get_times(datetime(2100, 1, 1), 'Османов Ильяс Нариманович')

    @skip('Подозреваю то же самое')
    def test_get_times_wrong_type(self):
        self.req.get_times('aboba', 'Османов Ильяс Нариманович')

    @skip('Проверь точно ли можно доверять datetime.combine')
    def test_get_times_date_not_datetime(self):
        self.req.get_times(date.today(), 'Османов Ильяс Нариманович')
