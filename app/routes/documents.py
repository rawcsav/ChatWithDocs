from flask import session, Blueprint, render_template, request, jsonify, current_app, \
    has_request_context
import pandas as pd
import shutil
from app.util import add_embeddings_to_df, gather_text_sections
from app.config import MAIN_TEMP_DIR, ALLOWED_EXTENSIONS
import os
import openai
from werkzeug.utils import secure_filename

bp = Blueprint('documents', __name__)


@bp.route('/')
def index():
    if 'UPLOAD_DIR' not in session:
        session_id = str(id(session))  # Use the session id to create a unique directory for each session
        session_dir = os.path.join(MAIN_TEMP_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        session['UPLOAD_DIR'] = session_dir

    os.makedirs(session['UPLOAD_DIR'], exist_ok=True)

    if 'EMBED_DATA' not in session:
        EMBED_DATA_PATH = os.path.join(session['UPLOAD_DIR'], 'embed_data.json')
        session['EMBED_DATA'] = EMBED_DATA_PATH
        if not os.path.exists(EMBED_DATA_PATH):
            with open(EMBED_DATA_PATH, 'w') as f:
                pass

    uploaded_files = session.get('uploaded_files', [])
    existing_files = [f for f in uploaded_files if os.path.exists(os.path.join(session['UPLOAD_DIR'], f))]

    session['uploaded_files'] = existing_files

    return render_template('index.html', uploaded_files=existing_files)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['POST'])
def upload_file():
    api_key = session.get('api_key')
    openai.api_key = api_key
    response = {
        "status": "success",
        "messages": []
    }

    if 'UPLOAD_DIR' not in session or 'EMBED_DATA' not in session:
        session_id = str(id(session))  # Use the session id to create a unique directory for each session
        session_dir = os.path.join(MAIN_TEMP_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        session['UPLOAD_DIR'] = session_dir
        EMBED_DATA_PATH = os.path.join(session['UPLOAD_DIR'], 'embed_data.json')
        session['EMBED_DATA'] = EMBED_DATA_PATH
        # Create the file if it doesn't exist
        if not os.path.exists(EMBED_DATA_PATH):
            with open(EMBED_DATA_PATH, 'w') as f:
                pass

    if 'file' not in request.files:
        response["status"] = "error"
        response["messages"].append("No file part in the request.")
        return jsonify(response), 400

    uploaded_files = request.files.getlist('file')
    if not uploaded_files:
        response["status"] = "error"
        response["messages"].append("No file selected for uploading.")
        return jsonify(response), 400

    uploaded_file_names = session.get('uploaded_files', [])
    UPLOAD_DIR = session.get('UPLOAD_DIR')

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    new_files = []
    for file in uploaded_files:
        secure_file_name = secure_filename(file.filename)
        if secure_file_name in uploaded_file_names:
            response["messages"].append(f"File {secure_file_name} already uploaded.")
            continue
        if file and allowed_file(secure_file_name):
            filename = os.path.join(UPLOAD_DIR, secure_file_name)
            file.save(filename)
            new_files.append(secure_file_name)
            response["messages"].append(f"File {secure_file_name} processed successfully.")

    df_new = gather_text_sections(UPLOAD_DIR)
    df_new = add_embeddings_to_df(df_new, api_key)

    EMBED_DATA_PATH = session.get('EMBED_DATA')
    if os.path.exists(EMBED_DATA_PATH) and os.path.getsize(
            EMBED_DATA_PATH) > 0:
        df_existing = pd.read_json(EMBED_DATA_PATH, orient='split')
    else:
        df_existing = pd.DataFrame()

    if df_existing.empty:
        df_combined = df_new
    else:
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)

    df_combined.to_json(EMBED_DATA_PATH, orient='split')

    session['uploaded_files'] = list(set(uploaded_file_names + new_files))

    return jsonify(response)


@current_app.teardown_appcontext
def cleanup(exception=None):
    if has_request_context():
        if not session:
            UPLOAD_DIR = session.get('UPLOAD_DIR')
            if UPLOAD_DIR and os.path.exists(UPLOAD_DIR):
                try:
                    shutil.rmtree(UPLOAD_DIR)
                except Exception as e:
                    print(f"Error cleaning up temporary directory {UPLOAD_DIR}: {e}")
            EMBED_DATA_PATH = session.get('EMBED_DATA')
            if EMBED_DATA_PATH and os.path.exists(EMBED_DATA_PATH):
                try:
                    os.remove(EMBED_DATA_PATH)
                except Exception as e:
                    print(f"Error cleaning up temporary file {EMBED_DATA_PATH}: {e}")
