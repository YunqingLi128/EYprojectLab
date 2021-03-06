import itertools
import os
import requests
import urllib3
import json
import pandas as pd
from flask import current_app
from datetime import datetime
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_cur_path():
    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    return path


def create_dir(path, name):
    dir_name = os.path.join(path, name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def download_csv(path, report, RSSD_ID, date):
    csv_file_name = "_".join([report, RSSD_ID, date]) + ".csv"
    csv_file_path = os.path.join(path, csv_file_name)
    # Assuming the published reports will not be updated
    if os.path.exists(csv_file_path):  # TODO: What if reports may be updated?
        return None

    base_url = "https://www.ffiec.gov/npw/FinancialReport/ReturnFinancialReportCSV?rpt={}&id={}&dt={}"
    csv_url = base_url.format(report, RSSD_ID, date)
    try:
        if not os.path.exists(csv_file_path):
            response = requests.get(url=csv_url, verify=False)
            if response.status_code == 200 and "<body>" not in response.text:
                logging.info("%s is downloaded", csv_file_name)
                with open(csv_file_path, "wb") as f:
                    f.write(response.content)
                return csv_file_path
        return None
    except Exception as e:
        print(e)


def format_date(date):
    quarter_map = {"0331": "Q1", "0630": "Q2", "0930": "Q3", "1231": "Q4"}
    year, day = date[:4], date[4:]
    quarter_date = year + quarter_map[day]
    return quarter_date


def parse_csv_path(csv_path):
    _, csv_name = os.path.split(csv_path)
    report, institution, date = csv_name.split(".")[0].split("_")
    return report, institution, date


def raw_csv_consolidation(report, csv_path):
    report, institution, date = parse_csv_path(csv_path)
    date = format_date(date)
    df = pd.read_csv(csv_path, header=0)
    item_prefix = {"FFIEC102": "M", "FRY9C": "B"}  # drop the rows which ItemName is not "M*" or "B*"
    index_names = df[~df["ItemName"].str.startswith(item_prefix[report])].index
    df.drop(index_names, inplace=True)
    df["Institution"] = institution
    df["Date"] = date
    df.drop("Description", axis=1, inplace=True)  # drop the Description
    df = df[["Institution", "Date", "ItemName", "Value"]]  # change the order
    return df


def init_data(update_everytime):
    # TODO: Store institution_list into the config file
    current_year = datetime.now().year
    years = range(2015, current_year + 1)
    quarters = ["0331", "0630", "0930", "1231"]
    all_dates = []
    for r in itertools.product(years, quarters):
        all_dates.append(str(r[0]) + r[1])

    # create data folder
    path = get_cur_path()
    create_dir(path, "data/raw_data")

    # load the data config file
    json_file_path = os.path.join(path, "data_setting.json")
    with open(json_file_path, 'r') as f:
        data_info = json.loads(f.read())
    report = data_info["report"]
    institution_list = data_info["institutions"]

    df_list = []
    for institution_obj in institution_list:
        if "end_date" not in institution_obj:
            dates = all_dates
            start_date = all_dates[0]
            end_date = all_dates[-1]
        else:
            if not update_everytime:
                continue
            dates = list(filter(lambda x: x > institution_obj["end_date"], all_dates))
            start_date = institution_obj["start_date"]
            end_date = institution_obj["end_date"]
        for i in range(len(dates)):
            csv_file_path = download_csv(path, report, institution_obj["RSSD_ID"], dates[i])
            if csv_file_path is not None:
                end_date = dates[i]
                df = raw_csv_consolidation("", csv_file_path)
                df_list.append(df)
        institution_obj["start_date"] = start_date
        institution_obj["end_date"] = end_date

    if len(df_list) > 0:
        full_df = pd.concat(df_list)
        full_csv_path = os.path.join(get_cur_path(), "data", report + ".csv")
        full_df.to_csv(full_csv_path, mode='a', header=False, index=False)

    with open(json_file_path, 'w') as f:
        json.dump(data_info, f, indent=4)


# TODO: multiple thread handling
def download_csv_for_institution(path, rssd_id, reports, dates):
    """
    :param path: Institution folder path
    :param rssd_id: Institution RSSD ID
    :param reports: Report list
    :param dates: Dates need to be downloaded
    :return: {report_name_1: file_path_list, report_name_2: file_path_list}
    """
    res = {}
    for report in reports:
        file_list = []
        for date in dates:
            file_path = download_csv(path, report, rssd_id, date)
            if file_path is not None:
                file_list.append(file_path)
        res[report] = file_list
    return res


def download_raw_csv_files():
    """
    Downloading raw csv files for institutions in the data_setting.json

    :return: Downloaded csv paths for each report
    """
    current_year = datetime.now().year
    current_date = datetime.now().strftime('%m%d')
    years = range(2015, current_year)
    quarters = ["0331", "0630", "0930", "1231"]
    all_dates = []
    for r in itertools.product(years, quarters):
        all_dates.append(str(r[0]) + r[1])
    for q in quarters:
        if q < current_date:
            all_dates.append(str(current_year) + q)
    logging.info("dates %s", all_dates)

    # create data folder
    path = get_cur_path()
    data_dir_path = create_dir(path, "data/raw_data")

    # load the data config file
    json_file_path = os.path.join(path, "data_setting.json")
    with open(json_file_path, 'r') as f:
        data_info = json.loads(f.read())
    reports = data_info["reports"]
    institutions = data_info["institutions"]

    file_info = {report: [] for report in reports}
    for rssd_id in institutions:
        institution = institutions[rssd_id]
        institution_dir_path = create_dir(data_dir_path, rssd_id)
        res = download_csv_for_institution(institution_dir_path, rssd_id, reports, all_dates)
        for report in reports:
            file_list = res[report]
            if report not in institution:
                institution[report] = {}
            if len(file_list) > 0:
                _, _, start_date = parse_csv_path(file_list[0])
                _, _, end_date = parse_csv_path(file_list[-1])
                institution[report]["start_date"] = start_date
                institution[report]["end_date"] = end_date
            file_info[report].extend(file_list)

    with open(json_file_path, 'w') as f:
        json.dump(data_info, f, indent=4)
    return file_info


def walk_through_files(file_info):
    """
    Raw csv consolidation for downloaded csv files

    :param file_info: dict(): Downloaded csv paths for each report
    :return: None
    """
    for report in file_info:
        df_list = []
        for csv_file_path in file_info[report]:
            df = raw_csv_consolidation(report, csv_file_path)
            df_list.append(df)

        if len(df_list) > 0:
            full_df = pd.concat(df_list)
            full_csv_path = os.path.join(get_cur_path(), "data", report + ".csv")
            full_df.to_csv(full_csv_path, mode='a', header=False, index=False)
            logging.info("full csv for %s is constructed", report)


def data_preprocessing():
    """
    Starting initialization
    :return:
    """
    csv_file_info = download_raw_csv_files()
    walk_through_files(csv_file_info)
