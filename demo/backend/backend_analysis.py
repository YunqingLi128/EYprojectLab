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

### Capture Company and Quarters
##For test
#Company_list = ['Bank of America', 'Citigroup','Goldman Sachs','JP Morgan']
#date = '2017Q4'
date = year + 'Q' + quarter
idx = pd.IndexSlice

### Data Analysis
## 1.1 VaR and sVaR
#MRRRS298 = VaR
#MRRRS302 = sVaR

data_Item_list_VAR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])
data_Item_list_sVAR = pd.DataFrame(columns=['Company','Quarter','Item_ID','Item'])

for i in Company_list:
    data = raw_data.loc[(Comp_dict[i],idx[date])]

    data_Item_VAR = data.loc[data['Item_ID'] == 'MRRRS298'].reset_index()
    data_Item_sVAR = data.loc[data['Item_ID'] == 'MRRRS302'].reset_index()

    data_Item_list_VAR = pd.concat([data_Item_list_VAR, data_Item_VAR])
    data_Item_list_sVAR = pd.concat([data_Item_list_sVAR, data_Item_sVAR])

data_Item_list_VAR = data_Item_list_VAR.drop(['Quarter'], axis=1)
data_Item_list_VAR = data_Item_list_VAR.pivot(index='Company', columns='Item_ID', values='Item')

data_Item_list_sVAR = data_Item_list_sVAR.drop(['Quarter'], axis=1)
data_Item_list_sVAR = data_Item_list_sVAR.pivot(index='Company', columns='Item_ID', values='Item')

Company_list_new = []
for i in data_Item_list_VAR.index:
    Company_list_new.append(Inv_comp_dict[i])

## 1.2 Plot Bar Graph
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



