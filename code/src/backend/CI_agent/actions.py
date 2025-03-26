from datetime import datetime, timedelta
from firebase import db

# Python scripts
def get_CI_health(CI_number):
    print("get_CI_health")
    # ci_data = return_CI_data()
    # ci_output = []
    # for data in ci_data:
    #     if data["ci-id"].lower()==CI_number.lower():
    #         ci_output.append(data)
    #         return ci_output
    ci_data = db.collection("CI_DATA").document(CI_number.lower()).get()
    if ci_data.to_dict()!=None:
        print("ci_data is not null")
        return ci_data.to_dict()
    print("ci_data:",ci_data)
    return {}
def CI_node_up(CI_number):
    print("CI_node_up")
    # ci_data = return_CI_data()
    # updated_ci_data = []
    # for data in ci_data:
    #     if data["ci-id"].lower()==CI_number.lower():
    #         data['ci-health'] = "up"
    #         updated_ci_data.append(data)
    #     else:
    #         updated_ci_data.append(data)
    # # Step 3: Write the updated JSON back to the file
    # updated_json_bytes = json.dumps(updated_ci_data, indent=4).encode("utf-8")
    # update_supabase_data("CI-data.json",updated_json_bytes)
    # # Upload the updated JSON back to Supabase
    if get_CI_health(CI_number)!={}:
        update_ref = db.collection("CI_DATA").document(CI_number.lower()).update({"ci-health":"up"})
        get_CI_health(CI_number)
        return get_CI_health(CI_number)
        
    return {}

def CI_node_down(CI_number):
    print("CI node down")
    # ci_data = return_CI_data()
    # updated_ci_data = []
    # for data in ci_data:
    #     if data["ci-id"].lower()==CI_number.lower():
    #         data['ci-health'] = "down"
    #         updated_ci_data.append(data)
    #     else:
    #         updated_ci_data.append(data)
    # # Step 3: Write the updated JSON back to the file
    # updated_json_bytes = json.dumps(updated_ci_data, indent=4).encode("utf-8")
    # update_supabase_data("CI-data.json",updated_json_bytes)
    # # Upload the updated JSON back to Supabase
    # return get_CI_health(CI_number)
    if get_CI_health(CI_number)!={}:
        update_ref = db.collection("CI_DATA").document(CI_number.lower()).update({"ci-health":"down"})
        get_CI_health(CI_number)
        return get_CI_health(CI_number)
        
    return {}

def get_grafana_data(CI_number):
    # print("get_grafana_data")
    # grafana_data = return_grafana_data()
    # # print(grafana_data)
    print("get_grafana_data")
    grafana_data_ref = db.collection("Grafana_data").stream()
    node_data = {}

    try:
        for g_data in grafana_data_ref:
            data = g_data.to_dict()
            if data['fields']['labels']['agent_hostname'] == CI_number:
                node_data = data
                break
    except:
        print("Something went wrong")
    
    return node_data

def get_alert_data(CI_number, factor, factor_string):
    alert_data=[]
    print("get_alert_data")
    # grafana_data = return_grafana_data()
    # print(factor)
    # print(factor_string)
    grafana_data_ref = db.collection("Grafana_data").stream()

    for g_data in grafana_data_ref:
        data = g_data.to_dict()
        if data['fields']['labels']['agent_hostname'] == CI_number:

            dahsboard_name = data['fields']['name']
            if factor_string in dahsboard_name.lower():
                values = data["Data"]["values"]

                time_interval = int((24*60)/len(values))

                # Get the current time
                current_time = datetime.now()

                # Calculate the start time (24 hours ago)
                start_time = current_time - timedelta(hours=24)

                # Generate timestamps for the last 24 hours 
                timestamps = [start_time + timedelta(minutes=time_interval * i) for i in range(len(values))]

                # Filter data where value > 8
                alert_data = [
                    {"timestamp": timestamps[i].strftime("%Y-%m-%d %H:%M:%S"), "value": value}
                    for i, value in enumerate(values) if value > int((8 * int(factor))/10)
                ]
                break

    # print("\n\n\nalert_data:",alert_data)
    print("-------------------------------")
    return alert_data

def get_ci_incidents_changes(CI_number):
    print("get_ci_incidents_changes")
    # servicenow_data = return_servicenow_data()['records']
    servicenow_data_ref = db.collection("Service_Now").stream()
    incidents_data = []
    change_data = []
    # print(servicenow_data)
    try:
        for s_data in servicenow_data_ref:
            data = s_data.to_dict()
            if data['cmdb_ci'].lower()==CI_number.lower():
                if data['sys_class_name'].lower()=="change":
                    change_data.append(data)
                elif data['sys_class_name'].lower()=="incident":
                    incidents_data.append(data)
    except Exception as e :
        print(f"Something wet wrong: {e}")

    return {"incidents":incidents_data, "changes":change_data}

