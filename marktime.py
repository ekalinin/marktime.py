#!/usr/bin/env python

import json
import time


labels = {}


class TimerIt(object):

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self, start_time=None):
        self.start_time = int(start_time) if start_time else time.time()
        return self

    def stop(self, end_time=None):
        self.end_time = int(end_time) if end_time else time.time()
        return self

    def is_running(self):
        return self.start_time is not None and self.end_time is None

    def is_stopped(self):
        return self.start_time is not None and self.end_time is not None

    def duration(self):
        return self.end_time - self.start_time

    def dumps(self):
        return json.dumps({
            'start_time': self.start_time,
            'end_time': self.end_time
        })

    def loads(self, statestring):
        tmp = json.loads(statestring)
        self.start_time = int(tmp['start_time'])
        self.end_time = int(tmp['end_time']) if tmp['end_time'] else None
        return self


def start(label):
    """Begins the countdown"""
    t = time.time()
    labels[label] = TimerIt().start(t).dumps()


def stop(label, timeat=None, remove_from_labels=False, stop_once=True):
    """Stops the countdown"""
    t = time.time() if not timeat else timeat

    timer = TimerIt().loads(labels[label])

    if timer.is_running() or (timer.is_stopped() and not stop_once):
        timer.stop(t)

    if remove_from_labels:
        del labels[label]
    else:
        labels[label] = timer.dumps()

    return timer.duration()
