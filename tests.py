#!/usr/bin/env python

import json
import random

import mock
import unittest

import marktime


class ApiTestCase(unittest.TestCase):

    @mock.patch('marktime.time.time')
    def test_start_stop(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', at=124), 1)

    def test_start_stop_at(self):
        marktime.start('test run', at=123)
        self.assertEquals(marktime.stop('test run', at=124), 1)

    @mock.patch('marktime.time.time')
    def test_severals_markers(self, mock_time):
        start_time = 123
        markers_count = 10
        mock_time.return_value = start_time
        for i in xrange(1, markers_count):
            marktime.start('test run %d' % i)

        for i in xrange(1, markers_count):
            time_diff = marktime.stop('test run %d' % i,
                                      at=(start_time + i))
            self.assertEquals(time_diff, i)

    @mock.patch('marktime.time.time')
    def test_float_diffs(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')
        self.assertEquals(marktime.stop('test run', at=124.5), 1.5)

    @mock.patch('marktime.time.time')
    def test_stop_twice(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', at=124), 1)
        self.assertEquals(marktime.stop('test run', at=125), 1)
        self.assertEquals(marktime.stop('test run', at=125,
                                        stop_once=False), 2)

    @mock.patch('marktime.time.time')
    def test_real_times(self, mock_time):
        start_time = 1370451294.106749
        diff_time = random.random() * 100
        stop_time = start_time + diff_time
        print start_time
        print stop_time

        mock_time.return_value = start_time
        marktime.start('test run')
        mock_time.return_value = stop_time
        self.assertEquals(round(marktime.stop('test run'), 4),
                          round(diff_time, 4))

    def test_remove_from_labels(self):
        marktime.start('test run')
        marktime.stop('test run')
        self.assertIn('test run', marktime.labels)

        marktime.stop('test run', remove_from_labels=True)
        self.assertNotIn('test run', marktime.labels)

    @mock.patch('marktime.time.time')
    def test_duration_data_in_dumps(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')
        time_diff = marktime.stop('test run', at=124,
                                  remove_from_labels=False)

        marker_data = json.loads(marktime.labels['test run'])

        self.assertEquals(float(marker_data['duration']), time_diff)

    def test_duration(self):
        start_time = 1370451294
        diff_time = round(random.random() * 100)
        stop_time = start_time + diff_time

        marktime.start('test run', at=start_time)
        marktime.stop('test run', at=stop_time)
        self.assertEquals(marktime.duration('test run'), diff_time)
