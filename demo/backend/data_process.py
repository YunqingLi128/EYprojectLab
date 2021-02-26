import itertools
import os
import requests
import urllib3
import json
import pandas as pd
from flask import current_app
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_cur_path():
    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    return path


def download_csv(report, RSSD_ID, date):
    base_url = "https://www.ffiec.gov/npw/FinancialReport/ReturnFinancialReportCSV?rpt={}&id={}&dt={}"
    path = get_cur_path()
    dir_name = os.path.join(path, "data", RSSD_ID)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    try:
        csv_url = base_url.format(report, RSSD_ID, date)
        csv_file_name = "_".join([report, RSSD_ID, date]) + ".csv"
        csv_file_path = os.path.join(dir_name, csv_file_name)
        if not os.path.exists(csv_file_path):
            response = requests.get(url=csv_url, verify=False)
            if response.status_code == 200 and "<body>" not in response.text:
                with open(csv_file_path, "wb") as f:
                    f.write(response.content)
                return csv_file_path
        return None
    except Exception as e:
        print(e)


def raw_csv_consolidation(csv_path):
    _, csv_name = os.path.split(csv_path)
    report, institution, date = csv_name.split(".")[0].split("_")
    df = pd.read_csv(csv_path, header=0)
    index_names = df[~df["ItemName"].str.startswith("M")].index  # drop the rows which ItemName is not "M*"
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
    dir_name = os.path.join(path, "data")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

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
            csv_file_path = download_csv(report, institution_obj["RSSD_ID"], dates[i])
            if csv_file_path is not None:
                end_date = dates[i]
                df = raw_csv_consolidation(csv_file_path)
                df_list.append(df)
        institution_obj["start_date"] = start_date
        institution_obj["end_date"] = end_date

    if len(df_list) > 0:
        full_df = pd.concat(df_list)
        full_csv_path = os.path.join(get_cur_path(), "data", report + ".csv")
        full_df.to_csv(full_csv_path, mode='a', header=False, index=False)

    with open(json_file_path, 'w') as f:
        json.dump(data_info, f, indent=4)


# Not used currently
def walk_through_files(path, file_extension='.csv'):
    for dir_path, dir_names, filenames in os.walk(path):
        for file_name in filenames:
            if file_name.endswith(file_extension):
                yield os.path.join(dir_path, file_name)


# Not used currently
def data_preprocessing():
    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    institutions = ["1073757", "1951350", "2380443", "1039502", "2162966", "1120754"]
    dir_paths = []
    for name in institutions:
        dir_paths.append(os.path.join(path, "data", name))
    df_list = []
    for dir_path in dir_paths:
        for csv_path in walk_through_files(dir_path):
            df = raw_csv_consolidation(csv_path)
            df_list.append(df)
    result = pd.concat(df_list)
    print(result.head(5))
    result.to_csv(os.path.join(path, "data", "FFIEC102.csv"), index=False)
