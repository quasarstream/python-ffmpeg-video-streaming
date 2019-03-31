from .export import Export


class HLS(Export):

    def __init__(self, filename, **kwargs):
        self.hls_time = kwargs.pop('hls_time', None)
        self.hls_allow_cache = kwargs.pop('hls_allow_cache', None)
        self.hls_key_info_file = kwargs.pop('hls_key_info_file', None)
        super(HLS, self).__init__(filename)
