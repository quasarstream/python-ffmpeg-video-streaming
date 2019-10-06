import tempfile

from os import listdir
from os.path import isfile, join

from google.cloud import storage


class Clouds(object):
    pass


class GoogleCloudStorage(Clouds):
    def __init__(self, dirname, bucket_name, **kwargs):
        self.storage_client = storage.Client(**kwargs)
        self.bucket_name = bucket_name
        self.dirname = dirname

    def __enter__(self):
        self.bucket = self.storage_client.get_bucket(self.bucket_name)
        return self.bucket

    def __exit__(self):
        files = [f for f in listdir(self.dirname) if isfile(join(self.dirname, f))]
        for file in files:
            local_file = self.dirname + file
            blob = self.bucket.blob(self.bucket_name + file)
            blob.upload_from_filename(local_file)

    @staticmethod
    def download(bucket_name, object_name, **kwargs):
        if bucket_name is None or object_name is None:
            raise ValueError('You should specify both "bucket_name" and "object_name"')

        client = storage.Client(**kwargs)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.get_blob(object_name)

        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='_py_ff_vi_st.tmp', delete=False)

        blob.download_to_filename(tmp.name)

        return tmp.name

