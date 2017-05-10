import os
import json
import calendar
from dateutil.parser import parse


class DataProvider(object):

    def __init__(self, path):
        self.habitation_files = {}
        for filename in os.listdir(path):
            if filename.startswith("habitation_"):
                file = path + "/" + filename
                with open(file) as habitant:
                    habitant_id = json.load(habitant)["id"]
                    self.habitation_files[habitant_id] = file

    def get_bills(self, habitant_id):
        with open(self.habitation_files[habitant_id]) as data:
            bills = json.load(data)["bills"]
        bills = self.__transform_date_to_int(bills)
        bills = self.__increment_end_date_with_one_day(bills)
        return bills

    def get_residents(self, habitant_id):
        with open(self.habitation_files[habitant_id]) as data:
            residents = json.load(data)["residents"]
        residents = self.__transform_date_to_int(residents)
        return residents

    def get_resident_by_id(self, habitant_id, resident_id):
        with open(self.habitation_files[habitant_id]) as data:
            residents = json.load(data)["residents"]
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
