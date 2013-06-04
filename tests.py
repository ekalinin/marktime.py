#!/usr/bin/env python

import mock
import unittest

import marktime


class ApiTestCase(unittest.TestCase):

    @mock.patch('marktime.time.time')
    def test_start_stop(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', timeat=124), 1)

    @mock.patch('marktime.time.time')
    def test_stop_twice(self, mock_time):
        mock_time.return_value = 123
        marktime.start('test run')

        self.assertEquals(marktime.stop('test run', timeat=124), 1)
        self.assertEquals(marktime.stop('test run', timeat=125), 1)
        self.assertEquals(marktime.stop('test run', timeat=125,
                                        stop_once=False), 2)

    def test_remove_from_labels(self):
        marktime.start('test run')
        marktime.stop('test run')
        self.assertIn('test run', marktime.labels)

        marktime.stop('test run', remove_from_labels=True)
        self.assertNotIn('test run', marktime.labels)
