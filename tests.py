#!/usr/bin/env python

import time
import random

import mock
import unittest

import marktime


class ApiTestCase(unittest.TestCase):

    @mock.patch('marktime.time.time')
    def test_start_stop(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', at=124).seconds, 1)

    def test_start_stop_at(self):
        marktime.start('test run', at=123)
        self.assertEquals(marktime.stop('test run', at=124).msecs, 1000)

    @mock.patch('marktime.time.time')
    def test_severals_markers(self, mock_time):
        start_time = 123
        markers_count = 10
        mock_time.return_value = start_time
        for i in range(1, markers_count):
            marktime.start('test run %d' % i)

        for i in range(1, markers_count):
            time_diff = marktime.stop('test run %d' % i,
                                      at=(start_time + i)).seconds
            self.assertEquals(time_diff, i)

    @mock.patch('marktime.time.time')
    def test_float_diffs(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')
        self.assertEquals(marktime.stop('test run', at=124.5).seconds, 1.5)

    @mock.patch('marktime.time.time')
    def test_stop_twice(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', at=124).seconds, 1)
        self.assertEquals(marktime.stop('test run', at=125).seconds, 1)
        self.assertEquals(marktime.stop('test run', at=183,
                                        stop_once=False).minutes, 1)

    @mock.patch('marktime.time.time')
    def test_real_times(self, mock_time):
        start_time = 1370451294.106749
        diff_time = random.random() * 100
        stop_time = start_time + diff_time

        mock_time.return_value = start_time
        marktime.start('test run')
        mock_time.return_value = stop_time
        self.assertEquals(round(marktime.stop('test run').seconds, 4),
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
                                  remove_from_labels=False).seconds

        self.assertEquals(marktime.labels['test run']['duration'], time_diff)

    def test_duration(self):
        start_time = 1370451294
        diff_time = round(random.random() * 100)
        stop_time = start_time + diff_time

        marktime.start('test run', at=start_time)
        marktime.stop('test run', at=stop_time)
        self.assertEquals(marktime.duration('test run').seconds, diff_time)

    def test_duration_None(self):
        marktime.start('test run')
        self.assertIsNone(marktime.duration('test run', stop_it=False))

    def test_duration_with_stop(self):
        start_time = 1370451294
        diff_time = round(random.random() * 100)
        stop_time = start_time + diff_time

        marktime.start('test run', at=start_time)
        self.assertEquals(
            marktime.duration('test run', stop_it=True,
                              stop_at=stop_time).seconds,
            diff_time)

    def test_stop_label_not_exists(self):
        self.assertIsNone(marktime.stop('not existance label'))

    def test_duration_label_not_exists(self):
        self.assertIsNone(marktime.duration('not existance label'))

    def test_stopwatch(self):
        diff_time = 0.5
        with marktime.stopwatch('test_stopwatch'):
            time.sleep(diff_time)

        self.assertEquals(
            round(marktime.duration('test_stopwatch').seconds, 2),
            round(diff_time, 2))


class InternalsTestCase(unittest.TestCase):

    def test_sleep(self):
        diff_time = 0.5
        marker = marktime.Marker()

        self.assertEquals(
            round(marker.start().sleep(diff_time)
                        .stop().duration().seconds, 2),
            round(diff_time, 2))

    def test_continue(self):
        marker = marktime.Marker().start().stop().coninue()
        self.assertTrue(marker.is_running())

    def test_is_running(self):
        marker = marktime.Marker()

        self.assertFalse(marker.is_running())
        self.assertTrue(marker.start().is_running())
        self.assertFalse(marker.stop().is_running())

    def test_is_stopped(self):
        marker = marktime.Marker()

        self.assertFalse(marker.is_stopped())
        self.assertFalse(marker.start().is_stopped())
        self.assertTrue(marker.stop().is_stopped())

    def test_with(self):
        diff_time = 0.5
        with marktime.Marker() as m:
            time.sleep(diff_time)
            self.assertEquals(
                round(m.duration().seconds, 2),
                round(diff_time, 2))
