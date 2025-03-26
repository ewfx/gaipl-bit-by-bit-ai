from flask import Flask, session, request, jsonify
import os
from RCA.prompts import system_prompts as rca_prompts
from CI_agent.prompts import system_prompts as ci_prompts
from RCA.main import rca_ai
from CI_agent.main import ci_ai
import sys
from troubleshoot.main import get_troubleshoot
from supabase_module import return_supabase_env_keys
from troubleshoot.prompt import system_prompt as troubleshoot_prompts
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = return_supabase_env_keys()["FLASK_SECRET_KEY"]  # Use a secure key in production
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure session storage exists
def init_session():
    # session_size = sys.getsizeof(dict(session))
    # if session_size >=4093:
    #     session.pop("rca", None)
    #     session.pop("ciagent", None)
    #     session.pop("troubleshoot",None)
    #     print("Sessions refreshed due to max-size reached")
    session_cookie = request.cookies.get("session") 
    if session_cookie:
        size_in_bytes = len(session_cookie.encode("utf-8"))  # Convert to bytes and get size
        print(f"Session cookie size: {size_in_bytes} bytes")
        if size_in_bytes > 7000:
            session.pop("rca", None)
            session.pop("ciagent", None)
            session.pop('troubleshoot',None)
            session.clear()
        else:
            print(size_in_bytes)
    if "rca" not in session:
        session["rca"] = {"messages":[]}
    if "ciagent" not in session:
        session["ciagent"] = {"messages":[]}
    if "troubleshoot" not in session:
        session["troubleshoot"] = {"messages":[]}

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to BitByBit.ai!!!"})

@app.route("/rca", methods=["POST"])
def rca():
    init_session()  # Ensure session keys exist
    try:
        data = request.get_json()  # Expecting a JSON payload
        user_prompt = data.get("user_prompt", "")
        result = rca_ai(session['rca'],user_prompt)
        session['rca']['messages'].append({"role":"user", "content":user_prompt})
        session['rca']['messages'].append({"role":"assistant", "content":result})
        session.modified = True  # Ensure session updates
        return jsonify({"message": "RCA data added", "data": session["rca"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ci-agent", methods=["POST"])
def ci_agent():
    init_session()  # Ensure session keys exist
    try:
        data = request.get_json()  # Expecting a JSON payload
        user_prompt = data.get("user_prompt", "")
        result = ci_ai(session['ciagent'],user_prompt)
        print(result)
        session['ciagent']['messages'].append({"role":"user", "content":user_prompt})
        session['ciagent']['messages'].append({"role":"assistant", "content":result})
        session.modified = True  # Ensure session updates
        return jsonify({"message": "CI-agent data added", "data": session["ciagent"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/troubleshoot", methods=["POST"])
def troubleshoot():
    init_session()  # Ensure session keys exist
    try:
        data = request.get_json()  # Expecting a JSON payload
        user_prompt = data.get("user_prompt", "")
        result = get_troubleshoot(session['troubleshoot'],user_prompt)
        print(result)
        session['troubleshoot']['messages'].append({"role":"user", "content":user_prompt})
        session['troubleshoot']['messages'].append({"role":"assistant", "content":result})
        session.modified = True  # Ensure session updates
        return jsonify({"message": "troubleshoot data added", "data": session["troubleshoot"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/flush", methods=["POST"])
def flush():
    session.pop("rca", None)
    session.pop("ciagent", None)
    session.pop('troubleshoot',None)
    session_cookie = request.cookies.get("session")
    # print(session_cookie) 
    if session_cookie:
        size_in_bytes = len(session_cookie.encode("utf-8"))  # Convert to bytes and get size
        session.clear()
        print(f"Session cookie size: {size_in_bytes} bytes")
    return jsonify({"message": "Session flushed successfully"})


if __name__ == "__main__":
    print("app starting")
    app.run(debug=True)
