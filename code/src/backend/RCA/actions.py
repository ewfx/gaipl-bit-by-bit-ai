import json
# from firebase import db
from supabase_module import return_CI_data, return_grafana_data, return_servicenow_data
def get_all_incidents():

    servicenow_data = return_servicenow_data()['records']
    incidents_data = []
    for data in servicenow_data:
        if data['sys_class_name'].lower()=="incident":
            incidents_data.append(data)
    return incidents_data

def get_all_changes():
    servicenow_data = return_servicenow_data()['records']
    change_data = []
    for data in servicenow_data:
        if data['sys_class_name'].lower()=="change":
            change_data.append(data)
    return change_data

def get_all_data():
    servicenow_data = return_servicenow_data()['records']
    all_data = []
    for data in servicenow_data:
        all_data.append(data)
    return all_data

def get_data_assigned_group(assigned_group):
    servicenow_data = return_servicenow_data()['records']
    incidents_data =[]
    change_data = []
    for data in servicenow_data:
        if data['assigned_group'].lower()==assigned_group.lower():
            if data['sys_class_name'].lower() == "incident":
                incidents_data.append(data)
            elif data['sys_class_name'].lower() == "change":
                change_data.append(data)
    return {'incidents_data':incidents_data, 'change_data':change_data}
