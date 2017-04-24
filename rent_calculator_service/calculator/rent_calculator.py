import numpy as np
from rent_calculator_service.data_access.data_provider import DataProvider

class RentCalculator(object):

    def __init__(self, dataProvider):
        self.dp = dataProvider

    def getDebt(self, resident):
        return self.sumCostPerSkull(resident["start"], resident["end"]) - resident["paid"]

    def sumCost(self, start, end):
        return sum(list(map(lambda bill: bill["amount"] * self.getTimeCoveragePercent(bill, start, end), self.dp.getBills())))

    def sumCostPerSkull(self, start, end):
        return sum(list(map(lambda date: self.getCostPerSkull(date), np.arange(start, end, 86400))))

    def getCostPerSkull(self, date):
        count = self.getDwellerCount(date);
        return sum(list(map(lambda bill: (bill["amount"] * self.getTimeCoveragePercent(bill, date, date + 86400) / count), self.dp.getBills() )))

    def getDwellerCount(self, date):
        return sum(map(lambda resident: 1 if self.isDwell(resident, date) else 0, self.dp.getResidents()))

    def isDwell(self, resident, date):
        return True if resident["start"] <= date <= resident["end"] else False

    def getTimeCoveragePercent(self, bill, start, end):
        wholeInterval = bill["end"] - bill["start"]
        startInterval = start - bill["start"]
        endInterval = bill["end"] - end
        if start < bill["start"]: startInterval = 0
        if end > bill["end"]: endInterval = 0
        valuableInterval = wholeInterval - startInterval - endInterval
        valuablePercent = valuableInterval / wholeInterval
        if start > bill["end"]: valuablePercent = 0
        if end < bill["start"]: valuablePercent = 0
        return valuablePercent
