marktime
========

Simple python module for marking time.

Inspired by two functions from node.js:

  * `console.time <http://nodejs.org/docs/v0.10.10/api/all.html#all_console_time_label>`_
  * `console.timeEnd <http://nodejs.org/docs/v0.10.10/api/all.html#all_console_timeend_label>`_


Usage
-----

.. code-block:: bash

    $ pip install marktime

.. code-block:: python

    import marktime

    marktime.start('some task')
    marktime.start('some another task')

    marktime.stop('some task')
    8.757422924041748

    marktime.stop('some another task')
    14.805735111236572

    marktime.duration('some another task')
    14.805735111236572

    marktime.start('some task # 3')

    marktime.labels
    {
        'some another task': {
            'duration': 14.805735111236572,
            'start_time': 1370453758.064955,
            'end_time': 1370453772.87069
        },

        'some task # 3': {
            'start_time': 1370453892.025603,
            'end_time': None
        },

        'some task': {
            'duration': 8.757422924041748,
            'start_time': 1370453753.185846,
            'end_time': 1370453761.943269
        }
    }


API
---

Internal Class
==============

License
=======
