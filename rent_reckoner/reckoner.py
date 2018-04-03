import numpy as np
import datetime

class RentReckoner(object):

    def __init__(self, data_provider):
        self.data_provider = data_provider

    def get_debt(self, habitant_id, resident, residents, bills):
        sum_cost_per_skull = self.sum_cost_per_skull(
            habitant_id, resident["start"], resident["end"], residents, bills)
        sum_cost_per_skull = int(sum_cost_per_skull)

        paid = sum(map(lambda b: b['amount'], filter(lambda x: x['paid_by'] == resident['name'], bills)))

        return sum_cost_per_skull - paid

    def sum_cost(self, habitant_id, start, end, bills):
        cost = sum(list(map(lambda bill: bill["amount"] * self.get_time_coverage_percent(bill, start, end), bills)))
        return cost

    def sum_cost_per_skull(self, habitant_id, start, end, residents, bills):
        sum_per_skull = sum([self.get_cost_per_skull(habitant_id, date, residents, bills) for date in np.arange(start, end, step=86400, dtype=np.int64)])
        return sum_per_skull

    def get_cost_for_a_day(self, bill, date, count):
        percent = self.get_time_coverage_percent(bill, date, date + 86400)
        return bill["amount"] * percent / count

    def get_cost_per_skull(self, habitant_id, date, residents, bills):
        count = self.get_dweller_count(habitant_id, date, residents)
        cost = sum(list(map(lambda bill: self.get_cost_for_a_day(bill, date, count), bills)))
        return cost

    def get_dweller_count(self, habitant_id, date, residents):
        return sum(map(lambda resident: 1 if self.is_dwell(resident, date) else 0, residents))

    def is_dwell(self, resident, date):
        is_dwell = True if resident["start"] <= date <= resident["end"] else False
        return is_dwell

    def get_time_coverage_percent(self, bill, start, end):
        bill['end'] = float(bill['end'])
        bill['start'] = float(bill['start'])
        start = float(start)
        end = float(end)
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
        data = {}
        data["rows"] = []
        data["rows"].append(self.create_row("rent"))
        data["rows"].append(self.create_row("common"))
        data["rows"].append(self.create_row("inter"))
        data["rows"].append(self.create_row("elec"))
        data["rows"].append(self.create_row("gas"))
        data["rows"].append(self.create_row("water"))
        for bill in bills:
            bill_to_add = {
                "amount": bill["amount"],
                "sectionHeight": self.get_amount_per_day(bill),
                "start": bill["start"],
                "end": bill["end"]
            }
            if not bill["type"] in map(lambda type: type["name"], data["rows"]):
                data["rows"].append(self.create_row(bill["type"]))
            data["rows"][self.get_index_of_type(
                data["rows"], bill["type"])]["sections"].append(bill_to_add)

        # filter rows that not present in data
        data["rows"] = [typ for typ in data["rows"]
                        if len(typ["sections"]) != 0]

        # fill rows fields
        i = 1
        for typ in data["rows"]:
            typ["id"] = i
            typ["maxSectionHeight"] = max(
                typ["sections"], key=lambda bill: bill["sectionHeight"])["sectionHeight"]
            typ["start"] = min(typ["sections"], key=lambda bill: bill["start"])[
                "start"]
            typ["end"] = max(
                typ["sections"], key=lambda bill: bill["end"])["end"]
            i += 1

        # fill data fields
        data["sumMaxSectionHeight"] = sum(
            map(lambda type: type["maxSectionHeight"], data["rows"]))
        data["start"] = min(
            data["rows"], key=lambda type: type["start"])["start"]
        data["end"] = max(data["rows"], key=lambda type: type["end"])["end"]

        # transfor the date numbers to string
        data["start"] = self.to_iso8601(data["start"])
        data["end"] = self.to_iso8601(data["end"])
        for typ in data["rows"]:
            typ["start"] = self.to_iso8601(typ["start"])
            typ["end"] = self.to_iso8601(typ["end"])
            for bill in typ["sections"]:
                bill["start"] = self.to_iso8601(bill["start"])
                bill["end"] = self.to_iso8601(bill["end"])

        return data

    def get_residents_to_ui(self, habitant_id):
        residents = self.data_provider.get_residents(habitant_id)
        residents.sort(key=lambda x: x["start"], reverse=False)

        # add the residents
        data = {}
        data["rows"] = []
        data["rows"].append(self.create_row("Peti"))
        data["rows"].append(self.create_row("Geri"))
        data["rows"].append(self.create_row("Oliver"))
        data["rows"].append(self.create_row("Ara"))
        data["rows"].append(self.create_row("Adam"))
        for resident in residents:
            resident_to_add = {
                "amount": resident["dept"],
                "sectionHeight": 1,
                "start": resident["start"],
                "end": resident["end"]
            }
            if not resident["name"] in map(lambda row: row["name"], data["rows"]):
                data["rows"].append(self.create_row(resident["name"]))
            data["rows"][self.get_index_of_type(
                data["rows"], resident["name"])]["sections"].append(resident_to_add)

        # filter rows that not present in data
        data["rows"] = [row for row in data["rows"]
                        if len(row["sections"]) != 0]

        # fill rows sections
        i = 1
        for row in data["rows"]:
            row["id"] = i
            row["maxSectionHeight"] = max(
                row["sections"], key=lambda resident: resident["sectionHeight"])["sectionHeight"]
            row["start"] = min(row["sections"], key=lambda resident: resident["start"])[
                "start"]
            row["end"] = max(
                row["sections"], key=lambda resident: resident["end"])["end"]
            i += 1

        # fill data fields
        data["sumMaxSectionHeight"] = sum(
            map(lambda type: type["maxSectionHeight"], data["rows"]))
        data["start"] = min(
            data["rows"], key=lambda type: type["start"])["start"]
        data["end"] = max(data["rows"], key=lambda type: type["end"])["end"]

        # transfor the date numbers to string
        data["start"] = self.to_iso8601(data["start"])
        data["end"] = self.to_iso8601(data["end"])
        for row in data["rows"]:
            row["start"] = self.to_iso8601(row["start"])
            row["end"] = self.to_iso8601(row["end"])
            for resident in row["sections"]:
                resident["start"] = self.to_iso8601(resident["start"])
                resident["end"] = self.to_iso8601(resident["end"])

        return data

    def create_row(self, name):
        type_to_add = {}
        type_to_add["name"] = name
        type_to_add["sections"] = []
        return type_to_add

    def get_index_of_type(self, types, type_name):
        return next(index for (index, d) in enumerate(types) if d["name"] == type_name)

    def to_iso8601(self, date_int):
        date = datetime.datetime.fromtimestamp(date_int)
        return date.strftime("%Y-%m-%d")

    def get_amount_per_day(self, bill):
        return bill["amount"] / ((bill["end"] - bill["start"]) / 86400)

    def update_debts(self, habitant_id):
        residents_copy = self.data_provider.get_residents(habitant_id)
        residents = self.data_provider.get_residents(habitant_id)
        bills = self.data_provider.get_bills(habitant_id)
        payments = self.data_provider.get_payments(habitant_id)

        bills = list(filter(lambda b: 'paid_by' in b and b['paid_by'] != '', bills))

        for resident in residents_copy:
            resident["dept"] = self.get_debt(habitant_id, resident, residents, bills)
            resident["start"] = self.to_iso8601(resident["start"])
            resident["end"] = self.to_iso8601(resident["end"])

        for p in payments:
            for r in residents_copy:
                if r['name'] == p['from']: r['dept'] -= p['amount']
                if r['name'] == p['to']: r['dept'] += p['amount']

        self.data_provider.save_residents(habitant_id, residents_copy)
        return residents_copy

