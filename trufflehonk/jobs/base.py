import abc


class BaseJob(abc.ABC):
    @abc.abstractmethod
    def run(self) -> None:
        pass

    @property
    @abc.abstractmethod
    def name(self):
        '''return some sort of identifier for this particular run of the job,
        may be used by outputters (eg in key names or file paths)'''
        pass

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, output):
        self.__output = output

    # FIXME hacked in
    def format(self, fmt):
        if fmt == 'json':
            return self.output_json
        if fmt == 'human':
            return self.output_human
        raise KeyError(fmt)

    @property
    def output_json(self):
        return self.output

    @property
    def output_human(self):
        return self.output
