import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import json

### clearing data
raw_data = pd.read_csv(r'./data/FFIEC102.csv')
raw_data.columns = ['Company','Quarter','Item_ID','Item']
# raw_data['Quarter'] = pd.PeriodIndex(raw_data['Date'],freq='Q')
# raw_data = raw_data.drop(['Date'],axis = 1)
raw_data = raw_data.set_index(['Company','Quarter'])
raw_data.sort_index(inplace=True)
# print(raw_data)

## Company dictionary capture
Comp_dict = {'Bank of America': 1073757, 'Citigroup': 1951350, 'Goldman Sachs': 2380443, 'JP Morgan': 1039502, 'Morgan Stanley': 2162966, 'Wells Fargo': 1120754}
Inv_comp_dict = {v: k for k, v in Comp_dict.items()}

### user input
'''
Company_list = []
input_flag_Company = True
print('Enter a list of company name, type “exit” to exit:')
while input_flag_Company == True:
    company_name = input()
    if company_name == 'exit':
        input_flag = False
        break
    Company_list.append(company_name)

print('Enter a year you want to analyze:')
year = input()

print('Enter a quarter you want to analyze:')
quarter = input()
'''
### Capture Company and Quarters
##For test
Company_list = ['Bank of America', 'Citigroup','Goldman Sachs','JP Morgan']
date = '2017Q4'
#date = year + 'Q' + quarter
idx = pd.IndexSlice

### Data Analysis
#MRRRS343 = De minimis
#MRRRH327 or MRRRH323 = Standardized comprehensive risk measure
#MRRRS313 = Incremental risk capital requirement
#MRRRS311 = Standardized measure of specific risk add-ons
#MRRRS302 = sVaR
#MRRRS298 = VaR


# Yaoqi's test
def get_data():
    df = pd.read_csv('./data/FFIEC102.csv', dtype=str)
    df.columns = ['Company', 'Quarter', 'Item_ID', 'Item']
    df = df.set_index(['Company', 'Quarter'])
    df.sort_index(inplace=True)
    return df


# previous day's Value-at-risk (VaR)-based measure
# IR, Debt, Equity, FX, Commodities
# return JSON: {id: [{item_name_1: item_value_1}, {item_name_2: item_value_2}]
def test_asset_VaR_query(quarter_date):
    raw_data = get_data()
    asset_VaR_item_names = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    data = raw_data.query('Item_ID in @asset_VaR_item_names and Quarter == @quarter_date')
    # print(data)
    asset_VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    for k, v in asset_VaR_data.items():
        asset_VaR_data[k] = list(map(lambda x: {x[0]: x[1]}, v))
    res = json.dumps(asset_VaR_data)
    print(res)
    # data.reset_index(inplace=True)
    # data.set_index(['Company', 'Quarter', 'Item_ID'], inplace=True)
    # result = data.to_json(orient="index", indent=4)
    # print(result)


# Previous day's VaR-based measure and Most recent stressed VaR-based measure
# return JSON: {id: [[item_name_1, item_value_1], [item_name_2: item_value_2]]
def test_VaR_sVarR_query(quarter_date):
    VaR_item_names = ['MRRRS298', 'MRRRS302']
    data = raw_data.query('Item_ID in @VaR_item_names and Quarter == @quarter_date')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = json.dumps(VaR_data)
    print(res)


test_asset_VaR_query(date)
test_VaR_sVarR_query(date)

data_Item_list_DeMinimis = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Comprehensive = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Incremental = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_AddOns = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_VAR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_sVAR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])

data_Item_list_IR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Debt = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Equity = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Fx = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Commodities = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])

for i in Company_list:
    data = raw_data.loc[(Comp_dict[i],idx[date])]

    data_Item_DeMinimis = data.loc[data['Item_ID'] == 'MRRRS343'].reset_index()
    if data.loc[data['Item_ID'] == 'MRRRH327'].empty:
        data_Item_Comprehensive = data.loc[data['Item_ID'] == 'MRRRH323'].reset_index()
        data_Item_Comprehensive['Item_ID'] = 'MRRRH327'
    else:
        data_Item_Comprehensive = data.loc[data['Item_ID'] == 'MRRRH327'].reset_index()
    data_Item_Incremental = data.loc[data['Item_ID'] == 'MRRRS313'].reset_index()
    data_Item_AddOns = data.loc[data['Item_ID'] == 'MRRRS311'].reset_index()
    data_Item_VAR = data.loc[data['Item_ID'] == 'MRRRS298'].reset_index()
    data_Item_sVAR = data.loc[data['Item_ID'] == 'MRRRS302'].reset_index()

    data_Item_IR = data.loc[data['Item_ID'] == 'MRRRS354'].reset_index()
    data_Item_Debt = data.loc[data['Item_ID'] == 'MRRRS355'].reset_index()
    data_Item_Equity = data.loc[data['Item_ID'] == 'MRRRS356'].reset_index()
    data_Item_Fx = data.loc[data['Item_ID'] == 'MRRRS357'].reset_index()
    data_Item_Commodities = data.loc[data['Item_ID'] == 'MRRRS358'].reset_index()

    data_Item_list_DeMinimis = pd.concat([data_Item_list_DeMinimis, data_Item_DeMinimis])
    data_Item_list_Comprehensive = pd.concat([data_Item_list_Comprehensive, data_Item_Comprehensive])
    data_Item_list_Incremental = pd.concat([data_Item_list_Incremental, data_Item_Incremental])
    data_Item_list_AddOns = pd.concat([data_Item_list_AddOns, data_Item_AddOns])
    data_Item_list_VAR = pd.concat([data_Item_list_VAR, data_Item_VAR])
    data_Item_list_sVAR = pd.concat([data_Item_list_sVAR, data_Item_sVAR])

    data_Item_list_IR=pd.concat([data_Item_list_IR,data_Item_IR])
    data_Item_list_Debt=pd.concat([data_Item_list_Debt,data_Item_Debt])
    data_Item_list_Equity=pd.concat([data_Item_list_Equity,data_Item_Equity])
    data_Item_list_Fx=pd.concat([data_Item_list_Fx,data_Item_Fx])
    data_Item_list_Commodities=pd.concat([data_Item_list_Commodities,data_Item_Commodities])

data_Item_list_DeMinimis = data_Item_list_DeMinimis.drop(['Quarter'], axis=1)
data_Item_list_DeMinimis = data_Item_list_DeMinimis.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_Comprehensive = data_Item_list_Comprehensive.drop(['Quarter'], axis=1)
data_Item_list_Comprehensive = data_Item_list_Comprehensive.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_Incremental = data_Item_list_Incremental.drop(['Quarter'], axis=1)
data_Item_list_Incremental = data_Item_list_Incremental.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_AddOns = data_Item_list_AddOns.drop(['Quarter'], axis=1)
data_Item_list_AddOns = data_Item_list_AddOns.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_VAR = data_Item_list_VAR.drop(['Quarter'], axis=1)
data_Item_list_VAR = data_Item_list_VAR.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_sVAR = data_Item_list_sVAR.drop(['Quarter'], axis=1)
data_Item_list_sVAR = data_Item_list_sVAR.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_IR = data_Item_list_IR.drop(['Quarter'], axis=1)
data_Item_list_IR = data_Item_list_IR.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_Debt = data_Item_list_Debt.drop(['Quarter'], axis=1)
data_Item_list_Debt = data_Item_list_Debt.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_Equity = data_Item_list_Equity.drop(['Quarter'], axis=1)
data_Item_list_Equity = data_Item_list_Equity.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_Fx = data_Item_list_Fx.drop(['Quarter'], axis=1)
data_Item_list_Fx = data_Item_list_Fx.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_Commodities = data_Item_list_Commodities.drop(['Quarter'], axis=1)
data_Item_list_Commodities = data_Item_list_Commodities.pivot(index='Company', columns='Item_ID', values='Item')


Company_list_new = []
for i in data_Item_list_VAR.index:
    Company_list_new.append(Inv_comp_dict[i])

## Plot Bar Graph for sVaR and VaR
index = np.arange(len(Company_list))
bar_width = 0.35

fig, ax = plt.subplots()
VaR = ax.bar(index, data_Item_list_VAR["MRRRS298"].astype(int), bar_width,
                label="VaR")

sVaR = ax.bar(index+bar_width, data_Item_list_sVAR["MRRRS302"].astype(int),
                 bar_width, label="sVaR")

ax.set_xlabel('Company')
ax.set_ylabel('Amount')
ax.set_title(date + ' VaR and sVaR')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(Company_list_new)
ax.legend()
plt.show()

## Plot risk-weighted asset breakdown
index = np.arange(len(Company_list))
bar_width = 0.35

de_minimis = data_Item_list_DeMinimis["MRRRS343"].astype(int)
comprehensive=data_Item_list_Comprehensive['MRRRH327'].astype(int)
incremental=data_Item_list_Incremental['MRRRS313'].astype(int)
adds_on=data_Item_list_AddOns['MRRRS311'].astype(int)
stacked_var=data_Item_list_VAR['MRRRS298'].astype(int)
stacked_svar=data_Item_list_sVAR['MRRRS302'].astype(int)

de_min = plt.bar(index, de_minimis, bar_width,
                label="De minimis positions and other adjustment",)

com_pre = plt.bar(index, comprehensive,
                 bar_width, label="Standardized comprehensive risk measure",bottom=de_minimis)

inc_risk = plt.bar(index, incremental,
                 bar_width, label="Incremental risk capital requirement",bottom=de_minimis+comprehensive)

add_on = plt.bar(index, adds_on,
                 bar_width, label="Standardized measure of specific risk add-ons",bottom=de_minimis+comprehensive+incremental)

VaR_2 = plt.bar(index, stacked_var, bar_width,
                label="VaR-based capital", bottom=de_minimis+comprehensive+incremental+adds_on)

sVaR_2 = plt.bar(index, stacked_svar,
                 bar_width, label="sVaR-based capital",bottom=de_minimis+comprehensive+incremental+adds_on+stacked_var)

plt.xlabel('Company')
plt.ylabel('Amount')
plt.title('Standardized market risk-weighted assets breakdown by bank')

for r1, r2, r3, r4, r5, r6 in zip(de_min,com_pre,inc_risk, add_on, VaR_2, sVaR_2):
    h1 = r1.get_height()
    h2 = r2.get_height()
    h3 = r3.get_height()
    h4 = r4.get_height()
    h5 = r5.get_height()
    h6 = r6.get_height()
    plt.text(r1.get_x() + r1.get_width() / 2., h1 / 2., "%d" % h1, ha="center", va="center", color="white", fontsize=8)
    plt.text(r2.get_x() + r2.get_width() / 2., h1 + h2 / 2., "%d" % h2, ha="center", va="center", color="white",
             fontsize=8)
    plt.text(r3.get_x() + r3.get_width() / 2., h1 + h2 + h3 / 2., "%d" % h3, ha="center", va="center", color="white",
             fontsize=8)
    plt.text(r4.get_x() + r4.get_width() / 2., h1 + h2 + h3 + h4 / 2., "%d" % h4, ha="center", va="center", color="white",
             fontsize=8)
    plt.text(r5.get_x() + r5.get_width() / 2., h1 + h2 + h3 +h4 + h5 / 2., "%d" % h5, ha="center", va="center", color="white",
             fontsize=8)
    plt.text(r6.get_x() + r5.get_width() / 2., h1 + h2 + h3 + h4 + h5 +h6 / 2., "%d" % h6, ha="center", va="center",
             color="white", fontsize=8)
plt.xticks(index,Company_list_new)
plt.legend(loc="upper center",bbox_to_anchor=(0.5, 0))
plt.show()

##plot VaR by Asset Class and Diversification Effect
index = np.arange(len(Company_list))
bar_width = 0.35

IR = data_Item_list_IR["MRRRS354"].astype(int)
Debt=data_Item_list_Debt['MRRRS355'].astype(int)
Equity=data_Item_list_Equity['MRRRS356'].astype(int)
Fx=data_Item_list_Fx['MRRRS357'].astype(int)
Commodities=data_Item_list_Commodities['MRRRS358'].astype(int)

int_rate = plt.bar(index, IR, bar_width, label="IR")

var_debt = plt.bar(index, Debt, bar_width, label="Debt",bottom=IR)

var_equity = plt.bar(index, Equity, bar_width, label="Equity",bottom=IR+Debt)

var_Fx = plt.bar(index, Fx, bar_width, label="FX", bottom=IR+Debt+Equity)

var_commodities = plt.bar(index, Commodities, bar_width, label="Commodities",bottom=IR+Debt+Equity+Fx)

plt.xlabel('Company')
plt.ylabel('Amount')
plt.title('VaR by Asset Class and Diversification Effect')

for r1, r2, r3, r4, r5 in zip(int_rate,var_debt,var_equity, var_Fx, var_commodities):
    h1 = r1.get_height()
    h2 = r2.get_height()
    h3 = r3.get_height()
    h4 = r4.get_height()
    h5 = r5.get_height()
    plt.text(r1.get_x() + r1.get_width() / 2., h1 / 2., "%d" % h1, ha="center", va="center", color="black", fontsize=8)
    plt.text(r2.get_x() + r2.get_width() / 2., h1 + h2 / 2., "%d" % h2, ha="center", va="center", color="black",
             fontsize=8)
    plt.text(r3.get_x() + r3.get_width() / 2., h1 + h2 + h3 / 2., "%d" % h3, ha="center", va="center", color="black",
             fontsize=8)
    plt.text(r4.get_x() + r4.get_width() / 2., h1 + h2 + h3 + h4 / 2., "%d" % h4, ha="center", va="center", color="black",
             fontsize=8)
    plt.text(r5.get_x() + r5.get_width() / 2., h1 + h2 + h3 +h4 + h5 / 2., "%d" % h5, ha="center", va="center", color="black",
             fontsize=8)


plt.xticks(index,Company_list_new)
plt.legend(loc="upper center",bbox_to_anchor=(0.5, 0))
plt.show()