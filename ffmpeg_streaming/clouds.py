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


class Clouds(abc.ABC):
    @abc.abstractmethod
    def upload_directory(self, directory, **options):
        pass

    @abc.abstractmethod
    def download(self, filename=None, **options):
        pass


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
        if not isinstance(clouds, (list, tuple)):
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
]
