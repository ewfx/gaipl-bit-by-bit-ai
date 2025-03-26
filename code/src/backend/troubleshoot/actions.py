import json
import requests
from bs4 import BeautifulSoup
from supabase_module import return_supabase_env_keys
def view_to_plain_text(view_content):
    soup = BeautifulSoup(view_content, 'html.parser')
    # Get text content (this strips HTML tags)
    plain_text = soup.get_text(separator=' ', strip=True)
    return plain_text

def get_confluence_page(base_url):
    
    url = "https://someonsr045.atlassian.net/wiki/rest/api/content?type=page&limit=100"
    headers = {
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers, auth=("someonsr045@gmail.com", return_supabase_env_keys()['confluence_key'])) # auth=(username, api_token))
    # print(response.json())
    if response.status_code!=200:
        return []
    pages_data = response.json()['results']
    result_data = []
    for page in pages_data:
        page_id = page['id']
        web_ui = page['_links']['webui']
        page_title = page['title']

        web_ui_list = web_ui.split("/")
        web_ui_mod = web_ui_list[0] + "/" + web_ui_list[1] + "/" + web_ui_list[2]

        kb_url = f"https://someonsr045.atlassian.net/wiki{web_ui_mod}/pages/{page_id}"
        get_kb_content_url = f"https://someonsr045.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.view,metadata,space"
        kb_content_res = requests.get(get_kb_content_url, headers=headers, auth=("someonsr045@gmail.com",return_supabase_env_keys()['confluence_key'] ))
        if kb_content_res.status_code == 200:
            kb_content_data_html = kb_content_res.json()['body']['view']['value']
            kb_content_data_text = view_to_plain_text(kb_content_data_html)
        else:
            kb_content_data_text = ""
        
        return_obj = {"kb_url": kb_url, "title": page_title, "content": kb_content_data_text }
        result_data.append(return_obj)

    return result_data


    

    