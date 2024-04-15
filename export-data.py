import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix.settings')

django.setup()

from django.http import HttpResponse
from content.admin import VideoResource



def download_json():
    dataset = VideoResource().export()
    json_data = dataset.json

    response = HttpResponse(json_data, content_type='application/json')

    response['Content-Disposition'] = 'attachment; filename="export.json"'
    # print(json_data)
    parsed = json.loads(json_data)
    # print(json.dumps(parsed, indent=4))
    text_file = open("Video.json", "w")
    text_file.write(json.dumps(parsed, indent=4))
    text_file.close()

    return response


download_response = download_json()
print(download_response)

