import calendar
from dateutil.parser import parse
from splitwise import Splitwise
from rent_reckoner.provider.provider import DataProvider
import re
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from splitwise.category import Category
from functools import reduce
from datetime import datetime
from dateutil import parser

class SplitwiseDataProvider(DataProvider):

    def __init__(self):
        api_key = 'GrsqkubjdaoTlyCGAeZbFQZMZHZx5tnKvtaxeuea'
        api_secret = '3zgKW7CWurwhlM8jAWQWJBoDeegCMgE7ebNatlZ2'
        self.p = re.compile('[^0-9][0-1][0-9]\.[0-3][0-9]')
        self.sw = Splitwise(api_key,api_secret)
        self.categories_of_interest = None
        self.aradi = None
        self.secret = None

    def get_auth_url(self):
        url, self.secret = self.sw.getAuthorizeURL()
        return url
        
    def auth(self, oauth_token, oauth_verifier):
        access_token = self.sw.getAccessToken(oauth_token, self.secret, oauth_verifier)
        self.sw.setAccessToken(access_token)
        self.categories_of_interest = self.get_categories_of_interest()
        self.aradi = self.get_group_by_name('Aradi')

    def get_bills(self, group):
        expenses = self.sw.getExpenses()
        bills = list(filter(lambda e: self.expense_in_interest(e, group), expenses))
        bills = list(map(self.map_bill, bills))
        bills = self.__transform_date_to_int(bills)
        return bills

    def get_residents(self, habitant_id):
        pass

    def add_bill(self, habitant_id, start, end, type, amount, paid_by):
        pass

    def add_resident(self, habitant_id, start, end, name):
        pass

    def save_residents(self, habitant_id, residents):
        pass

    def get_group_by_name(self, name):
        groups = self.sw.getGroups()
        return list(filter(lambda group: group.name == name, groups))[0]

    def get_categories_of_interest(self):
        categories_of_interest = filter(lambda c: c.name == 'Home' or c.name == 'Utilities', self.sw.getCategories())
        categories_subcategories = map(lambda c: c.subcategories, categories_of_interest)
        subcategories = reduce(list.__add__, categories_subcategories)
        subcategories_names = map(lambda sc: sc.name, subcategories)
        subcategories_names = filter(lambda sc: sc != 'Other', subcategories_names)
        return list(subcategories_names)

    def expense_in_interest(self, e, group):
        return e.deleted_at == None and e.group_id == self.aradi.id and e.category.name in self.categories_of_interest
    
    def string_to_mounth_number(self, string):
        m = {'jan': 1, 'feb': 2, 'mar': 3, 'apr':4,
            'may':5, 'jun':6, 'jul':7, 'aug':8,
            'sep':9, 'oct':10, 'nov':11, 'dec':12}
        try:
            s = string.strip()[:3].lower()
            return m[s]
        except:
            if len(string) < 3:
                return None
            else:
                return self.string_to_mounth_number(string[1:])

    def get_month_number(self, b):
        month = self.string_to_mounth_number(b.description)
        if not month:
            month = b.getDate()[5:7]
        return int(month)

    def get_overlapped_start_end(self, date, found):
            month = date.month
            sm = int(found[0][0:2])
            sd = int(found[0][3:5])
            em = int(found[1][0:2])
            ed = int(found[1][3:5])
            if month < 6:
                if sm > 6:
                    start = datetime(date.year - 1, sm, sd)
                else:
                    start = datetime(date.year, sm, sd)
                if int(found[1][0:2]) > 6:
                    end = datetime(date.year - 1, em, ed)
                else:
                    end = datetime(date.year, em, ed)
            else:
                start = datetime(date.year, sm, sd)
                end = datetime(date.year, em, ed)
            return {'start': start, 'end': end}

    def get_overlapped_start_end_month(self, date, my_month):
            month = date.month
            if month < 6:
                if my_month > 6:
                    start = datetime(date.year - 1, my_month, 1)
                else:
                    start = datetime(date.year, my_month, 1)
                if my_month > 6:
                    _, last_day = calendar.monthrange(date.year - 1, my_month)
                    end = datetime(date.year - 1, my_month, last_day)
                else:
                    _, last_day = calendar.monthrange(date.year, my_month)
                    end = datetime(date.year, my_month, last_day)
            else:
                _, last_day = calendar.monthrange(date.year, my_month)
                start = datetime(date.year, my_month, 1)
                end = datetime(date.year, my_month, last_day)
            return {'start': start, 'end': end}
    p = re.compile('[^0-9][0-1][0-9]\.[0-3][0-9]')

    def get_start_end(self, b):
        date = parser.parse(b.getDate()[:11])
        found = list(map(lambda x: x[1:], self.p.findall('b' + b.description)))
        if len(found) >= 2:
            return self.get_overlapped_start_end(date, found)
        else:
            month = self.get_month_number(b)
            return self.get_overlapped_start_end_month(date, month)

    def get_paid_by(self, b):
        return list(filter(lambda u: float(u.paid_share) > 0, b.users))[0].getFirstName()

    def map_bill(self, b):
        start_end = self.get_start_end(b)
        amount = int(float(b.cost))
        start = start_end['start'].strftime('%Y-%m-%d')
        end = start_end['end'].strftime('%Y-%m-%d')
        type = b.category.name
        paid_by = self.get_paid_by(b)
        return {"amount": amount, "start": start, "end": end, "type": type, "paid_by": paid_by}

    def __transform_date_to_int(self, items):
        for item in items:
            item["end"] = calendar.timegm(parse(item["end"]).timetuple())
            item["start"] = calendar.timegm(parse(item["start"]).timetuple())
        return items

    def __increment_end_date_with_one_day(self, items):
        for item in items:
            item["end"] = item["end"] + 86400
        return items
