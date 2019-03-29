from .export import Export


class DASH(Export):

    def __init__(self, filename):
        self.adaption = None
        super().__init__(filename)

    def adaption(self, adaption):
        self.adaption = adaption
        return self

