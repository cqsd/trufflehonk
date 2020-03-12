import abc


class BaseOutput(abc.ABC):
    def __init__(self, *args, format='json', **kwargs):
        self.format = format
        super().__init__()

    @abc.abstractmethod
    def output(self, job, *args, **kwargs):
        # TODO decide if this should ever be allowed to return
        pass
