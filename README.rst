marktime
========

Simple python module for mark time.

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

* **marktime.start**(label, at=None)

  * ``label`` — marker label. String. Required.
  * ``at`` — time to start the countdown. If ``None`` then uses ``time.time()``.

* **marktime.stop**(label, remove_from_labels=False, stop_once=True)

  * ``label`` — marker label. String. Required.
  * ``at`` — time to stop the countdown. If ``None`` then uses ``time.time()``
  * ``remove_from_labels`` — if ``True`` then ``label`` removed from global
    dict ``marktime.labels``.
  * ``stop_once`` — if ``False`` and the countdown for the certain ``label``
    is allready stopped thet it stopped it again. And thereafter the duration
    for the certain ``label`` will be increased. 

* **marktime.duration**(label, stop=True)

  * ``label`` — marker label. String. Required.
  * ``stop`` — if ``True`` then the countdown for the certain ``label``
    will be stopped. If ``False`` and the countdown for the certain ``label``
    is not stopped then returns ``None``.

* **marktime.labels** — Global ``dict`` that stores all the labels for time markers.


License
-------

See `LICENSE <https://github.com/ekalinin/marktime.py/blob/master/LICENSE>`_
file.

