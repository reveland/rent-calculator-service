import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar
from dateutil.parser import parse
from rent_reckoner.provider.provider import DataProvider

class GoogleDataProvider(DataProvider):

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('./rent_reckoner/provider/client_secret.json', scope)
        client = gspread.authorize(creds)
        self.cash_flow_sheet = client.open('Aradi').get_worksheet(2)
        self.residents_sheet = client.open('Aradi').get_worksheet(1)
        self.bills_sheet = client.open('Aradi').get_worksheet(0)

    def get_bills(self, habitant_id):
        bills =  self.bills_sheet.get_all_records()
        bills = self.__transform_date_to_int(bills)
        bills = self.__increment_end_date_with_one_day(bills)
        return bills

    def get_residents(self, habitant_id):
        residents = self.residents_sheet.get_all_records()
        residents = self.__transform_date_to_int(residents)
        residents = self.__increment_end_date_with_one_day(residents)
        return residents
    
    def get_cash_movements(self, habitant_id):
        cash_movements =  self.cash_flow_sheet.get_all_records()
        for item in cash_movements:
            item["date"] = calendar.timegm(parse(item["date"]).timetuple())
        return cash_movements

    def add_bill(self, habitant_id, start, end, type, amount, paid_by):
        self.bills_sheet.append_row([start, end, type, str(amount), paid_by])

    def add_resident(self, habitant_id, start, end, name):
        self.residents_sheet.append_row([start, end, name, '0', '0'])

    def add_cash_movement(self, habitant_id, amount, payer, receiver, date):
        self.cash_flow_sheet.append_row([amount, payer, receiver, date])

    def save_residents(self, habitant_id, residents):
        start_cell_list = self.residents_sheet.range('A2:A' + str(len(residents) + 1))
        end_cell_list = self.residents_sheet.range('B2:B' + str(len(residents) + 1))
        name_cell_list = self.residents_sheet.range('C2:C' + str(len(residents) + 1))
        dept_cell_list = self.residents_sheet.range('D2:D' + str(len(residents) + 1))
        paid_cell_list = self.residents_sheet.range('E2:E' + str(len(residents) + 1))

        for i in range(len(residents)):
            start_cell_list[i].value = residents[i]['start']
            end_cell_list[i].value = residents[i]['end']
            name_cell_list[i].value = residents[i]['name']
            dept_cell_list[i].value = str(residents[i]['dept'])
            paid_cell_list[i].value = str(residents[i]['paid'])

        self.residents_sheet.update_cells(start_cell_list)
        self.residents_sheet.update_cells(end_cell_list)
        self.residents_sheet.update_cells(name_cell_list)
        self.residents_sheet.update_cells(dept_cell_list)
        self.residents_sheet.update_cells(paid_cell_list)

    def __transform_date_to_int(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __increment_end_date_with_one_day(self, items):
        for item in items:
            item["end"] = item["end"] + 86399
        return items
