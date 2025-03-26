import json
# from firebase import db
from firebase import db
def get_all_incidents():

    # servicenow_data = return_servicenow_data()['records']
    servicenow_data_ref  = db.collection("Service_Now").stream()
    incidents_data = []
    for s_data in servicenow_data_ref:
        data = s_data.to_dict()
        if data['sys_class_name'].lower()=="incident":
            incidents_data.append(data)
    return incidents_data

def get_all_changes():
    servicenow_data_ref  = db.collection("Service_Now").stream()
    change_data = []
    for s_data in servicenow_data_ref:
        data = s_data.to_dict()
        if data['sys_class_name'].lower()=="change":
            change_data.append(data)
    return change_data

def get_all_data():
    servicenow_data_ref  = db.collection("Service_Now").stream()
    all_data = []
    for s_data in servicenow_data_ref:
        data = s_data.to_dict()
        all_data.append(data)
    return all_data

def get_data_assigned_group(assigned_group):
    servicenow_data_ref  = db.collection("Service_Now").stream()
    incidents_data =[]
    change_data = []
    for s_data in servicenow_data_ref:
        data = s_data.to_dict()
        if data['assigned_group'].lower()==assigned_group.lower():
            if data['sys_class_name'].lower() == "incident":
                incidents_data.append(data)
            elif data['sys_class_name'].lower() == "change":
                change_data.append(data)
    return {'incidents_data':incidents_data, 'change_data':change_data}
