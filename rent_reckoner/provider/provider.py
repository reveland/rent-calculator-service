from abc import ABC, abstractmethod

class DataProvider(ABC):

    @abstractmethod
    def get_bills(self, habitant_id):
        pass

    @abstractmethod
    def get_residents(self, habitant_id):
        pass

    @abstractmethod
    def save_residents(self, habitant_id, residents):
        pass

    @abstractmethod
    def add_resident(self, habitant_id, start, end, name):
        pass

    @abstractmethod
    def add_bill(self, habitant_id, start, end, type, amount):
        pass
