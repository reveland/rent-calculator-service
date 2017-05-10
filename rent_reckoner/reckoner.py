import numpy as np
import datetime


class RentReckoner(object):

    def __init__(self, data_provider):
        self.data_provider = data_provider

    def get_debt(self, habitant_id, resident):
        sum_cost_per_skull = self.sum_cost_per_skull(
            habitant_id, resident["start"], resident["end"])
        sum_cost_per_skull = int(sum_cost_per_skull)
        paid = int(resident["paid"])
        return sum_cost_per_skull - paid

    def sum_cost(self, habitant_id, start, end):
        return sum(list(map(lambda bill: bill["amount"] * self.get_time_coverage_percent(bill, start, end), self.data_provider.get_bills(habitant_id))))

    def sum_cost_per_skull(self, habitant_id, start, end):
        return sum([self.get_cost_per_skull(habitant_id, date) for date in np.arange(start, end, 86400, np.float)])

    def get_cost_per_skull(self, habitant_id, date):
        count = self.get_dweller_count(habitant_id, date)
        return sum(list(map(lambda bill: (bill["amount"] * self.get_time_coverage_percent(bill, date, date + 86400)
                                          / count), self.data_provider.get_bills(habitant_id))))

    def get_dweller_count(self, habitant_id, date):
        return sum(map(lambda resident: 1 if self.is_dwell(resident, date) else 0, self.data_provider.get_residents(habitant_id)))

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

    def get_bills_to_ui(self, habitant_id):
        bills = self.data_provider.get_bills(habitant_id)
        bills.sort(key=lambda x: x["start"], reverse=False)

        # add the bills
        i = 1
        data = {}
        data["types"] = []
        data["types"].append(self.create_type("rent"))
        data["types"].append(self.create_type("common"))
        data["types"].append(self.create_type("inter"))
        data["types"].append(self.create_type("elec"))
        data["types"].append(self.create_type("gas"))
        data["types"].append(self.create_type("water"))
        for bill in bills:
            bill_to_add = {
                "id": i,
                "amount": bill["amount"],
                "amountPerDay": self.get_amount_per_day(bill),
                "start": bill["start"],
                "end": bill["end"]
            }
            if not bill["type"] in map(lambda type: type["name"], data["types"]):
                data["types"].append(self.create_type(bill["type"]))
            data["types"][self.get_index_of_type(
                data["types"], bill["type"])]["bills"].append(bill_to_add)
            i += 1

        # filter types that not present in data
        data["types"] = [typ for typ in data["types"]
                         if len(typ["bills"]) != 0]

        # fill types fields
        i = 1
        for typ in data["types"]:
            typ["id"] = i
            typ["maxAmountPerDay"] = max(
                typ["bills"], key=lambda bill: bill["amountPerDay"])["amountPerDay"]
            typ["start"] = min(typ["bills"], key=lambda bill: bill["start"])[
                "start"]
            typ["end"] = max(typ["bills"], key=lambda bill: bill["end"])["end"]
            i += 1

        # fill data fields
        data["sumMaxAmountPerDay"] = sum(
            map(lambda type: type["maxAmountPerDay"], data["types"]))
        data["start"] = min(
            data["types"], key=lambda type: type["start"])["start"]
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

    def create_type(self, name):
        type_to_add = {}
        type_to_add["name"] = name
        type_to_add["bills"] = []
        return type_to_add

    def get_index_of_type(self, types, type_name):
        return next(index for (index, d) in enumerate(types) if d["name"] == type_name)

    def to_iso8601(self, date_int):
        date = datetime.datetime.fromtimestamp(date_int)
        return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def get_amount_per_day(self, bill):
        return bill["amount"] / ((bill["end"] - bill["start"]) / 86400)
