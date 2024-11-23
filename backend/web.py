import os
import http
import yaml

from typing import Dict
from flask import Flask, abort, render_template, send_file

INDEX_FILE = "files.yaml"
INDEX_FILE_MTIME = 0
FILES_DATA_LAST = None

app = Flask(__name__)

def load_files_data() -> Dict:
    global INDEX_FILE
    global INDEX_FILE_MTIME
    global FILES_DATA_LAST
    if INDEX_FILE_MTIME != os.path.getmtime(INDEX_FILE):
        INDEX_FILE_MTIME = os.path.getmtime(INDEX_FILE)
        with open(INDEX_FILE, "r") as f_h:
            FILES_DATA_LAST = yaml.safe_load(f_h.read())
    return FILES_DATA_LAST

@app.route("/")
def index():
    """Index page"""
    return render_template("index.html", files=load_files_data())

@app.route("/files/<string:section>/<string:file>")
def serve_files(section: str, file: str):
    """Serve files"""
    files_data = load_files_data()

    section_obj = None
    for entry in files_data["apps"]:
        if entry["name"] == section:
            section_obj = entry
            break
    if not section_obj:
        return abort(http.HTTPStatus.NOT_FOUND)

    ret_file = None
    for entry in section_obj["files"]:
        full_path = os.path.join(files_data["root"], entry)
        if os.path.basename(full_path) != file:
            continue
        if os.path.exists(full_path):
            ret_file = full_path
            break
    
    if not ret_file:
        return abort(http.HTTPStatus.NOT_FOUND)

    return send_file(ret_file, as_attachment=True)

if __name__ == "__main__":
    app.run("0.0.0.0")
