#!/usr/bin/env python

import json
import time


labels = {}


class Marker(object):

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self, start_time=None):
        self.start_time = float(start_time) if start_time else time.time()
        return self

    def stop(self, end_time=None):
        self.end_time = float(end_time) if end_time else time.time()
        return self

    def is_running(self):
        return self.start_time is not None and self.end_time is None

    def is_stopped(self):
        return self.start_time is not None and self.end_time is not None

    def duration(self):
        return self.end_time - self.start_time

    def dumps(self, add_duration=False):
        export_data = {
            'start_time': self.start_time,
            'end_time': self.end_time
        }

        if add_duration or self.is_stopped():
            export_data['duration'] = self.duration()

        return json.dumps(export_data)

    def loads(self, statestring):
        tmp = json.loads(statestring)
        self.start_time = float(tmp['start_time'])
        self.end_time = float(tmp['end_time']) if tmp['end_time'] else None
        return self


def start(label):
    """Begins the countdown"""
    t = time.time()
    labels[label] = Marker().start(t).dumps()


def stop(label, at=None, remove_from_labels=False, stop_once=True):
    """Stops the countdown"""
    t = time.time() if not at else at

    timer = Marker().loads(labels[label])

    if timer.is_running() or (timer.is_stopped() and not stop_once):
        timer.stop(t)

    if remove_from_labels:
        del labels[label]
    else:
        labels[label] = timer.dumps()

    return timer.duration()
