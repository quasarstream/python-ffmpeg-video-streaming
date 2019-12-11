"""
ffmpeg_streaming.clouds
~~~~~~~~~~~~

Upload and download files -> clouds


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import abc
import sys
import tempfile

from os import listdir
from os.path import isfile, join

import boto3
import botocore
import requests
from azure.storage.blob import BlockBlobService
from google.cloud import storage

from ffmpeg_streaming.utiles import deprecated


class Clouds(abc.ABC):
    @abc.abstractmethod
    def upload_directory(self, directory, **options):
        pass

    @abc.abstractmethod
    def download(self, filename=None, **options):
        pass


class Cloud(Clouds):
    @deprecated
    def upload_directory(self, directory, **options):
        field_name = options.pop('field_name', None)

        if field_name is None:
            raise ValueError('You should specify a field_name')

        method = options.pop('method', 'post')
        url = options.pop('url', None)
        upload_files = []

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in files:
            full_path_file = directory + file
            upload_files.append((field_name, open(full_path_file, 'rb')))

        r = requests.request(method, url, files=upload_files, **options)

        if not r.ok:
            raise RuntimeError('Error uploading file!')

    @deprecated
    def download(self, filename=None, **options):
        progress = options.pop('progress', None)
        method = options.pop('method', 'get')
        url = options.pop('url', None)

        if url is None:
            raise ValueError('You should specify an url')

        if filename is None:
            file = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
        else:
            file = open(filename, 'wb')

        with file as f:
            response = requests.request(method, url, stream=True, **options)
            total_byte = response.headers.get('content-length')

            if total_byte is None or not callable(progress):
                f.write(response.content)
            else:
                downloaded = 0
                total_byte = int(total_byte)
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
                    percentage = round(100 * downloaded / total_byte)
                    progress(percentage, downloaded, total_byte)
                sys.stdout.write('\n')

            return f.name


class AWS(Clouds):
    def __init__(self, **options):
        self.s3 = boto3.client('s3', options)

    @deprecated
    def upload_directory(self, directory, **options):
        bucket_name = options.pop('bucket_name', None)
        if bucket_name is None:
            raise ValueError('You should pass a bucket name')

        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        for file in files:
            full_path_file = directory + file
            self.s3.upload_file(full_path_file, bucket_name, file)

    @deprecated
    def download(self, filename=None, **options):
        if filename is None:
            tmp = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
            filename = tmp.name

        bucket_name = options.pop('bucket_name', None)
        key = options.pop('key', None)
        if bucket_name is None or key is None:
            raise ValueError('You should pass a bucket name and a key')

        try:
            self.s3.Bucket(bucket_name).download_file(key, filename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise RuntimeError("The object does not exist.")
            else:
                raise RuntimeError("Could not connect to the server")

        return filename


class GoogleCloudStorage(Clouds):
    def __init__(self, bucket_name, **kwargs):
        storage_client = storage.Client(**kwargs)
        self.bucket_name = bucket_name
        self.bucket = storage_client.get_bucket(bucket_name)

    @deprecated
    def upload_directory(self, directory, **options):
        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in files:
            full_path_file = directory + file
            blob = self.bucket.blob(self.bucket_name + file, options)
            blob.upload_from_filename(full_path_file)

    @deprecated
    def download(self, filename=None, **options):
        if filename is None:
            tmp = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
            filename = tmp.name

        object_name = options.pop('object_name', None)
        if object_name is None:
            raise ValueError('You should pass an object name')

        blob = self.bucket.get_blob(object_name, options)
        blob.download_to_filename(filename)

        return filename


class MicrosoftAzure(Clouds):
    def __init__(self, **options):
        self.block_blob_service = BlockBlobService(**options)

    @deprecated
    def upload_directory(self, directory, **options):
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        container = options.pop('container', None)
        for file in files:
            full_path_file = directory + file
            self.block_blob_service.create_blob_from_path(container, file, full_path_file)

    @deprecated
    def download(self, filename=None, **options):
        if filename is None:
            tmp = tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False)
            filename = tmp.name

        container = options.pop('container', None)
        blob = options.pop('blob', None)

        self.block_blob_service.get_blob_to_path(container, blob, filename)

        return filename


def open_from_cloud(cloud):
    cloud = dict(enumerate(cloud))

    cloud_obj = cloud.get(0, None)
    if not isinstance(cloud_obj, Clouds):
        raise TypeError('Clouds must be instance of Clouds object')

    options = cloud.get(1, None)
    if options is None:
        options = dict

    filename = cloud.get(2, None)

    return cloud_obj.download(filename, **options)


def save_to_clouds(clouds, dirname):
    if clouds is not None:
        if type(clouds) != list or type(clouds) != tuple:
            raise TypeError('Clouds must be type of list or tuple')

        if type(clouds) == tuple:
            clouds = [clouds]

        for cloud in clouds:
            cloud = dict(enumerate(cloud))

            cloud_obj = cloud.get(0, None)
            if not isinstance(cloud_obj, Clouds):
                raise TypeError('Clouds must be instance of Clouds object')

            options = cloud.get(1, None)
            if options is None:
                options = dict

            cloud_obj.upload_directory(dirname, **options)


__all__ = [
    'Clouds',
    'Cloud',
    'AWS',
    'GoogleCloudStorage',
    'MicrosoftAzure'
]
