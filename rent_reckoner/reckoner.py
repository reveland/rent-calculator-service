import numpy as np
import datetime


class RentReckoner(object):

    def __init__(self, data_provider):
        self.data_provider = data_provider

    def get_debt(self, resident):
        sum_cost_per_skull = self.sum_cost_per_skull(
            resident["start"], resident["end"])
        sum_cost_per_skull = int(sum_cost_per_skull)
        paid = int(resident["paid"])
        return sum_cost_per_skull - paid

    def sum_cost(self, start, end):
        return sum(list(map(lambda bill: bill["amount"] * self.get_time_coverage_percent(bill, start, end), self.data_provider.get_bills())))

    def sum_cost_per_skull(self, start, end):
        return sum([self.get_cost_per_skull(date) for date in np.arange(start, end, 86400, np.float)])

    def get_cost_per_skull(self, date):
        count = self.get_dweller_count(date)
        return sum(list(map(lambda bill: (bill["amount"] * self.get_time_coverage_percent(bill, date, date + 86400)
                                          / count), self.data_provider.get_bills())))

    def get_dweller_count(self, date):
        return sum(map(lambda resident: 1 if self.is_dwell(resident, date) else 0, self.data_provider.get_residents()))

    def is_dwell(self, resident, date):
        return True if resident["start"] <= date <= resident["end"] else False

    def get_time_coverage_percent(self, bill, start, end):
        whole_interval = bill["end"] - bill["start"]
        start_interval = start - bill["start"]
        end_interval = bill["end"] - end
        if start < bill["start"]:
            start_interval = 0
        if end > bill["end"]:
            end_interval = 0
        valuable_interval = whole_interval - start_interval - end_interval
        valuable_percent = valuable_interval / whole_interval
        if start > bill["end"]:
            valuable_percent = 0
        if end < bill["start"]:
            valuable_percent = 0
        return valuable_percent

    def get_bills_to_ui(self):
        bills = self.data_provider.get_bills()

        bills.sort(key=lambda x: x["start"], reverse=False)

        # data = {"asd": "ewe"}
        # data["values"] = []
        # data["values"].append(123)
        # data["values"].append(321)
        # print(min(data["values"]))  # 123
        # print(max(data["values"]))  # 321
        # print(data)  # {'asd': 'ewe', 'values': [123, 321]}
        # data["values"].sort(key=lambda x: x, reverse=True)
        # print(data)  # {'asd': 'ewe', 'values': [321, 123]}

        # add the bills
        data = {}
        data["types"] = []
        for bill in bills:
            bill_to_add = {
                "id": bill["id"],
                "amount": bill["amount"],
                "amountPerDay": self.get_amount_per_day(bill),
                "start": bill["start"],
                "end": bill["end"]
            }
            if not bill["type"] in map(lambda type: type["name"], data["types"]):
                type_to_add = {}
                type_to_add["name"] = bill["type"]
                type_to_add["bills"] = []
                data["types"].append(type_to_add)

            data["types"][self.get_index_of_type(data["types"], bill["type"])]["bills"].append(bill_to_add)

        # fill types fields
        i = 1
        for typ in data["types"]:
            typ["id"] = i
            typ["maxAmountPerDay"] = max(typ["bills"], key=lambda bill: bill["amountPerDay"])["amountPerDay"]
            typ["start"] = min(typ["bills"], key=lambda bill: bill["start"])["start"]
            typ["end"] = max(typ["bills"], key=lambda bill: bill["end"])["end"]
            i += 1

        # fill data fields
        data["sumMaxAmountPerDay"] = sum(
            map(lambda type: type["maxAmountPerDay"], data["types"]))
        data["start"] = min(data["types"], key=lambda type: type["start"])["start"]
        data["end"] = max(data["types"], key=lambda type: type["end"])["end"]

        # transfor the date numbers to string
        data["start"] = self.to_iso8601(data["start"])
        data["end"] = self.to_iso8601(data["end"] - 86400)
        for typ in data["types"]:
            typ["start"] = self.to_iso8601(typ["start"])
            typ["end"] = self.to_iso8601(typ["end"] - 86400)
            for bill in typ["bills"]:
                bill["start"] = self.to_iso8601(bill["start"])
                bill["end"] = self.to_iso8601(bill["end"] - 86400)

        return data

    def get_index_of_type(self, types, type_name):
        return next(index for (index, d) in enumerate(types) if d["name"] == type_name)

    def to_iso8601(self, date_int):
        date = datetime.datetime.fromtimestamp(date_int)
        return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def get_amount_per_day(self, bill):
        return bill["amount"] / ((bill["end"] - bill["start"]) / 86400)
