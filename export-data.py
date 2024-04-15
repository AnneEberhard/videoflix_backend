import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix.settings')

django.setup()

from django.http import HttpResponse
from content.admin import VideoResource



def download_json():
    dataset = VideoResource().export()
    json_data = dataset.json

    response = HttpResponse(json_data, content_type='application/json')

    response['Content-Disposition'] = 'attachment; filename="export.json"'
    print(json_data)

    return response


download_response = download_json()
print(download_response)

#return download_response
