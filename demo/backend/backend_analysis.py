import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math

### clearing data
raw_data = pd.read_csv(r'F:\UChicago\PJLAB2\EYPJLABV2.0\demo\backend\data\FFIEC102.csv',parse_dates=[1])
raw_data.columns = ['Company','Date','Item_ID','Item']
raw_data['Quarter'] = pd.PeriodIndex(raw_data['Date'],freq='Q')
raw_data = raw_data.drop(['Date'],axis = 1)
raw_data = raw_data.set_index(['Company','Quarter'])
raw_data.sort_index(inplace=True)

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


data_Item_list_DeMinimis = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Comprehensive = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_Incremental = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_AddOns = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_VAR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_sVAR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])

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

    data_Item_list_DeMinimis = pd.concat([data_Item_list_DeMinimis, data_Item_DeMinimis])
    data_Item_list_Comprehensive = pd.concat([data_Item_list_Comprehensive, data_Item_Comprehensive])
    data_Item_list_Incremental = pd.concat([data_Item_list_Incremental, data_Item_Incremental])
    data_Item_list_AddOns = pd.concat([data_Item_list_AddOns, data_Item_AddOns])
    data_Item_list_VAR = pd.concat([data_Item_list_VAR, data_Item_VAR])
    data_Item_list_sVAR = pd.concat([data_Item_list_sVAR, data_Item_sVAR])


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

de_min = plt.bar(index, data_Item_list_DeMinimis["MRRRS343"].astype(int), bar_width,
                label="De minimis positions and other adjustment",)

com_pre = plt.bar(index, data_Item_list_Comprehensive["MRRRH327"].astype(int),
                 bar_width, label="Standardized comprehensive risk measure",bottom=de_minimis)

inc_risk = plt.bar(index, data_Item_list_Incremental["MRRRS313"].astype(int),
                 bar_width, label="Incremental risk capital requirement",bottom=de_minimis+comprehensive)

add_on = plt.bar(index, data_Item_list_AddOns["MRRRS311"].astype(int),
                 bar_width, label="Standardized measure of specific risk add-ons",bottom=de_minimis+comprehensive+incremental)

VaR_2 = plt.bar(index, data_Item_list_VAR["MRRRS298"].astype(int), bar_width,
                label="VaR-based capital", bottom=de_minimis+comprehensive+incremental+adds_on)

sVaR_2 = plt.bar(index, data_Item_list_sVAR["MRRRS302"].astype(int),
                 bar_width, label="sVaR-based capital",bottom=de_minimis+comprehensive+incremental+adds_on+stacked_var)

plt.xlabel('Company')
plt.ylabel('Amount')
plt.title('Standardized market risk-weighted assets breakdown by bank')
plt.xticks(index,Company_list_new)
plt.legend(loc="lower center",bbox_to_anchor=(0.5, 0))
plt.show()

