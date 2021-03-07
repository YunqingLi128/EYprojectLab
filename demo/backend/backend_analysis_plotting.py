import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import json
import os
from backend.data_process import get_cur_path

# Yaoqi's test
def get_data():
    path = get_cur_path()
    csv_path = os.path.join(path, "data/FFIEC102.csv")
    df = pd.read_csv(csv_path, dtype=str)
    df.columns = ['Company', 'Quarter', 'Item_ID', 'Item']
    df = df.set_index(['Company', 'Quarter'])
    df.sort_index(inplace=True)
    return df

def get_data_2():
    path = get_cur_path()
    csv_path = os.path.join(path, "data/FRY9C.csv")
    df = pd.read_csv(csv_path, dtype=str)
    df.columns = ['Company', 'Quarter', 'Item_ID', 'Item']
    df = df.set_index(['Company', 'Quarter'])
    df.sort_index(inplace=True)
    return df

# previous day's Value-at-risk (VaR)-based measure
# IR, Debt, Equity, FX, Commodities
# return JSON: {id: [{item_name_1: item_value_1}, {item_name_2: item_value_2}]}
def test_asset_VaR_query(quarter_date):
    raw_data = get_data()
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
    raw_data = get_data()
    VaR_item_names = ['MRRRS298', 'MRRRS302']
    data = raw_data.query('Item_ID in @VaR_item_names and Quarter == @quarter_date')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], VaR_data[key]) for key in VaR_data)  # change the id to name
    return res

# VaR sVaR Comparison
# MRRRS298
# MRRRS302
def VaR_sVarR_comparison(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    VaR_item_names = ['MRRRS298', 'MRRRS302']
    data = raw_data.query('Item_ID in @VaR_item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], VaR_data[key]) for key in VaR_data)  # change the id to name
    return res

# Trading asset comparison
# BHCK3545
# BHCK3548
def trading_asset_comparison(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data_2()
    trading_asset_item_names_asset = ['BHCK3545']
    trading_asset_item_names_liability = ['BHCK3548']
    trading_asset_item_names = ['BHCK3545','BHCK3548']
    data = raw_data.query('Item_ID in @trading_asset_item_names and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = raw_data.query('Item_ID in @trading_asset_item_names_asset and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data_liability = raw_data.query('Item_ID in @trading_asset_item_names_liability and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')

    data_asset['Item_2'] = data_liability['Item']
    data_asset['Gross'] = data_asset['Item'].astype(int) + data_asset['Item_2'].astype(int)
    data_asset['Net'] = data_asset['Item'].astype(int) - data_asset['Item_2'].astype(int)
    data_asset = data_asset.drop(['Item','Item_2'], axis=1)
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
    data = data.drop(['New_Item'],axis=1)
    trading_asset_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], trading_asset_data[key]) for key in trading_asset_data)  # change the id to name
    return res


# Advanced market risk-weighted assets
# MRRRS347
def advanced_market_risk_weighted_assets(quarter_date_from, quarter_date_to):
    # TODO: Store this company map in a csv?
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    advanced_market_risk_weighted_assets_ID = ['MRRRS347']
    data = raw_data.query('Item_ID in @advanced_market_risk_weighted_assets_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

# VaR based measure overtime
def VaR_based_measure_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    VaR_based_measure_overtime_ID = ['MRRRS298']
    data = raw_data.query('Item_ID in @VaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

# sVaR VaR ratio overtime
def sVaR_VaR_ratio_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    VaR_based_measure_overtime_ID = ['MRRRS298']
    sVaR_based_measure_overtime_ID = ['MRRRS302']
    data = raw_data.query('Item_ID in @VaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')

    data_2 = raw_data.query('Item_ID in @sVaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data['Item_2'] = data_2['Item']
    data['Ratio'] = data['Item_2'].astype(int)/data['Item'].astype(int)
    data = data.drop(['Item','Item_2'], axis=1)
    data['Item'] = data['Ratio']
    data = data.drop(['Ratio'], axis=1)
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

def diversification_of_var_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = data_asset.reset_index()
    data_asset['Item']=data_asset.Item.astype(int)
    data_asset['total_asset_var']=data_asset.groupby('Company')['Item'].transform('sum')

    varID = ['MRRRS298']
    data_day_var = raw_data.query('Item_ID in @varID and Quarter<= @quarter_date_to and '
                                  'Quarter >= @quarter_date_from')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item']=data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data.update(data.groupby('Company').ffill())

    data['total_asset_var'] = data.total_asset_var.astype(int)
    data['asset_var_by_percentage'] = 100 * (data.Item / data.total_asset_var)
    data.loc[data.Item_ID=='MRRRS298', 'asset_var_by_percentage'] =\
        100 * \
        (data.loc[data.Item_ID=='MRRRS298', 'total_asset_var']-data.loc[data.Item_ID=='MRRRS298', 'Item'])/ \
        data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var']
    data.sort_values(by='Company', inplace=True)

    output_data = data.groupby('Company')[['Item_ID', 'asset_var_by_percentage']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res

def var_by_assetclass_diversification(quarter_date):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    # Previous day's VaR: IR='MRRRS348' Debt='MRRRS349' Equity='MRRRS350' FX='MRRRS351' Commodities='MRRRS352'

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter == @quarter_date')
    data_asset = data_asset.reset_index()
    data_asset['Item']=data_asset.Item.astype(int)
    data_asset['total_asset_var']=data_asset.groupby('Company')['Item'].transform('sum')

    varID = ['MRRRS298']
    data_day_var = raw_data.query('Item_ID in @varID and Quarter == @quarter_date')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item']=data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data.update(data.groupby('Company').ffill())

    data['total_asset_var'] = data.total_asset_var.astype(int)
    data['asset_var_by_percentage'] = 100 * (data.Item / data.total_asset_var)
    data.loc[data.Item_ID=='MRRRS298', 'asset_var_by_percentage'] =\
        100 * \
        (data.loc[data.Item_ID=='MRRRS298', 'Item']-data.loc[data.Item_ID=='MRRRS298', 'total_asset_var'])/ \
        data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var']
    data.sort_values(by='Company', inplace=True)

    output_data = data.groupby('Company')[['Item_ID', 'asset_var_by_percentage']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res

# test_asset_VaR_query(date)
# test_VaR_sVarR_query(date)


# Yuyan's work
def standardized_risk_weighted_assets(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    item_names = ['MRRRS343', 'MRRRH327', 'MRRRS313', 'MRRRS311', 'MRRRS302', 'MRRRS298']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    return total_data

def num_var_breach_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data()
    item_names = ['MRRRS362']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res
    
# I don't know which item to use...
def stress_window(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data_2()
    item_names = ['BHCALE85']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res
