import abc


class BaseJob(abc.ABC):
    _type_name = None
    _name = None

    def __init__(self, timeout=600):
        self.timeout = timeout

    @abc.abstractmethod
    def run(self) -> None:
        pass

    @abc.abstractmethod
    def output(self) -> dict:
        '''Return a (preferrably json-serialazble) dict of output'''
        pass
