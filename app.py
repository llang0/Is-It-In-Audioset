from flask import Flask, jsonify, request
from flask_cors import CORS
from lib.queries import get_by_ytid, get_labels_by_ytid, get_youtube_title, get_random
from lib.utils import format_single_video_to_dict

app = Flask(__name__)
CORS(app)
# test = {'message': 'hello world'}

@app.route('/')
def hello_world():
    # print(request.args.get('ytid'))
    video = get_by_ytid(request.args.get('ytid'))
    labels = get_labels_by_ytid(request.args.get('ytid'))
    title = get_youtube_title(request.args.get('ytid'))
    # print(title)
    # print(video)
    # print(labels)

    if video:
        test = format_single_video_to_dict(video, labels)
        test["title"] = title
    else:
        test = {"ytid": 0, "title": title}
    
    print(test)
    return jsonify(test)

@app.route('/random')
def random():
    ytid = get_random()
    print(ytid)
    return jsonify({"ytid": ytid})