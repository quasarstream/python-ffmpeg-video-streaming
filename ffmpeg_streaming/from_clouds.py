import tempfile
import requests


def from_url(url, method='get', **kwargs):
    progress = kwargs.pop('progress', None)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        response = requests.request(method, url, stream=True, **kwargs)
        total_byte = response.headers.get('content-length')

        if total_byte is None or not callable(progress):
            tmp.write(response.content)
        else:
            downloaded = 0
            total_byte = int(total_byte)
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                tmp.write(data)
                percentage = round(100 * downloaded/total_byte)
                progress(percentage, downloaded, total_byte)
            print('\n')
        return tmp.name
