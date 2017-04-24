import json
import calendar
from dateutil.parser import parse

class DataProvider(object):

    def __init__(self, bills_file, residents_file):
        self.bills_file = bills_file
        self.residents_file = residents_file

    def getBills(self):
        with open(self.bills_file) as data:
            bills = json.load(data)
        bills = self.__transformDateToInt(bills)
        bills = self.__incrementEndDateWithOneDay(bills)
        return bills

    def getResidents(self):
        with open(self.residents_file) as data:
            residents = json.load(data)
        residents = self.__transformDateToInt(residents)
        return residents

    def __transformDateToInt(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __incrementEndDateWithOneDay(self, items):
        for item in items:
            item["end"] = item["end"] + 86399
        return items
