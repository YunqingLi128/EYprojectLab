import itertools
import os
import requests
import urllib.request
import urllib3
import json
import pandas as pd
import logging
import concurrent.futures
from datetime import datetime

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


# Old version
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


def generate_dates():
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
    return all_dates


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


def construct_urls(reports, institutions, dates):
    """
    :param reports:
    :param institutions:
    :param dates:
    :return: (csv_file_path, web_url) pair list
    """
    path = get_cur_path()
    data_dir_path = os.path.join(path, "data/raw_data")
    urls = []
    base_url = "https://www.ffiec.gov/npw/FinancialReport/ReturnFinancialReportCSV?rpt={}&id={}&dt={}"
    for element in itertools.product(reports, institutions, dates):
        csv_file_name = "_".join(element) + ".csv"
        csv_file_path = os.path.join(data_dir_path, element[1], csv_file_name)
        url = base_url.format(*element)
        urls.append((csv_file_path, url))
    return urls


def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


# Old version
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


def download_raw_csv_files(reports, institutions, dates):
    """
    Downloading raw csv files
    """
    # parallel downloading using threads
    urls = construct_urls(reports, institutions, dates)
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, pair[1], 60): pair for pair in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            path, url = future_to_url[future]
            try:
                data = future.result().decode("utf-8")
                if "<body>" not in data:
                    with open(path, "w") as f:
                        f.write(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                logging.info("%s is downloaded", path)


def walk_through_files(reports, path):
    """
    Raw csv consolidation for downloaded csv files

    :param path: raw csv data folder
    :return: file_info: updated downloaded reports
    """
    file_info = {}
    report_df_dict = {report: [] for report in reports}
    for root, dirs, files in os.walk(path):
        if len(dirs) == 0:  # institution folder
            _, rssd_id = os.path.split(root)
            report_info = {report: [] for report in reports}
            sorted_files = sorted(files)
            for file in sorted_files:
                if file.endswith(".csv"):
                    csv_file_path = os.path.join(root, file)
                    report, institution, date = parse_csv_path(csv_file_path)
                    df = raw_csv_consolidation(report, csv_file_path)
                    report_df_dict[report].append(df)
                    report_info[report].append(date)
            # find start date and end date and update config object
            for report, dates in report_info.items():
                start_date, end_date = format_date(min(dates)), format_date(max(dates))
                report_info[report] = {
                    "start_quarter": start_date,
                    "end_quarter": end_date
                }
            file_info[rssd_id] = report_info
    logging.info("config file %s", file_info)

    for report, df_list in report_df_dict.items():
        if len(df_list) > 0:
            full_df = pd.concat(df_list)
            full_csv_path = os.path.join(get_cur_path(), "data", report + ".csv")
            full_df.to_csv(full_csv_path, header=False, index=False)
            logging.info("full csv for %s is constructed", report)

    return file_info


def data_preprocessing():
    """
    Starting initialization
    :return:
    """
    dates = generate_dates()

    # create data folder
    path = get_cur_path()
    data_dir_path = create_dir(path, "data/raw_data")

    # load the data config file
    json_file_path = os.path.join(path, "data_setting.json")
    with open(json_file_path, 'r') as f:
        data_info = json.loads(f.read())
    reports = data_info["reports"]
    institutions = data_info["institutions"]

    # create institution folders
    for rssd_id in institutions:
        create_dir(data_dir_path, rssd_id)

    download_raw_csv_files(reports, institutions, dates)

    # combine raw csv files to full csv file
    path = get_cur_path()
    data_dir_path = os.path.join(path, "data", "raw_data")
    csv_file_info = walk_through_files(reports, data_dir_path)

    # update the data config file
    for rssd_id in institutions:
        institutions[rssd_id]["data_status"] = csv_file_info[rssd_id]
    with open(json_file_path, 'w') as f:
        json.dump(data_info, f, indent=4)

    return data_info
