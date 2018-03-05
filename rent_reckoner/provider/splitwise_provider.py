import calendar
from dateutil.parser import parse
from rent_reckoner.provider.provider import DataProvider

class SplitwiseDataProvider(DataProvider):

    def __init__(self):
        api_key = 'GrsqkubjdaoTlyCGAeZbFQZMZHZx5tnKvtaxeuea'
        api_secret = '3zgKW7CWurwhlM8jAWQWJBoDeegCMgE7ebNatlZ2'
        self.sw = Splitwise(api_key,api_secret)

    def get_auth_url():
        url, self.secret = sw.getAuthorizeURL()
        return url
        
    def auth(oauth_token, oauth_verifier):
        access_token = sw.getAccessToken(oauth_token, self.secret, oauth_verifier)
        self.sw.setAccessToken(access_token)

    def get_bills(self, habitant_id):
        bills =  self.bills_sheet.get_all_records()
        bills = self.__transform_date_to_int(bills)
        bills = self.__increment_end_date_with_one_day(bills)
        return bills

    def get_residents(self, habitant_id):
        pass

    def add_bill(self, habitant_id, start, end, type, amount, paid_by):
        pass

    def add_resident(self, habitant_id, start, end, name):
        pass

    def save_residents(self, habitant_id, residents):
        pass

    def 

    def __transform_date_to_int(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __increment_end_date_with_one_day(self, items):
        for item in items:
            item["end"] = item["end"] + 86400
        return items
