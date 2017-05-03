import json
import calendar
from dateutil.parser import parse


class DataProvider(object):

    def __init__(self, bills_file, residents_file):
        self.bills_file = bills_file
        self.residents_file = residents_file

    def get_bills(self):
        with open(self.bills_file) as data:
            bills = json.load(data)
        bills = self.__transform_date_to_int(bills)
        bills = self.__increment_end_date_with_one_day(bills)
        return bills

    def get_residents(self):
        with open(self.residents_file) as data:
            residents = json.load(data)
        residents = self.__transform_date_to_int(residents)
        return residents

    def get_resident_by_id(self, resident_id):
        with open(self.residents_file) as data:
            residents = json.load(data)
        residents = self.__transform_date_to_int(residents)
        return next(resident for resident in residents if resident["id"] == resident_id)

    def __transform_date_to_int(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __increment_end_date_with_one_day(self, items):
        for item in items:
            item["end"] = item["end"] + 86400
        return items
