from unittest import TestCase
from CrmRequest import CrmRequest
from exceptions import ElementNotFoundError
from datetime import datetime, date


class TestCRMRequest(TestCase):
    def setUp(self) -> None:
        self.req = CrmRequest()


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
        self.req.get_dates('Османов Ильяс Нариманович')

    def test_get_dates_wrong_name(self):
        try:
            self.req.get_dates('aboba')

        except ElementNotFoundError:
            pass


class TestGetTimes(TestCRMRequest):
    def test_get_times(self):
        try:
            self.req.get_times(datetime.now(), 'Османов Ильяс Нариманович')

        except ElementNotFoundError:
            pass

    def test_get_times_wrong_name(self):
        try:
            self.req.get_times(datetime.now(), 'aboba')

        except ElementNotFoundError:
            pass

    def test_get_times_too_old_date(self):
        try:
            self.req.get_times(datetime(1900, 1, 1), 'Османов Ильяс Нариманович')

        except ElementNotFoundError:
            pass

    def test_get_times_far_future_date(self):
        try:
            self.req.get_times(datetime(2100, 1, 1), 'Османов Ильяс Нариманович')

        except ElementNotFoundError:
            pass

    def test_get_times_wrong_type(self):
        try:
            self.req.get_times('aboba', 'Османов Ильяс Нариманович')

        except ElementNotFoundError:
            pass

    def test_get_times_date_not_datetime(self):
        try:
            self.req.get_times(date.today(), 'Османов Ильяс Нариманович')

        except ElementNotFoundError:
            pass


class TestPostDataCollector(TestCRMRequest):
    def test_post_data_collector(self):
        self.req.post_data_collector('Иванов Иван Иванович', '+7(904)243-23-43', 'Позвони мне',
                                     'Османов Ильяс Нариманович',
                                     'Консультация врача-ортодонта кандидата медицинских наук',
                                     datetime.now(),
                                     datetime.now())

    def test_post_data_collector_not_formated_number(self):
        phone_numbers = ['79067288438', '+79067288438', '9067288438', '+7(906)7288438', '+7(906)728-84-38',
                         '+7906728-84-38']
        for phone_number in phone_numbers:
            self.req.post_data_collector('Иванов Иван Иванович', phone_number, 'Позвони мне',
                                         'Османов Ильяс Нариманович',
                                         'Консультация врача-ортодонта кандидата медицинских наук',
                                         datetime.now(),
                                         datetime.now())
