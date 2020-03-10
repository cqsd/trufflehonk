import abc


class BaseOutput(abc.ABC):
    _type_name = None
    _name = None

    @abc.abstractmethod
    def output(self, job, *args, **kwargs):
        # TODO decide if this should ever be allowed to return
        pass
