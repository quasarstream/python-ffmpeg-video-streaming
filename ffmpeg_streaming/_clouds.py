"""
ffmpeg_streaming.clouds
~~~~~~~~~~~~

Upload and download files -> clouds


:copyright: (c) 2020 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import abc
import logging
import tempfile
from os import listdir
from os.path import isfile, join


class Clouds(abc.ABC):
    """
    @TODO: add documentation
    """
    @abc.abstractmethod
    def upload_directory(self, directory: str, **options) -> None:
        pass

    @abc.abstractmethod
    def download(self, filename: str = None, **options) -> str:
        pass


class S3(Clouds):
    def __init__(self, **options):
        """
        @TODO: add documentation
        """
        try:
            import boto3
            from botocore.exceptions import ClientError
        except ImportError as e:
            raise ImportError("no specified import name! make sure you install the package via pip:\n\n"
                              "pip install boto3")

        self.s3 = boto3.client('s3', **options)
        self.err = ClientError

    def upload_directory(self, directory, **options):
        bucket_name = options.pop('bucket_name', None)
        folder = options.pop('folder', '')
        if bucket_name is None:
            raise ValueError('You should pass a bucket name')

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        try:
            for file in files:
                self.s3.upload_file(join(directory, file), bucket_name, join(folder, file))
        except self.err as e:
            logging.error(e)
            raise RuntimeError(e)

        logging.info("The " + directory + "directory was uploaded to Amazon S3 successfully")

    def download(self, filename=None, **options):
        bucket_name = options.pop('bucket_name', None)
        key = options.pop('key', None)

        if bucket_name is None or key is None:
            raise ValueError('You should pass a bucket and key name')

        if filename is None:
            filename = tempfile.NamedTemporaryFile(suffix='_' + key + '_py_ff_vi_st.tmp', delete=False)
        else:
            filename = open(filename, 'wb')

        try:
            with filename as f:
                self.s3.download_fileobj(bucket_name, key, f)
            logging.info("The " + filename.name + " file was downloaded")
        except self.err as e:
            logging.error(e)
            raise RuntimeError(e)

        return filename.name


class GCS(Clouds):
    def __init__(self, **options):
        """
        @TODO: add documentation
        """
        try:
            from google.cloud import storage
        except ImportError as e:
            raise ImportError("no specified import name! make sure you install the package via pip:\n\n"
                              "pip install google-cloud-storage")
        self.client = storage.Client(**options)

    def upload_directory(self, directory, **options):
        bucket_name = options.pop('bucket_name', None)
        if bucket_name is None:
            raise ValueError('You should pass a bucket name')

        bucket = self.client.get_bucket(bucket_name)

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in files:
            blob = bucket.blob(bucket_name + file, **options)
            blob.upload_from_filename(join(directory, file))

    def download(self, filename=None, **options):
        bucket_name = options.pop('bucket_name', None)
        if bucket_name is None:
            raise ValueError('You should pass a bucket name')

        bucket = self.client.get_bucket(bucket_name)

        if filename is None:
            with tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False) as tmp:
                filename = tmp.name

        object_name = options.pop('object_name', None)
        if object_name is None:
            raise ValueError('You should pass an object name')

        blob = bucket.get_blob(object_name, options)
        blob.download_to_filename(filename)

        return filename


class MAS(Clouds):
    def __init__(self, **options):
        """
        @TODO: add documentation
        """
        try:
            from azure.storage.blob import BlockBlobService
        except ImportError as e:
            raise ImportError("no specified import name! make sure you installed the package via pip:\n\n"
                              "pip install azure-storage-blob")
        self.block_blob_service = BlockBlobService(**options)

    def upload_directory(self, directory, **options):
        container = options.pop('container', None)
        if container is None:
            raise ValueError('You should pass a container name')

        files = [f for f in listdir(directory) if isfile(join(directory, f))]

        try:
            for file in files:
                self.block_blob_service.create_blob_from_path(container, file, join(directory, file))
        except:
            error = "An error occurred while uploading the directory"
            logging.error(error)
            raise RuntimeError(error)

    def download(self, filename=None, **options):
        container = options.pop('container', None)
        blob = options.pop('blob', None)

        if container is None or blob is None:
            raise ValueError('You should pass a container name and a blob name')

        if filename is None:
            with tempfile.NamedTemporaryFile(suffix='_py_ff_vi_st.tmp', delete=False) as tmp:
                filename = tmp.name

        try:
            self.block_blob_service.get_blob_to_path(container, blob, filename)
            logging.info("The " + filename + " file was downloaded")
        except:
            error = "An error occurred while downloading the file"
            logging.error(error)
            raise RuntimeError(error)

        return filename


class CloudManager:
    def __init__(self, filename: str = None):
        """
        @TODO: add documentation
        """
        self.filename = filename
        self.clouds = []

    def add(self, cloud: Clouds, **options):
        self.clouds.append((cloud, options))
        return self

    def transfer(self, method, path):
        for cloud in self.clouds:
            getattr(cloud[0], method)(path, **cloud[1])


__all__ = [
    'Clouds',
    'CloudManager',
    'S3',
    'GCS',
    'MAS'
]
