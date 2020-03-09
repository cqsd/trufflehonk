import abc


class BaseQueue(abc.ABC):
    _type_name = None
    _name = None

    @abc.abstractmethod
    def pop(self):
        '''should return None when no items are available'''
        pass

    # should be required but isn't necessarily lmfao
    def push(self):
        raise NotImplementedError

    # not required, but some queues can potentially provide this
    def peek(self):
        raise NotImplementedError

    def __iter__(self):
        while True:
            el = self.pop()
            if el:
                yield el
            else:
                break
