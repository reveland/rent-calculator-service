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

    def merge(self, data_provider):
        """Merge data from source DataProvider to target DataProvider
        Methode:
            - get target data provider bills
            - get source data provider bills
            - merge them
            - save the whole on target data provider"""
        