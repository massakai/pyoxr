# -*- coding: utf-8 -*-

"""
Open Exchange Rates API for Python
"""

import requests


class OXRClient(object):
    def __init__(self,
                 app_id,
                 api_base="https://openexchangerates.org/api/"):
        self.api_base = api_base.rstrip("/")
        self.app_id = app_id
        self.session = requests.Session()

    def get_currencies(self):
        """
        Get a JSON list of all currency symbols available from the Open
        Exchange Rates API, along with their full names.
        ref. https://oxr.readme.io/docs/currencies-json
        """
        return self.__request("currencies.json")

    def get_latest(self,
                   base=None,
                   symbols=None):
        """
        Get latest data.
        ref. https://oxr.readme.io/docs/latest-json
        """
        return self.__get_exchange_rates("latest.json", base, symbols)

    def get_historical(self,
                       date,
                       base=None,
                       symbols=None):
        """
        Get daily historical data
        ref. https://oxr.readme.io/docs/historical-json
        """
        endpoint = "historical/" + date + ".json"
        return self.__get_exchange_rates(endpoint, base, symbols)

    def get_time_series(self,
                        start,
                        end,
                        base=None,
                        symbols=None):
        """
        Get time-series data.
        ref. https://oxr.readme.io/docs/time-series-json
        """
        payload = {"start": start, "end": end}
        return self.__get_exchange_rates("time-series.json",
                                         base,
                                         symbols,
                                         payload)

    def convert(self,
                value,
                from_symbol,
                to_symbol):
        """
        Convert any money value from one currency to another at the latest
        API rates.
        ref. https://oxr.readme.io/docs/convert
        """
        endpoint = "convert/{}/{}/{}".format(value, from_symbol, to_symbol)
        payload = {"app_id": self.app_id}
        return self.__request(endpoint, payload)

    def __request(self, endpoint, payload=None):
        url = self.api_base + "/" + endpoint
        request = requests.Request("GET", url, params=payload)
        prepared = request.prepare()

        response = self.session.send(prepared)
        if response.status_code != requests.codes.ok:
            raise OXRStatusError(request, response)
        json = response.json()
        if json is None:
            raise OXRDecodeError(request, response)
        return json

    def __get_exchange_rates(self, endpoint, base, symbols, payload=None):
        if payload is None:
            payload = dict()
        payload["app_id"] = self.app_id
        if base is not None:
            payload["base"] = base
        if isinstance(symbols, list) or isinstance(symbols, tuple):
            symbols = ",".join(symbols)
        if symbols is not None:
            payload["symbols"] = symbols
        return self.__request(endpoint, payload)


class OXRError(Exception):
    """Open Exchange Rates Error"""
    def __init__(self, req, resp):
        super(OXRError, self).__init__()
        self.request = req
        self.response = resp


class OXRStatusError(OXRError):
    """API status code error"""
    pass


class OXRDecodeError(OXRError):
    """JSON decode error"""
    pass
