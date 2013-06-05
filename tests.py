#!/usr/bin/env python

import json
import mock
import unittest

import marktime


class ApiTestCase(unittest.TestCase):

    @mock.patch('marktime.time.time')
    def test_start_stop(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

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
    def test_stop_twice(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', at=124), 1)
        self.assertEquals(marktime.stop('test run', at=125), 1)
        self.assertEquals(marktime.stop('test run', at=125,
                                        stop_once=False), 2)

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
