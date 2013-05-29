#!/usr/bin/env python

import time


labels = {}


class Horologe(object):

    def start(self, start_time=None):
        self.start_time = start_time if start_time else time.time()

    def end(self, end_time=None):
        self.end_time = end_time if end_time else time.time()

    def duration(self):
        return self.end_time - self.start_time


def start(label):
    """docstring for time"""
    labels[label] = Horologe()


def end(label):
    """docstring for time_end"""
    te = time.time()
    h = labels[label]
    h.end(te)
    return h.duration()
