import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import json
import os
from backend.data_process import get_cur_path
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

# VaR sVaR Comparison
# MRRRS298
# MRRRS302
# VaR_sVaR_comparison, return the amount of VaR and sVaR at each quarter in specific quarters
def get_var_svar_item_byquarter(quarter_date_from, quarter_date_to, comp_dict):
    raw_data = get_data('FFIEC102')
    VaR_item_names = ['MRRRS298', 'MRRRS302']
    data = raw_data.query('Item_ID in @VaR_item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], VaR_data[key]) for key in VaR_data)  # change the id to name
    return res

# Trading asset comparison
# BHCK3545
# BHCK3548
# return the amount of net and gross trading asset at each quarter in specific quarters
def get_trading_asset_item_byquarter(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FRY9C')
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
    return trading_asset_data


# Advanced market risk-weighted assets
# MRRRS347
# return the amount of advanced market risk weighted assets overtime
def get_riskweighted_asset_item_overtime(quarter_date_from, quarter_date_to):
    # TODO: Store this company map in a csv?
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
    advanced_market_risk_weighted_assets_ID = ['MRRRS347']
    data = raw_data.query('Item_ID in @advanced_market_risk_weighted_assets_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

# VaR based measure overtime
# return the amount of VaR-based measure overtime
def get_var_measure_item_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
    VaR_based_measure_overtime_ID = ['MRRRS298']
    data = raw_data.query('Item_ID in @VaR_based_measure_overtime_ID and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

# sVaR VaR ratio overtime
# return the ratio of sVaR and VaR overtime
def get_ratio_item_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
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

# Diversification Overtime
# return the amount of diversification as a percentage of VaR overtime
def get_var_diversification_item_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = data_asset.reset_index()
    data_asset['Item']=data_asset.Item.astype(int)
    data_asset['total_asset_var']=data_asset.groupby(['Company','Quarter'])['Item'].transform('sum')

    varID = ['MRRRS298']
    data_day_var = raw_data.query('Item_ID in @varID and Quarter<= @quarter_date_to and '
                                  'Quarter >= @quarter_date_from')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item']=data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data.update(data.groupby(['Company','Quarter']).ffill())

    data['total_asset_var'] = data.total_asset_var.astype(int)
    data = data.loc[data.Item_ID == 'MRRRS298']

    data['diver_as_percent_of_Var'] = 100 * (data.total_asset_var-data.Item)/data.total_asset_var

    output_data = data.groupby('Company')[['Quarter', 'diver_as_percent_of_Var']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res

# Asset Diversification Overtime
# return VaR percentage in different asset classes and diversification effect of companies in specific quarters
def get_asset_class_var_item_byquarter(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    # Previous day's VaR: IR='MRRRS348' Debt='MRRRS349' Equity='MRRRS350' FX='MRRRS351' Commodities='MRRRS352'
    asset_dict = {'MRRRS348': 'IR',
                  'MRRRS349': 'Debt',
                  'MRRRS350': 'Equity',
                  'MRRRS351': 'FX',
                  'MRRRS352': 'Commodities',
                  'MRRRS298': 'Diversification'}

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
        (data.loc[data.Item_ID=='MRRRS298', 'Item']-data.loc[data.Item_ID=='MRRRS298', 'total_asset_var'])/ \
        data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var']
    data.sort_values(by='Company', inplace=True)
    output_data = data.groupby('Item_ID')[['Company', 'asset_var_by_percentage']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res

# Num of Breach overtime
# return the amount of the number of VaR breaches overtime
def get_num_var_breach_item_overtime(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data = get_data('FFIEC102')
    item_names = ['MRRRS362']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res

# Risk weighted assets
# return the amount of standardized market risk-weighted assets breakdown by bank in specific quarters
#def standardized_risk_weighted_assets(quarter_date_from, quarter_date_to):
def get_standardized_risk_weighted_assets_byquarter(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}

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

# return trading asset to risk ratio in specific quarters, the ratios order is: 'Net/VaR', 'Gross/VaR', 'Net/sVaR', 'Gross/sVaR'
def get_asset_to_var_ratio_item_byquarter(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data_var = get_data('FFIEC102')
    raw_data_asset = get_data('FRY9C')
    var_item_names = ['MRRRS298', 'MRRRS302']
    data_var = raw_data_var.query('Item_ID in @var_item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from').reset_index()
    
    data_var1 = data_var[data_var['Item_ID']=='MRRRS298'].rename(columns={'Item': 'VaR'}).drop(['Item_ID'], axis=1)
    data_var2 = data_var[data_var['Item_ID']=='MRRRS302'].rename(columns={'Item': 'sVaR'}).drop(['Item_ID'], axis=1)
    data_var = pd.merge(data_var1, data_var2, on=['Company', 'Quarter']).reset_index(drop=True)
    data_var[['VaR', 'sVaR']] = data_var[['VaR', 'sVaR']].astype('int')
    
    trading_asset_item_names_asset = ['BHCK3545']
    trading_asset_item_names_liability = ['BHCK3548']
    trading_asset_item_names = ['BHCK3545','BHCK3548']
    data = raw_data_asset.query('Item_ID in @trading_asset_item_names and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    data_asset = raw_data_asset.query('Item_ID in @trading_asset_item_names_asset and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data_liability = raw_data_asset.query('Item_ID in @trading_asset_item_names_liability and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data_asset.loc[:, 'Item_2'] = data_liability.loc[:, 'Item']
    data_asset.loc[:, 'Gross'] = data_asset.loc[:, 'Item'].astype(int) + data_asset.loc[:, 'Item_2'].astype(int)
    data_asset.loc[:, 'Net'] = data_asset.loc[:, 'Item'].astype(int) - data_asset.loc[:, 'Item_2'].astype(int)
    data_asset = data_asset.drop(['Item','Item_2', 'Item_ID'], axis=1)
    data_asset = data_asset.reset_index()
    
    tot_data = pd.merge(data_var, data_asset, on=['Company', 'Quarter'])
    
    
    tot_data['Net/VaR'] = tot_data['Net'] / tot_data['VaR']
    tot_data['Gross/VaR'] = tot_data['Gross'] / tot_data['VaR']
    tot_data['Net/sVaR'] = tot_data['Net'] / tot_data['sVaR']
    tot_data['Gross/sVaR'] = tot_data['Gross'] / tot_data['sVaR']
    tot_data = tot_data.drop(['VaR', 'sVaR', 'Gross', 'Net'], axis=1)
    # You can just remember the name and order of this 4 things...
    total_data = tot_data.groupby('Company')[['Net/VaR', 'Gross/VaR', 'Net/sVaR', 'Gross/sVaR']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res
    
# return trading revenue to VaR and sVaR ratios in specific quarters, the ratios order is: 'revenue/VaR', 'revenue/sVaR'
def get_revenue_to_var_ratio_item_byquarter(quarter_date_from, quarter_date_to):
    comp_dict = {'1073757': 'BAC',
                 '1951350': 'CITI',
                 '2380443': 'GS',
                 '1039502': 'JPMC',
                 '2162966': 'MS',
                 '1120754': 'WF'}
    raw_data_var = get_data('FFIEC102')
    raw_data_revenue = get_data('FRY9C')
    var_item_names = ['MRRRS298', 'MRRRS302']
    data_var = raw_data_var.query('Item_ID in @var_item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from').reset_index()
    
    data_var1 = data_var[data_var['Item_ID']=='MRRRS298'].rename(columns={'Item': 'VaR'}).drop(['Item_ID'], axis=1)
    data_var2 = data_var[data_var['Item_ID']=='MRRRS302'].rename(columns={'Item': 'sVaR'}).drop(['Item_ID'], axis=1)
    data_var = pd.merge(data_var1, data_var2, on=['Company', 'Quarter']).reset_index(drop=True)
    data_var[['VaR', 'sVaR']] = data_var[['VaR', 'sVaR']].astype('int')
    
    trading_revenue_item_names = ['BHCKA220']
    data_revenue = raw_data_revenue.query('Item_ID in @trading_revenue_item_names and Quarter <= @quarter_date_to and '
                                'Quarter >= @quarter_date_from')
    
    tot_data = pd.merge(data_var, data_revenue, on=['Company', 'Quarter']).rename(columns={'Item': 'revenue'})
    tot_data['revenue/VaR'] = tot_data['revenue'].astype(int) / tot_data['VaR']
    tot_data['revenue/sVaR'] = tot_data['revenue'].astype(int) / tot_data['sVaR']
    tot_data = tot_data.drop(['VaR', 'sVaR', 'revenue', 'Item_ID'], axis=1)
    # You can just remember the name and order of these 2 things...
    total_data = tot_data.groupby('Company')[['revenue/VaR', 'revenue/sVaR']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res
    
