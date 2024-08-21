import pandas as pd
from django.shortcuts import render
import os

print('Running')


Recent_Context = {}

#All paths
#path = f'"C:\Users\Mohamed Khalil\Desktop\Custodian\custodian\custodian\Resources\PATHS.xlsx"'



groups_path = r'C:\Users\Mohamed Khalil\Desktop\Custodian_IAM\Resources\groups'
RBAC_df = pd.read_excel(r'C:\Users\Mohamed Khalil\Desktop\Custodian_IAM\Resources\RBAC Sample.xlsx')
HR_df = pd.read_excel(r'C:\Users\Mohamed Khalil\Desktop\Custodian_IAM\Resources\HR Sheet - Dummy Data.xlsx')


def groups_handler(request):
    global Recent_Context
    context = Recent_Context
    id = context['id']

    app_name = request.GET.get('app_name')
    path = f'{groups_path}\{app_name}_groups.xlsx'

    # Check if the file exists
    if os.path.exists(path):
        df = pd.read_excel(path)
        groups_list = df[df['ID'] == id]['Group'].tolist()

        if not groups_list:
            groups_list = ["No groups available"]
    else:
        groups_list = ["No groups available"]

    context['groups'] = groups_list

    return render(request, 'dashboard/index.html', context)




def handler(request):
    global Recent_Context
    if(request.GET.get('q') == None):
        return render(request, 'dashboard/index.html', {})

    context = {}

    context['title'] = ''

    status = 'Found'
    query = request.GET.get('q')
    print(query)
    HR_data = HR_df[HR_df['ID'] == query]
    HR_data_dict = {}

    if(len(HR_data) == 0):
        status = 'Not Found'
    else:
        context['id'] = HR_data['ID'].values[0]
        context['name'] = HR_data['Employee Name'].values[0]
        context['state'] = HR_data['الحالة'].values[0]
        context['title'] = HR_data['Functional Title English'].values[0]
        context['sector'] = HR_data['Sector'].values[0]
        context['division'] = HR_data['Division'].values[0]
        context['location'] = HR_data['Location'].values[0]
        context['managerID'] = HR_data['Line Manager E0'].values[0]
        context['manager'] = HR_data['Line Manager'].values[0]
        context['cc'] = HR_data['Cost Center'].values[0]
        context['ccDisc'] = HR_data['Cost Center Description'].values[0]
        context['apps'] = get_application(HR_data)

        id = context.get('id')
        title = context.get('title')
        context['RBAC'] = RBAC_apps(title)

        context['recent'] = daily_data(id)

    Recent_Context = context

    return render(request, 'dashboard/index.html', context)


def get_application(df):
    apps = df.iloc[-1, -7:]
    apps_access = apps[apps == 'X'].index.tolist()

    apps_access = apps_access

    return apps_access


def RBAC_apps(title):
    rbac = pd.read_excel(r'C:\Users\Mohamed Khalil\Desktop\Custodian_IAM\Resources\RBAC Sample.xlsx')
    row = rbac[rbac['Functional Title English'] == title]


    result = {}
    for col in row.columns[1::]:  # Iterate through each column in the row
        if row[col].values[0] != 'Not Eligible':  # Check if the value is different from 'Not Eligible'
            result[col] = row[col].values[0]  # Add to the result dictionary'''

    return result


def daily_data(id):

    df = pd.read_excel(r'C:\Users\Mohamed Khalil\Desktop\Custodian_IAM\Resources\Daily Sheet Sample.xlsx')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.rename(columns={'Branch/Department':'branch'})
    rows = df[df['E0'] == id]
    rows = rows.sort_values(by='Date', ascending=False)

    topfive = rows.head(10)

    recent = topfive.to_dict(orient='records')

    print(recent)


    return recent



