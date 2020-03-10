import sys

from trufflehonk.queues.base import BaseQueue


class StdinQueue(BaseQueue):
    def pop(self):
        return sys.stdin.readline()
