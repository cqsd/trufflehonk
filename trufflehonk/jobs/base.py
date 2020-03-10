import abc


class BaseJob(abc.ABC):
    @abc.abstractmethod
    def run(self) -> None:
        pass

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output
