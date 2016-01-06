# -*- coding: utf-8 -*-
from pyoxr import OXRClient

if __name__ == "__main__":
    oxr_cli = OXRClient(app_id="XXXXXXXX")
    result = oxr_cli.get_latest()
    print(result)
