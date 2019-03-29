from ._ffprobe import *
from .auto_rep import AutoRepresentation


class Export(object):
    def __init__(self, filename):
        self.reps = None
        self.filename = filename

    def add_rep(self, *args):
        self.reps = list(args)
        return self

    def auto_rep(self):
        self.reps = AutoRepresentation(ffprobe(self.filename)).generate()
        return self

    def package(self):
        return self.reps
