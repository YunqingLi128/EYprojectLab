import itertools
import os
import requests
import urllib3
from flask import current_app
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_csv(report, RSSD_ID, date):
    base_url = "https://www.ffiec.gov/npw/FinancialReport/ReturnFinancialReportCSV?rpt={}&id={}&dt={}"
    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    dir_name = os.path.join(path, "data", RSSD_ID)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    try:
        csv_url = base_url.format(report, RSSD_ID, date)
        # print(csv_url)
        csv_file_name = "_".join([report, RSSD_ID, date]) + ".csv"
        csv_file_path = os.path.join(dir_name, csv_file_name)
        if not os.path.exists(csv_file_path):
            response = requests.get(url=csv_url, verify=False)
            if response.status_code == 200 and "<body>" not in response.text:
                with open(csv_file_path, "wb") as f:
                    f.write(response.content)
    except Exception as e:
        print(e)


def init_data():
    # TODO: Store institution_list into the config file
    institution_list = ["1073757"]
    current_year = datetime.now().year
    years = range(2015, current_year)
    quarters = ["0331", "0630", "0930", "1231"]
    dates = []
    for r in itertools.product(years, quarters):
        dates.append(str(r[0]) + r[1])
    report = "FFIEC102"
    for institution in institution_list:
        for date in dates:
            download_csv(report, institution, date)

