import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import operator
import json
import os
from backend.data_process import get_cur_path, get_previous_quarter
from flask import session


def get_data(report):
    path = get_cur_path()
    csv_path = os.path.join(path, "data", report + ".csv")
    df = pd.read_csv(csv_path, dtype=str)
    df.columns = ['Company', 'Quarter', 'Item_ID', 'Item']
    df = df.set_index(['Company', 'Quarter'])
    df.sort_index(inplace=True)
    return df


# previous day's Value-at-risk (VaR)-based measure
# IR, Debt, Equity, FX, Commodities
# return JSON: {id: [{item_name_1: item_value_1}, {item_name_2: item_value_2}]}
def test_asset_VaR_query(quarter_date):
    raw_data = get_data('FFIEC102')
    asset_VaR_item_names = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    data = raw_data.query('Item_ID in @asset_VaR_item_names and Quarter == @quarter_date')
    # print(data)
    asset_VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    for k, v in asset_VaR_data.items():
        asset_VaR_data[k] = list(map(lambda x: {x[0]: x[1]}, v))
    res = json.dumps(asset_VaR_data)
    # data.reset_index(inplace=True)
    # data.set_index(['Company', 'Quarter', 'Item_ID'], inplace=True)
    # result = data.to_json(orient="index", indent=4)
    # print(result)


# Previous day's VaR-based measure and Most recent stressed VaR-based measure
# return JSON: {id: [[item_name_1, item_value_1], [item_name_2, item_value_2]]}
def test_VaR_sVarR_query(quarter_date):
    raw_data = get_data('FFIEC102')
    VaR_item_names = ['MRRRS298', 'MRRRS302']
    data = raw_data.query('Item_ID in @VaR_item_names and Quarter == @quarter_date')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    return VaR_data


def item_name_mapping(x, mapping):
    data_map = {}
    data_list = x.values.tolist()
    for item in data_list:
        data_map[mapping[item[0]]] = item[1]
    return data_map


# VaR sVaR Comparison
def get_var_svar_item_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    """
    VaR_sVaR_comparison, return the amount of VaR and sVaR at each quarter in specific quarters
    MRRRS298: Previous day's VaR-based measure
    MRRRS302: Most recent stressed VaR-based measure
    """
    raw_data = get_data('FFIEC102')
    VaR_comp_map = {'MRRRS298': 'VaR', 'MRRRS302': 'SVaR'}
    data = raw_data.query('Item_ID in @VaR_comp_map.keys() and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(item_name_mapping, mapping=VaR_comp_map).to_dict()
    res = dict((comp_dict[key], VaR_data[key]) for key in VaR_data)  # change the id to name
    return res


# Trading asset comparison
def get_trading_asset_item_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the amount of net and gross trading asset at each quarter in specific quarters
    BHCK3545: TRADING ASSETS
    BHCK3548: TRADING LIABILITIES
    """
    raw_data = get_data('FRY9C')
    trading_asset_item_names_asset = ['BHCK3545']
    trading_asset_item_names_liability = ['BHCK3548']
    trading_asset_item_names = ['BHCK3545', 'BHCK3548']
    data = raw_data.query('Item_ID in @trading_asset_item_names and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = raw_data.query('Item_ID in @trading_asset_item_names_asset and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data_liability = raw_data.query('Item_ID in @trading_asset_item_names_liability and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')

    data_asset['Item_2'] = data_liability['Item']
    data_asset['Gross'] = data_asset['Item'].astype(int) + data_asset['Item_2'].astype(int)
    data_asset['Net'] = data_asset['Item'].astype(int) - data_asset['Item_2'].astype(int)
    data_asset = data_asset.drop(['Item', 'Item_2'], axis=1)
    data_asset = data_asset.reset_index()
    whole_val = []
    Flag = 1
    for index, row in data_asset.iterrows():
        if Flag == 1:
            whole_val.append(row['Gross'])
            Flag = -1
        if Flag == -1:
            whole_val.append(row['Net'])
            Flag = 1
    new = pd.Series(whole_val)
    data['New_Item'] = new.values
    data['Item'] = data['New_Item']
    data = data.drop(['New_Item'], axis=1)
    trading_asset_map = {'BHCK3545': 'Net Trading Asset', 'BHCK3548': 'Gross Trading Asset'}
    trading_asset_data = data.groupby('Company')[['Item_ID', 'Item']].apply(item_name_mapping, mapping=trading_asset_map).to_dict()
    res = dict((comp_dict[key], trading_asset_data[key]) for key in trading_asset_data)  # change the id to name
    return res


# Advanced market risk-weighted assets
def get_risk_weighted_asset_item_overtime(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the amount of advanced market risk weighted assets overtime
    MRRRS347: MARKET RISK-WEIGHTED ASSETS
    """
    raw_data = get_data('FFIEC102')
    advanced_market_risk_weighted_assets_ID = ['MRRRS347']
    data = raw_data.query('Item_ID in @advanced_market_risk_weighted_assets_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res


# VaR based measure overtime
def get_var_measure_item_overtime(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the amount of VaR-based measure overtime
    MRRRS298: Previous day's VaR-based measure
    """
    raw_data = get_data('FFIEC102')
    VaR_based_measure_overtime_ID = ['MRRRS298']
    data = raw_data.query('Item_ID in @VaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res


# sVaR VaR ratio overtime
def get_ratio_item_overtime(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the ratio of sVaR and VaR overtime
    MRRRS298: Previous day's VaR-based measure
    MRRRS302: Most recent stressed VaR-based measure
    """
    raw_data = get_data('FFIEC102')
    VaR_based_measure_overtime_ID = ['MRRRS298']
    sVaR_based_measure_overtime_ID = ['MRRRS302']
    data = raw_data.query('Item_ID in @VaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')

    data_2 = raw_data.query('Item_ID in @sVaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data['Item_2'] = data_2['Item']
    data['Ratio'] = data['Item_2'].astype(int) / data['Item'].astype(int)
    data = data.drop(['Item', 'Item_2'], axis=1)
    data['Item'] = data['Ratio']
    data = data.drop(['Ratio'], axis=1)
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res


# Diversification Overtime
def get_var_diversification_item_overtime(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the amount of diversification as a percentage of VaR overtime
    """
    raw_data = get_data('FFIEC102')
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = data_asset.reset_index()
    data_asset['Item'] = data_asset.Item.astype(int)
    data_asset['total_asset_var'] = data_asset.groupby(['Company', 'Quarter'])['Item'].transform('sum')

    varID = ['MRRRS298']
    data_day_var = raw_data.query('Item_ID in @varID and Quarter<= @quarter_date_to and '
                                  'Quarter >= @quarter_date_from')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item'] = data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data.update(data.groupby(['Company', 'Quarter']).ffill())

    data['total_asset_var'] = data.total_asset_var.astype(int)
    data = data.loc[data.Item_ID == 'MRRRS298']

    data['diver_as_percent_of_Var'] = 100 * (data.total_asset_var-data.Item)/data.total_asset_var

    output_data = data.groupby('Company')[['Quarter', 'diver_as_percent_of_Var']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res


# Asset Diversification Overtime
def get_asset_class_var_item_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    """
    return VaR percentage in different asset classes and diversification effect of companies in specific quarters
    Previous day's VaR:
    IR='MRRRS348' Debt='MRRRS349' Equity='MRRRS350' FX='MRRRS351' Commodities='MRRRS352'
    """
    raw_data = get_data('FFIEC102')
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    asset_dict = {'MRRRS348': 'IR',
                  'MRRRS349': 'Debt',
                  'MRRRS350': 'Equity',
                  'MRRRS351': 'FX',
                  'MRRRS352': 'Commodities',
                  'MRRRS298': 'Diversification'}

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = data_asset.reset_index()
    data_asset['Item'] = data_asset.Item.astype(int)
    data_asset['total_asset_var'] = data_asset.groupby('Company')['Item'].transform('sum')

    varID = ['MRRRS298']
    data_day_var = raw_data.query('Item_ID in @varID and Quarter<= @quarter_date_to and '
                                  'Quarter >= @quarter_date_from')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item'] = data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data.update(data.groupby('Company').ffill())

    data['total_asset_var'] = data.total_asset_var.astype(int)
    data['asset_var_by_percentage'] = 100 * (data.Item / data.total_asset_var)
    data.loc[data.Item_ID == 'MRRRS298', 'asset_var_by_percentage'] =\
        100 * \
        (data.loc[data.Item_ID == 'MRRRS298', 'Item']-data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var'])/ \
        data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var']
    data.sort_values(by='Company', inplace=True)
    output_data = data.groupby('Item_ID')[['Company', 'asset_var_by_percentage']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res


# Num of Breach overtime
def get_num_var_breach_item_overtime(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the amount of the number of VaR breaches overtime
    MRRRS362: Number of trading days in the calendar quarter where the trading day's trading loss
    exceeded the respective VaR estimate
    """
    raw_data = get_data('FFIEC102')
    item_names = ['MRRRS362']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res


# Standardized risk weighted assets
def get_standardized_risk_weighted_assets_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the amount of standardized market risk-weighted assets breakdown by bank in specific quarters
    """
    asset_dict = {'MRRRS343': 'De Minimis',
                  'MRRRH327': 'Std Comprehensive Risk',
                  'MRRRS313': 'Incremental Risk',
                  'MRRRS311': 'Add-Ons',
                  'MRRRS302': 'sVaR',
                  'MRRRS298': 'VaR'}

    raw_data = get_data('FFIEC102')
    item_names = ['MRRRS343', 'MRRRH327', 'MRRRS313', 'MRRRS311', 'MRRRS302', 'MRRRS298']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res


# Stress window
# return the classification of stress window under creteria: if year in 2007/2008, then it is 2008 Financial Crisis; if year in 2019, then it is Covid 19
def get_stress_window_item_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
    item_names = ['MRRRS366']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    for i in range(len(data['Item'])):
        if '2007' in data.loc[i, 'Item'] or '2008' in data.loc[i, 'Item']:
            data.loc[i, 'Item'] = '2008 Financial Crisis'
        if '2019' in data.loc[i, 'Item']:
            data.loc[i, 'Item'] = 'Covid 19'
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res


def get_asset_to_var_ratio_item_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    """
    return trading asset to risk ratio in specific quarters,
    the ratios order is: 'Net/VaR', 'Gross/VaR', 'Net/sVaR', 'Gross/sVaR'
    """
    raw_data_var = get_data('FFIEC102')
    raw_data_asset = get_data('FRY9C')
    var_item_names = ['MRRRS298', 'MRRRS302']
    data_var = raw_data_var.query('Item_ID in @var_item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from').reset_index()
    
    data_var1 = data_var[data_var['Item_ID'] == 'MRRRS298'].rename(columns={'Item': 'VaR'}).drop(['Item_ID'], axis=1)
    data_var2 = data_var[data_var['Item_ID'] == 'MRRRS302'].rename(columns={'Item': 'sVaR'}).drop(['Item_ID'], axis=1)
    data_var = pd.merge(data_var1, data_var2, on=['Company', 'Quarter']).reset_index(drop=True)
    data_var[['VaR', 'sVaR']] = data_var[['VaR', 'sVaR']].astype('int')
    
    trading_asset_item_names_asset = ['BHCK3545']
    trading_asset_item_names_liability = ['BHCK3548']
    trading_asset_item_names = ['BHCK3545', 'BHCK3548']
    data = raw_data_asset.query('Item_ID in @trading_asset_item_names and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = raw_data_asset.query('Item_ID in @trading_asset_item_names_asset and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data_liability = raw_data_asset.query('Item_ID in @trading_asset_item_names_liability and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data_asset.loc[:, 'Item_2'] = data_liability.loc[:, 'Item']
    data_asset.loc[:, 'Gross'] = data_asset.loc[:, 'Item'].astype(int) + data_asset.loc[:, 'Item_2'].astype(int)
    data_asset.loc[:, 'Net'] = data_asset.loc[:, 'Item'].astype(int) - data_asset.loc[:, 'Item_2'].astype(int)
    data_asset = data_asset.drop(['Item', 'Item_2', 'Item_ID'], axis=1)
    data_asset = data_asset.reset_index()
    
    tot_data = pd.merge(data_var, data_asset, on=['Company', 'Quarter'])

    tot_data['Net/VaR'] = tot_data['Net'] / tot_data['VaR']
    tot_data['Gross/VaR'] = tot_data['Gross'] / tot_data['VaR']
    tot_data['Net/sVaR'] = tot_data['Net'] / tot_data['sVaR']
    tot_data['Gross/sVaR'] = tot_data['Gross'] / tot_data['sVaR']
    tot_data = tot_data.drop(['VaR', 'sVaR', 'Gross', 'Net'], axis=1)
    # You can just remember the name and order of this 4 things...

    # return dict
    def func(x, keys):
        values = x.values.tolist()[0]
        return dict(zip(keys, values))

    ratio_list = ['Net Trading \nAsset / VaR', 'Gross Trading \nAsset / VaR',
                  'Net Trading \nAsset / sVaR', 'Gross Trading \nAsset / sVaR']
    total_data = tot_data.groupby('Company')[['Net/VaR', 'Gross/VaR', 'Net/sVaR', 'Gross/sVaR']].apply(func, keys=ratio_list).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res


def get_revenue_to_var_ratio_item_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    """
    return trading revenue to VaR and sVaR ratios in specific quarters,
    the ratios order is: 'revenue/VaR', 'revenue/sVaR'
    """
    raw_data_var = get_data('FFIEC102')
    raw_data_revenue = get_data('FRY9C')
    var_item_names = ['MRRRS298', 'MRRRS302']
    data_var = raw_data_var.query('Item_ID in @var_item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from').reset_index()
    
    data_var1 = data_var[data_var['Item_ID'] == 'MRRRS298'].rename(columns={'Item': 'VaR'}).drop(['Item_ID'], axis=1)
    data_var2 = data_var[data_var['Item_ID'] == 'MRRRS302'].rename(columns={'Item': 'sVaR'}).drop(['Item_ID'], axis=1)
    data_var = pd.merge(data_var1, data_var2, on=['Company', 'Quarter']).reset_index(drop=True)
    data_var[['VaR', 'sVaR']] = data_var[['VaR', 'sVaR']].astype('int')
    
    trading_revenue_item_names = ['BHCKA220']
    data_revenue = raw_data_revenue.query('Item_ID in @trading_revenue_item_names and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    
    tot_data = pd.merge(data_var, data_revenue, on=['Company', 'Quarter']).rename(columns={'Item': 'revenue'})
    tot_data['revenue/VaR'] = tot_data['revenue'].astype(int) / tot_data['VaR']
    tot_data['revenue/sVaR'] = tot_data['revenue'].astype(int) / tot_data['sVaR']
    tot_data = tot_data.drop(['VaR', 'sVaR', 'revenue', 'Item_ID'], axis=1)

    # return dict
    def func(x, keys):
        values = x.values.tolist()[0]
        return dict(zip(keys, values))

    ratio_list = ['Trading Revenue / VaR', 'Trading Revenue / sVaR']
    # You can just remember the name and order of these 2 things...
    total_data = tot_data.groupby('Company')[['revenue/VaR', 'revenue/sVaR']].apply(func, keys=ratio_list).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res


def get_trading_item_and_change_by_quarter(item_id, item_name, quarter, comp_dict):
    pre_quarter = get_previous_quarter(quarter)
    raw_data_asset = get_data('FRY9C')
    data_last = raw_data_asset.query('Item_ID == @item_id and Quarter == @pre_quarter').reset_index()
    data_current = raw_data_asset.query('Item_ID == @item_id and Quarter == @quarter').reset_index()
    data = pd.merge(data_last, data_current, on='Company', how='right', validate="one_to_one")
    data['Item_x'] = data.Item_x.astype(float)
    data['Item_y'] = data.Item_y.astype(float)
    data['percentage_change'] = 100 * (data.Item_y - data.Item_x) / data.Item_x
    data.rename(columns={'Item_y': item_name}, inplace=True)
    output_data = data.groupby('Company')[[item_name, 'percentage_change']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)
    return res


def get_trading_assets_and_change_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    item_id, item_name = 'BHCK3545', 'Trading_Assets'
    res = get_trading_item_and_change_by_quarter(item_id, item_name, quarter_date_from, comp_dict)
    return res


def get_trading_liabilities_and_change_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    item_id, item_name = 'BHCK3548', 'Trading_Liabilities'
    res = get_trading_item_and_change_by_quarter(item_id, item_name, quarter_date_from, comp_dict)
    return res


def calculate_trading_asset_and_percent_change(cal_type, quarter, comp_dict):
    op_dict = {"Net": operator.sub, "Gross": operator.add}
    op = op_dict[cal_type]
    pre_quarter = get_previous_quarter(quarter)
    raw_data_asset = get_data('FRY9C')
    trading_asset = 'BHCK3545'
    trading_liability = 'BHCK3548'
    data_asset_last = raw_data_asset.query('Item_ID == @trading_asset and Quarter == @pre_quarter')
    data_asset_current = raw_data_asset.query('Item_ID == @trading_asset and Quarter == @quarter')
    data_liability_last = raw_data_asset.query('Item_ID == @trading_liability and Quarter == @pre_quarter')
    data_liability_current = raw_data_asset.query('Item_ID == @trading_liability and Quarter == @quarter')

    data_asset_last['Item_2'] = data_liability_last['Item']
    data_asset_last[cal_type] = op(data_asset_last['Item'].astype(int), data_asset_last['Item_2'].astype(int))
    data_asset_current['Item_2'] = data_liability_current['Item']
    data_asset_current[cal_type] = op(data_asset_current['Item'].astype(int), data_asset_current['Item_2'].astype(int))
    data_asset_current = data_asset_current.drop(['Item', 'Item_2'], axis=1)
    data_asset_current = data_asset_current.reset_index()
    data_asset_last = data_asset_last.drop(['Item', 'Item_2'], axis=1)
    data_asset_last = data_asset_last.reset_index()

    data = pd.merge(data_asset_last, data_asset_current, on='Company', how='right', validate='one_to_one')
    pre_quarter_net, cur_quarter_net = cal_type + '_x', cal_type + '_y'
    data[pre_quarter_net] = data[pre_quarter_net].astype(float)
    data[cur_quarter_net] = data[cur_quarter_net].astype(float)
    data['percent_change'] = 100 * (data[cur_quarter_net] - data[pre_quarter_net]) / data[pre_quarter_net]
    trading_asset_item_name = cal_type + "_Trading_Assets"
    data.rename(columns={cur_quarter_net: trading_asset_item_name}, inplace=True)
    net_data = data.groupby('Company')[[trading_asset_item_name, 'percent_change']].apply(
        lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], net_data[key]) for key in net_data)
    return res


# return net trading asset by quarter (bar chart) and percent change from last quarter(line chart)
def get_net_trading_asset_and_percent_change(quarter_date_from, quarter_date_to, comp_dict):
    res = calculate_trading_asset_and_percent_change("Net", quarter_date_from, comp_dict)
    return res


# return gross trading asset by quarter (bar chart) and percent change from last quarter(line chart)
def get_gross_trading_asset_and_percent_change(quarter_date_from, quarter_date_to, comp_dict):
    res = calculate_trading_asset_and_percent_change("Gross", quarter_date_from, comp_dict)
    return res
