import calendar
from dateutil.parser import parse
from trello import TrelloClient
from rent_reckoner.provider.provider import DataProvider

class TrelloDataProvider(DataProvider):

    def __init__(self):
        client = TrelloClient(
            api_key='4c48eb6acff05f1a7105b93ed58e912b',
            api_secret='7196c21a9f0a7a8656bf802b9af2e1cbae447fc30d5ccd64868836cf4d14e74f',
            token='6bbb65aab16eada17f8137017b695dd0b61f463b5b77ce98ff7f25c8ecabd71f',
            token_secret='7196c21a9f0a7a8656bf802b9af2e1cbae447fc30d5ccd64868836cf4d14e74f'
        )
        self.board = client.get_board('f0EDhQy7')

    def get_bills(self, habitant_id):
        bills_cards = self.board.open_lists()[4].list_cards()
        bills_splitted = self.__split_them(bills_cards)
        bills = self.__dict_them(bills_splitted, ['start', 'end', 'type', 'amount', 'paid_by'])
        for item in bills:
            item["amount"] = float(item["amount"])
        bills = self.__transform_date_to_int(bills)
        bills = self.__increment_end_date_with_one_day(bills)
        return bills

    def get_residents(self, habitant_id):
        residents_cards = self.board.open_lists()[3].list_cards()
        residents_splitted = self.__split_them(residents_cards)
        residents = self.__dict_them(residents_splitted, ['start', 'end', 'name', 'dept', 'paid'])
        for item in residents:
            item["dept"] = float(item["dept"])
            item["paid"] = float(item["paid"])
        residents = self.__transform_date_to_int(residents)
        return residents

    def save_residents(self, habitant_id, residents):
        cards = self.board.open_lists()[3].list_cards()
        for i in range(len(residents)):
            row = residents[i]
            cards[i].set_name(' '.join([row['start'], row['end'], row['name'], str(row['dept']), str(row['paid'])]))

    def add_bill(self, habitant_id, start, end, type, amount, paid_by):
        self.board.open_lists()[4].add_card(start + ' ' + end + ' ' + type + ' ' + str(amount) + ' ' + paid_by)

    def add_resident(self, habitant_id, start, end, name):
        self.board.open_lists()[3].add_card(start + ' ' + end + ' ' + name + ' 0 0')

    def __transform_date_to_int(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __increment_end_date_with_one_day(self, items):
        for item in items:
            item["end"] = item["end"] + 86400
        return items

    def __dict_them(self, l, keys):
        return list(map(lambda r: dict(zip(keys, r)), l))

    def __split_them(self, l):
        return list(map(lambda r: str(r).replace('<', '').replace('>', '').split(' ')[1:], l))
