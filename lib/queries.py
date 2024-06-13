import sqlite3
import json
import argparse
import urllib
import requests

def get_by_ytid(ytid):
    con = sqlite3.connect("audioset.db")
    cur = con.cursor()
    res = cur.execute('''SELECT * 
                      FROM balanced_train_segments
                      WHERE YTID = ?
                      UNION
                      SELECT * 
                      FROM unbalanced_train_segments
                      WHERE YTID = ?
                      UNION
                      SELECT * 
                      FROM eval_segments
                      WHERE YTID = ?
                      ''', (ytid, ytid, ytid))
    
    return res.fetchall()

def get_by_pid(pid):
    con = sqlite3.connect("audioset.db")
    cur = con.cursor()
    res = cur.execute('''
                      SELECT *
                      FROM positive_labels
                      JOIN unbalanced_train_segments
                      ON positive_labels.YTID = unbalanced_train_segments.YTID
                      WHERE positive_label = ?
                      ''', (pid,))
    
    return res.fetchall()

def get_labels_by_ytid(ytid):
    con = sqlite3.connect("audioset.db")
    cur = con.cursor()
    res = cur.execute('''SELECT positive_label FROM positive_labels WHERE YTID = ?''', (ytid,))
    return res.fetchall()


def empty_ontologies():
    """Returns a list of ontologies with no positive ids"""
    with open("ontology.json") as json_file:
        data = json.load(json_file)

    for ont in data: 
        if not get_by_pid(ont["id"]):
            print(ont["id"])

def main():
    if pid_flag:
        res = get_by_pid(label)
        print(f"Videos with label {label}:\n")
        for row in res:
            print(row)
    elif empty_ont:
        empty_ontologies()
    else:
        print(f'Video:\n{get_by_ytid(label)}\n')
        print(f'Labels:\n{get_labels_by_ytid(label)}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="Query audioset by youtube id or ontology.", 
    usage="python queries.py <YTID or ontololgy> \n use flag -pid to search ontologies"
    )

    parser.add_argument('label')
    parser.add_argument('-pid', '--positive-id', action='store_true')
    parser.add_argument('-e', '--empty-ontologies', action='store_true')
    args = parser.parse_args()

    label = args.label
    pid_flag = args.positive_id
    empty_ont = args.empty_ontologies
    
    main()

def get_youtube_title(ytid):
    params = {"format": "json", "url": f"https://www.youtube.com/watch?v={ytid}"}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string 
    response = requests.get(url)
    data = response.json()
    print(data['title'])
    return data['title']

def get_random():
    con = sqlite3.connect("audioset.db")
    cur = con.cursor()
    res = cur.execute('''
                      SELECT ytid
                      FROM unbalanced_train_segments
                      ORDER BY RANDOM()
                      LIMIT 1;
                      ''', ())
    
    # print(res.fetchone()[0])
    # return res.fetchone()[1]
    return res.fetchone()[0]
