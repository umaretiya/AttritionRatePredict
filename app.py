import os
from site import abs_paths
from flask import Flask, render_template
from flask import request, send_file, abort

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", **locals())


@app.route("/artifacts", defaults={"req_path": "project/attritionRate"})
@app.route("/artifacts/<path:req_path>")
def render_artifact_dir(req_path):
    os.makedirs("project/attritionRate", exist_ok=True)
    'project/attritionRate/artifacts'
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)

    if os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ""
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    files = {
        os.path.join(abs_path, file_name): file_name
        for file_name in os.listdir(abs_path)
        if "artifacts" in os.path.join(abs_path, file_name)
    }
    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path,
    }
    return render_template("files.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
