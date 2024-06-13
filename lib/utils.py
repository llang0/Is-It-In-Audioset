
from lib.queries import get_youtube_title

def format_single_video_to_dict(row, labels):
    """formats a row from the unbalanced_train_segments, 
    balanced_train_segments, or eval_segments tables into
    a dict"""

    # {
    #     'ytid': 'asdfas',
    #     'start_seconds': 0.0,
    #     'end_seconds': 10.0,
    #     'labels': ['asdf', 'sdfg', 'dfhdgf']
    # }

    cleaned_labels = [item[0] for item in labels]

    video = {
        'ytid': row[0][0],
        'start_seconds': float(row[0][1].replace(' ', '')),
        'end_seconds': float(row[0][2].replace(' ', '')),
        'labels': cleaned_labels,
        'title': ""
    }

    return(video)

