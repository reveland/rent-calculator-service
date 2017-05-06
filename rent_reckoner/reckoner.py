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
        print(bills)

        sum_per_day = 80000 / 31
        result = {
            "start": "2017-01-01T00:00:00.000Z",
            "end": "2017-01-31T00:00:00.000Z",
            "sumMaxAmountPerDay": sum_per_day,
            "types": [{
                "id": 1,
                "start": "2017-01-01T00:00:00.000Z",
                "end": "2017-01-31T00:00:00.000Z",
                "maxAmountPerDay": sum_per_day,
                "name": "rent",
                "bills": [{
                    "id": 1,
                    "amount": 80000,
                    "amountPerDay": sum_per_day,
                    "start": "2017-01-01T00:00:00.000Z",
                    "end": "2017-01-31T00:00:00.000Z"
                }]
            }]
        }

        return result

    def to_iso8601(self, date_int):
        date = datetime.datetime.fromtimestamp(date_int)
        return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def get_amount_per_day(self, bill):
        return bill["amount"] / ((bill["end"] - bill["start"]) / 86400)
