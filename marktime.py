#!/usr/bin/env python

import time
from contextlib import contextmanager

# module version
version = '0.2.0'

# global dict where all statictics are stored
labels = {}


class Duration(object):

    def __init__(self, seconds):
        self.value = seconds

    @property
    def seconds(self):
        return self.value

    @property
    def msecs(self):
        return self.seconds * 1000

    @property
    def minutes(self):
        return self.seconds / 60


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

    def sleep(self, duration):
        time.sleep(duration)
        return self

    def is_running(self):
        return self.start_time is not None and self.end_time is None

    def is_stopped(self):
        return self.start_time is not None and self.end_time is not None

    def duration(self, at=None):
        res = None

        if self.is_running():
            end_time = at if at else time.time()
            res = end_time - self.start_time

        if self.is_stopped():
            res = self.end_time - self.start_time

        return Duration(res)

    def coninue(self):
        if self.is_stopped():
            self.end_time = None
        return self

    def dumps(self, add_duration=False):
        export_data = {
            'start_time': self.start_time,
            'end_time': self.end_time
        }

        if add_duration or self.is_stopped():
            export_data['duration'] = self.duration().seconds

        return export_data

    def loads(self, data):
        self.start_time = data['start_time']
        self.end_time = data['end_time'] if data['end_time'] else None
        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()


def start(label, at=None):
    """Begins the countdown"""
    t = at if at is not None else time.time()
    marker = Marker().start(t)
    labels[label] = marker.dumps()


def stop(label, at=None, remove_from_labels=False, stop_once=True):
    """Stops the countdown"""
    t = at if at is not None else time.time()

    if label not in labels:
        return None

    timer = Marker().loads(labels[label])

    if timer.is_running() or (timer.is_stopped() and not stop_once):
        timer.stop(t)

    if remove_from_labels:
        del labels[label]
    else:
        labels[label] = timer.dumps()

    return timer.duration()


def duration(label, stop_it=True, stop_at=None):
    """Returns duration in seconds for label"""

    if label not in labels:
        return None

    if "duration" in labels[label]:
        return Duration(labels[label]["duration"])

    if stop_it:
        return stop(label, at=stop_at)
    else:
        return None


@contextmanager
def stopwatch(label):
    marker = start(label)
    yield marker
    stop(label)
