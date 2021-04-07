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


def format_date(date):
    quarter_map = {"0331": "Q1", "0630": "Q2", "0930": "Q3", "1231": "Q4"}
    year, day = date[:4], date[4:]
    quarter_date = year + quarter_map[day]
    return quarter_date


def get_previous_quarter(cur_quarter):
    year_quarter = cur_quarter.split('Q')
    if year_quarter[1] == '1':
        year = str(int(year_quarter[0]) - 1)
        quarter = '4'
    else:
        year = year_quarter[0]
        quarter = str(int(year_quarter[1]) - 1)
    pre_quarter = year + 'Q' + quarter
    return pre_quarter


def generate_dates():
    """
    Generate quarter dates from 2015 to current date

    :return: quarter date list
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
    return all_dates


def parse_csv_path(csv_path):
    _, csv_name = os.path.split(csv_path)
    report, institution, date = csv_name.split(".")[0].split("_")
    return report, institution, date


def load_url(url, timeout):
    response = requests.get(url=url, verify=False, allow_redirects=False, timeout=timeout)
    if response.status_code == 200:
        return response.content


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
                res = future.result()
                if res is None:
                    raise Exception("invalid csv url")
                data = res.decode('utf-8')
                if "<body>" in data:
                    raise Exception("not a csv file")
                with open(path, "w") as f:
                    f.write(data)
            except Exception as exc:
                logging.info('%r generated an exception: %s' % (url, exc))
            else:
                logging.info("%s is downloaded", path)


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


def walk_through_institution_folder_files(reports, institutions, mode):
    """
    Raw csv consolidation for downloaded csv files

    :param mode: if mode='w', overwrite the full csv, elif mode='a', append to the full csv
    :param institutions: institution RSSD ID list
    :param reports: report list

    :return data info for input institutions
    """
    path = get_cur_path()
    data_dir_path = os.path.join(path, "data", "raw_data")
    data_info = {}
    report_df_dict = {report: [] for report in reports}
    for rssd_id in institutions:
        folder_path = os.path.join(data_dir_path, rssd_id)
        report_info = {report: [] for report in reports}
        for root, dirs, files in os.walk(folder_path):
            if len(files) == 0:
                continue
            sorted_files = sorted(files)
            for file in sorted_files:
                if not file.endswith(".csv"):
                    continue
                csv_file_path = os.path.join(root, file)
                report, institution, date = parse_csv_path(csv_file_path)
                df = raw_csv_consolidation(report, csv_file_path)
                report_df_dict[report].append(df)
                report_info[report].append(date)

            # find start date and end date and update config object
            for report, dates in report_info.items():
                if len(dates) == 0:
                    continue
                start_date, end_date = format_date(min(dates)), format_date(max(dates))
                report_info[report] = {
                    "start_quarter": start_date,
                    "end_quarter": end_date
                }
            data_info[rssd_id] = report_info
        logging.info("data config info for %s: %s", rssd_id, report_info)

    for report, df_list in report_df_dict.items():
        if len(df_list) > 0:
            full_df = pd.concat(df_list)
            full_csv_path = os.path.join(get_cur_path(), "data", report + ".csv")
            full_df.to_csv(full_csv_path, header=False, index=False, mode=mode)
            logging.info("full csv for %s is constructed", report)
    return data_info


def load_data_config_file():
    path = get_cur_path()
    json_file_path = os.path.join(path, "data_setting.json")
    with open(json_file_path, 'r') as f:
        data_info = json.loads(f.read())
    return data_info


def save_data_config_file(data_info):
    path = get_cur_path()
    json_file_path = os.path.join(path, "data_setting.json")
    with open(json_file_path, 'w') as f:
        json.dump(data_info, f, indent=4)


def update_data_config_file(csv_file_info):
    # update the info of all institution in the data config file
    data_info = load_data_config_file()
    institutions = data_info["institutions"]
    for rssd_id in institutions:
        institutions[rssd_id]["data_status"] = csv_file_info[rssd_id]
    save_data_config_file(data_info)
    logging.info("updated data config info: %s", data_info)
    return data_info


def add_institution_to_data_config_file(csv_file_info, rssd_id, name, nick_name):
    data_info = load_data_config_file()
    institution_info = data_info["institutions"]
    institution_info[rssd_id] = {}
    institution_info[rssd_id]["Name"] = name
    institution_info[rssd_id]["Nick"] = nick_name
    institution_info[rssd_id]["data_status"] = csv_file_info[rssd_id]
    save_data_config_file(data_info)
    logging.info("updated data config info: %s", data_info)
    return data_info


def get_preprocess_data(reports, institutions, mode):
    dates = generate_dates()
    path = get_cur_path()
    data_dir_path = create_dir(path, "data/raw_data")  # create data folder

    # create institution folders
    for rssd_id in institutions:
        create_dir(data_dir_path, rssd_id)

    download_raw_csv_files(reports, institutions, dates)
    # combine raw csv files to full csv file
    csv_file_info = walk_through_institution_folder_files(reports, institutions, mode)
    return csv_file_info


def init_data():
    """
    Data initialization (update) for all institutions in the data config file
    :return: current data info
    """
    data_info = load_data_config_file()
    reports, institutions = data_info["reports"], data_info["institutions"].keys()
    csv_file_info = get_preprocess_data(reports, institutions, mode='w')
    return update_data_config_file(csv_file_info)


def add_data(rssd_id, name, nick_name):
    """
    Add new data of input institutions and update the data config file

    :param rssd_id: institution RSSD ID from user input
    :param name: institution name from user input
    :param nick_name: institution nick name from user input
    :return: operation status and message

    testing examples:
    rssd_id: '2277860', name: 'Capital One', nick_name: 'COF',
    rssd_id: '1119794', name: 'U.S. BANCORP', nick_name: 'USB'
    """
    # TODO: find a better way to check whether RSSD ID is valid
    # Maybe deal with:
    # https://www.ffiec.gov/npw/Institution/Search
    # ?Term=1073757&City=&Countries=1007&IdType=fdic-cert&Identifier=&Statuses=Active&X-Requested-With=XMLHttpRequest
    institution_check_base_url = "https://www.ffiec.gov/npw/Institution/Profile/"
    res = {"status": 500, "message": ""}
    try:
        # current logic: if any of institution raises exception, the function will return error
        response = load_url(institution_check_base_url + rssd_id, 60)
        if response is None:
            raise Exception("The institution does not exist")

        data_info = load_data_config_file()
        reports = data_info["reports"]
        if rssd_id in data_info["institutions"]:
            raise Exception("The institution {} already exists".format(rssd_id))
        institutions = [rssd_id]
        csv_file_info = get_preprocess_data(reports, institutions, mode='a')
        data_info = add_institution_to_data_config_file(csv_file_info, rssd_id, name, nick_name)
        res["status"] = 200
        res["message"] = "success"
        res["data_info"] = data_info
    except Exception as e:
        logging.error("%s", e)
        res["message"] = str(e)
    return res

# testing institutions = '1069778'
