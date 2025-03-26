# from openai import OpenAI
import os
from dotenv import load_dotenv
from CI_agent.actions import get_CI_health
from CI_agent.actions import CI_node_down
from CI_agent.actions import CI_node_up
# from jsonhelper import extract_json
from CI_agent.actions import get_grafana_data
from CI_agent.actions import get_alert_data
from CI_agent.actions import get_ci_incidents_changes
from CI_agent.jsonhelper import extract_json
from CI_agent.prompts import system_prompts
load_dotenv()
from groq import Groq
from firebase import get_env_keys
def generate_text_with_conversations(messages):
        
        client = Groq(api_key=get_env_keys()["GROQ_API_KEY_1"])
        response = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        model="qwen-2.5-32b",
        # model = "qwen-2.5-coder-32b",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
        )
        output_stat = ""
        for chunk in response:
            # print(chunk.choices[0].delta.content or "", end="")
            if chunk.choices[0].delta.content != None:
                output_stat = output_stat + chunk.choices[0].delta.content
        return output_stat
def ci_ai(session_data,user_prompt):
    available_actions = {
        "get_CI_health": get_CI_health,
        "CI_node_up":CI_node_up,
        "CI_node_down":CI_node_down,
        "get_grafana_data": get_grafana_data,
        "get_alert_data": get_alert_data,
        "get_ci_incidents_changes": get_ci_incidents_changes
    }

    messages = [{"role":"system","content":system_prompts}]
    msg = session_data['messages'].copy()
    messages = messages + msg
    messages.append({"role":"user","content":user_prompt})
    turn_count = 1
    max_turns = 3

    response_list = []
    while turn_count < max_turns:
        print (f"Loop: {turn_count}")
        print("----------------------")
        turn_count += 1

        response = generate_text_with_conversations(messages)

        # print(response)

        json_function = extract_json(response)
        
        # print("\n\n\njson_function::",json_function)
        if json_function:
                if 'function_name' not in json_function[0].keys():
                    break
                function_name = json_function[0]['function_name']
                function_parms = json_function[0]['function_params']
                if function_name not in available_actions:
                    raise Exception(f"Unknown action: {function_name}: {function_parms}")
                # print(f" -- running {function_name} {function_parms}")
                action_function = available_actions[function_name]
                #call the function
                result = action_function(**function_parms)
                function_result_message = f"Action_Response: {result}"
                messages.append({"role": "user", "content": function_result_message})
                # print(function_result_message)
                response_list.append(response)
        else:
            break
    messages.append({"role":"user","content":"So from the discussion get me the final proper only answer I am not focused on the action plan and all just give me the answer which I can display to the user."})
    final_response = generate_text_with_conversations(messages)
    # print("final_response:",final_response)
    return final_response


