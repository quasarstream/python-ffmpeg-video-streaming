import sys
import tempfile
import requests
import boto3


def from_url(url, method='get', **kwargs):
    progress = kwargs.pop('progress', None)
    with tempfile.NamedTemporaryFile(delete=False, suffix='_py_ff_vi_st.tmp') as tmp:
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
            sys.stdout.write('\n')

        return tmp.name


def from_s3(**kwargs):
    bucket_name = kwargs.pop('bucket_name', None)
    object_name = kwargs.pop('object_name', None)

    if bucket_name is None or object_name is None:
        raise ValueError('You should specify both "bucket_name" and "object_name"')

    s3 = boto3.client('s3', kwargs)
    with tempfile.NamedTemporaryFile(delete=False, suffix='_py_ff_vi_st.tmp') as tmp:
        s3.download_fileobj(bucket_name, object_name, tmp)

    return tmp.name



