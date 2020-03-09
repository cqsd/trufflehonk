import sys

from trufflepawg.queues.base import BaseQueue


class StdinQueue(BaseQueue):
    def pop(self):
        return sys.stdin.readline()
