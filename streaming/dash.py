from .export import Export


class DASH(Export):

    def __init__(self, filename):
        super().__init__(filename)

    def adaption(self, adaption):
        self.adaption = str(adaption)
        return self

