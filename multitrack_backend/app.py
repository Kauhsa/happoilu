#!/usr/bin/env python3
import os
from bottle import route, run, response, static_file, default_app


@route('/data')
def index():
    return get_data(os.environ["HAPPOILU_ROOT_DIR"], os.environ["HAPPOILU_ROOT_DIR"])


@route('/song/<filepath:path>')
def serve_song(filepath):
    response = static_file(filepath, root=os.environ["HAPPOILU_ROOT_DIR"])
    response.set_header("Cache-Control", "public, max-age=604800")
    return response


@route('/')
def serve_index():
    return static_file("index.html", root=os.environ["HAPPOILU_STATIC_DIR"])


@route('/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=os.environ["HAPPOILU_STATIC_DIR"])


def get_data(folder, rootdir):
    dirs = sorted([f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))])
    mp3_files = sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.mp3')])
    
    if (mp3_files):
        return {
            "type": "files",
            "name": os.path.basename(folder),
            "contents": [{ 'name': f, 'src': "song/" + os.path.relpath(os.path.join(folder, f), rootdir)} for f in mp3_files if "merged" not in f]
        }
    else:
        return {
            "type": "dir",
            "name": os.path.basename(folder),
            "contents": [get_data(os.path.join(folder, f), os.environ["HAPPOILU_ROOT_DIR"]) for f in dirs]
        }

if __name__ == '__main__':
    if "HAPPOILU_ROOT_DIR" not in os.environ:
        print("need root dir for songs")
    elif "HAPPOILU_STATIC_DIR" not in os.environ:
        print("need static dir for... static files")
    elif "HAPPOILU_FCGI" in os.environ:
        from flup.server.fcgi import WSGIServer
        WSGIServer(default_app()).run()
    else:
        run(host='localhost', port=8080, reloader=True)