"""
Exports the site as plain static files for github pages.

Pages can't run flask, so this bakes the api responses into json files
and rewrites the fetch urls in main.js to point at them. The contact
form falls back to mailto (main.js checks for data-static on <body>).

Usage: python build_static.py   ->  everything lands in build/
"""

import json
import re
import shutil
import os

from app import app

OUT = os.path.join(os.path.dirname(__file__), "build")

ENDPOINTS = ["profile", "skills", "projects", "experience"]


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "api"))

    # snapshot the api using the test client, no running server needed
    client = app.test_client()
    for name in ENDPOINTS:
        resp = client.get("/api/" + name)
        assert resp.status_code == 200, "api/%s returned %d" % (name, resp.status_code)
        with open(os.path.join(OUT, "api", name + ".json"), "w") as f:
            json.dump(resp.get_json(), f, ensure_ascii=False)

    shutil.copytree("static", os.path.join(OUT, "static"),
                    ignore=shutil.ignore_patterns("__pycache__"))

    # index.html: relative asset paths + the static marker on <body>
    html = open("templates/index.html").read()
    html = html.replace('"/static/', '"static/')
    html = html.replace("<body>", '<body data-static="1">', 1)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(html)

    # main.js: '/api/profile' -> 'api/profile.json' etc
    js_path = os.path.join(OUT, "static", "js", "main.js")
    js = open(js_path).read()
    js = re.sub(r"'/api/(\w+)'", r"'api/\1.json'", js)
    with open(js_path, "w") as f:
        f.write(js)

    # keeps github from running the output through jekyll
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    print("static build ready in build/")


if __name__ == "__main__":
    main()
