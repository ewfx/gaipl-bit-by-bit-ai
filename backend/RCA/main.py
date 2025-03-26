import os
from dotenv import load_dotenv
# from jsonhelper import extract_json
from RCA.actions import get_all_changes
from RCA.actions import get_all_data
from RCA.actions import get_all_incidents
from RCA.actions import get_data_assigned_group
from RCA.jsonhelper import extract_json
from RCA.prompts import system_prompts
load_dotenv()
from groq import Groq
from supabase_module import return_supabase_env_keys

def generate_text_with_conversations(messages,model="llama-3.3-70b-versatile"):
        client = Groq(api_key=return_supabase_env_keys()["GROQ_API_KEY_2"])
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

def rca_ai(session_data,user_prompt):
    
    available_actions = {
        "get_all_data": get_all_data,
        "get_all_incidents": get_all_incidents,
        "get_all_changes": get_all_changes,
        "get_data_assigned_group": get_data_assigned_group
        
    }

    messages = [{"role":"system","content":system_prompts}]
    msg = session_data['messages'].copy()
    messages = messages + msg

    #getting user inputs interactive
    messages.append({"role":"user","content":user_prompt})
    turn_count = 1
    max_turns = 5

    response_list = []
    while turn_count < max_turns:
        print (f"Loop: {turn_count}")
        print("----------------------")
        turn_count += 1

        response = generate_text_with_conversations(messages)

        print(response)

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
        
# rca_ai([],"what is you are doing")

