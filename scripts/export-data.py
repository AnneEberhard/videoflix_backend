import sys
import os
import json

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))

sys.path.append(parent_directory)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix.settings')

django.setup()

from datetime import datetime
from django.http import HttpResponse
from content.admin import VideoResource
from user.admin import UserResource


def export_data(resource, model_name):
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"export_{model_name}_{current_date}.json"

    folder_path = os.path.join("data")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)
    print(file_path)

    dataset = resource().export()
    json_data = dataset.json

    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    parsed = json.loads(json_data)
    with open(file_path, "w") as text_file:
        text_file.write(json.dumps(parsed, indent=4))

    return response


video_export_response = export_data(VideoResource, "video")
user_export_response = export_data(UserResource, "user")
