from abc import ABC, abstractmethod

class DataProvider(ABC):

    @abstractmethod
    def get_bills(self, habitant_id):
        pass

    @abstractmethod
    def get_residents(self, habitant_id):
        pass

    @abstractmethod
    def add_resident(self, habitant_id, start, end, name):
        pass

    @abstractmethod
    def add_bill(self, habitant_id, start, end, type, amount):
        pass

    @abstractmethod
    def save_residents(self, habitant_id, residents):
        pass

    @abstractmethod
    def save_bills(self, habitant_id, bills):
        pass

    def merge(self, habitant_id, target_data_provider):
        """Merge data from source DataProvider to target DataProvider
        Methode:
            - get target data provider bills
            - get source data provider bills
            - merge them
            - save the whole on target data provider"""
        source_data = self.get_bills(habitant_id)
        target_data = target_data_provider.get_bills(habitant_id)

        result_bills = []
        target_data.extend(source_data)
        for bill in target_data:
            if bill not in result_bills:
                result_bills.append(bill)

        target_data_provider.save_bills(habitant_id, result_bills)
        return result_bills
