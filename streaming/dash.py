from .export import Export


class DASH(Export):

    def __init__(self, filename, kwargs):
        self.adaption = kwargs.pop('adaption', None)
        super(DASH, self).__init__(filename)
