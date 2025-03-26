from dotenv import load_dotenv
from troubleshoot.actions import get_confluence_page
from troubleshoot.prompt import system_prompt
from troubleshoot.json_help import extract_json
from groq import Groq
from supabase_module import return_supabase_env_keys
# Load environment variables
from troubleshoot.prompt import system_prompt
load_dotenv()

# Create an instance of the OpenAI class



client = Groq(
    api_key= return_supabase_env_keys()['GROQ_API_KEY_2']
)


def generate_text_with_conversation(messages, model = "llama-3.3-70b-versatile", access = return_supabase_env_keys()['HF_ACESS']):
    response = client.chat.completions.create(
        model=model,
        messages=messages
        )
    return response.choices[0].message.content


def get_troubleshoot(session_data,user_prompt):
    #Available actions are:
    available_actions = {
        "get_confluence_page":get_confluence_page
    }

    # user_prompt = "How to create terraform workspace?"
    # user_prompt = "What is a provider in terraform?"

    messages = [{"role":"system","content":system_prompt}]
    msg = session_data['messages'].copy()
    messages = messages + msg
    messages.append({"role":"user","content":user_prompt})

    turn_count = 1
    max_turns = 5


    while turn_count < max_turns:
        print (f"Loop: {turn_count}")
        print("----------------------")
        turn_count += 1

        response = generate_text_with_conversation(messages, model="llama-3.3-70b-versatile", access = return_supabase_env_keys()['HF_ACESS'])

        # print(response)

        json_function = extract_json(response)
        # print(json_function)

        if json_function:
                function_name = json_function[0]['function_name']
                function_params = json_function[0]['function_params']
                if function_name not in available_actions:
                    raise Exception(f"Unknown action: {function_name}: {function_params}")
                # print(f" -- running {function_name} {function_params}")
                action_function = available_actions[function_name]
                #call the function
                result = action_function(**function_params)
                function_result_message = f"Action_Response: {result}"
                messages.append({"role": "user", "content": function_result_message})
                # print(function_result_message)
        else:
            break

    messages.append({"role":"user","content":"So from the discussion get me the final proper only answer I am not focused on the action plan and all just give me the answer which I can display to the user."})
    final_response = generate_text_with_conversation(messages)
    return final_response

