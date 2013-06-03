#!/usr/bin/env python

import mock
import unittest

import timerit


class ApiTestCase(unittest.TestCase):

    @mock.patch('timerit.time.time')
    def test_start_stop(self, mock_time):
        mock_time.return_value = 123
        timerit.start('test run')

        self.assertEquals(timerit.stop('test run', timeat=124), 1)

    @mock.patch('timerit.time.time')
    def test_stop_twice(self, mock_time):
        mock_time.return_value = 123
        timerit.start('test run')

        self.assertEquals(timerit.stop('test run', timeat=124), 1)
        self.assertEquals(timerit.stop('test run', timeat=125), 1)
        self.assertEquals(timerit.stop('test run', timeat=125,
                                       stop_once=False), 2)

    def test_remove_from_labels(self):
        timerit.start('test run')
        timerit.stop('test run')
        self.assertIn('test run', timerit.labels)

        timerit.stop('test run', remove_from_labels=True)
        self.assertNotIn('test run', timerit.labels)
