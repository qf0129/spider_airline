import json
from collections import OrderedDict

SUI_XIN_FEI_COMPANY = ['MU', 'FM']  # 随心飞仅支持东航、上航


class DataParser(object):

    def __init__(self, json_str:str):
        json_data = json.loads(json_str)
        self._flight_list = json_data['flightInfo']
        self._ticket_list = json_data['searchProduct']
        self.flights = OrderedDict()

    def get_flights(self):
        self._parse_flights()
        self._parse_tickets()
        return self.flights

    def _parse_flights(self):

        for flight_info in self._flight_list:
            index_str = 'idx_%s' % flight_info['index']
            is_suixinfei = False
            if flight_info['marketingAirline']['code'] in SUI_XIN_FEI_COMPANY and flight_info['marketingAirline']['code'] in SUI_XIN_FEI_COMPANY:
                is_suixinfei = True

            self.flights[index_str] = {
                'code': flight_info['flightNo'],
                'is_share': flight_info['isCodeShareAirline'],
                'marketing_airline': flight_info['marketingAirline']['codeContext'],
                'operating_airline': flight_info['operatingAirline']['codeContext'],
                'start_time': flight_info['departDateTime'],
                'has_economy': False,
                'is_suixinfei': is_suixinfei,
                'tickets': [],
            }


    def _parse_tickets(self):
        for ticket in self._ticket_list:
            index_str = 'idx_%s' % ticket['productGroupIndex']
            flight = self.flights[index_str]

            if index_str in self.flights:
                if ticket['cabin']['baseCabinCode'] == "economy":
                    flight['has_economy'] = True
                flight['tickets'].append({
                    'type': ticket['cabin']['baseCabinCode'],
                    'count': ticket['cabin']['cabinStatus'],
                    'price': ticket['salePrice'],
                })


ret = DataParser(json_str).get_flights()
print('code\tis_share\thas_economy')
for i, data in ret.items():
    # print('{}\t{}\t{}\t{}'.format(
    #     data['code'],
    #     data['is_share'],
    #     data['has_economy'],
    #     data['is_suixinfei']
    # )
    print(data)
