from abc import ABC, abstractmethod
import datetime

class DataProvider(ABC):

    @abstractmethod
    def get_bills(self, habitant_id):
        pass

    @abstractmethod
    def get_residents(self, habitant_id):
        pass
    
    @abstractmethod
    def get_cash_movements(self, habitant_id):
        pass

    @abstractmethod
    def add_resident(self, habitant_id, start, end, name):
        pass

    @abstractmethod
    def add_bill(self, habitant_id, start, end, type, amount, paid_by):
        pass

    @abstractmethod
    def add_cash_movement(self, habitant_id, amount, payer, receiver, date):
        pass

    @abstractmethod
    def save_residents(self, habitant_id, residents):
        pass

    def merge(self, habitant_id, target_data_provider):
        """Merge data from source DataProvider to target DataProvider"""
        source_data = self.get_bills(habitant_id)
        target_data = target_data_provider.get_bills(habitant_id)

        for bill in source_data:
            bill["start"] = self.to_iso8601(bill["start"])
            bill["end"] = self.to_iso8601(bill["end"])

        for bill in target_data:
            bill["start"] = self.to_iso8601(bill["start"])
            bill["end"] = self.to_iso8601(bill["end"])

        result_bills = []
        for bill in source_data:
            if bill not in target_data and 'amount' in bill:
                result_bills.append(bill)
        
        for bill in result_bills:
            target_data_provider.add_bill(habitant_id, bill['start'], bill['end'], bill['type'], bill['amount'], bill['paid_by'])
        return result_bills
    
    def to_iso8601(self, date_int):
        date = datetime.datetime.fromtimestamp(date_int)
        return date.strftime("%Y-%m-%d")
