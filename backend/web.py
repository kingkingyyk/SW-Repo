import os
import http
import yaml

from flask import Flask, abort, render_template, send_file

with open("files.yaml", "r") as f_h:
    files_data = yaml.safe_load(f_h.read())

app = Flask(__name__)

@app.route("/")
def index():
    """Index page"""
    return render_template("index.html", files=files_data)

@app.route("/files/<string:section>/<string:file>")
def serve_files(section: str, file: str):
    """Serve files"""
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
