import tempfile


class TempFileMixin:
    @property
    def tempfile(self):
        if not hasattr(self, '_tempfile'):
            self._tempfile = tempfile.mktemp()
        return self._tempfile

    @property
    def tempdir(self):
        if not hasattr(self, '_tempdir'):
            self._tempdir = tempfile.mkdtemp()
        return self._tempdir
