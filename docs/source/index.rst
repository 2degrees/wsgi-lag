**********************
wsgi-lag Documentation
**********************

:Latest release: |release|
:Download: `<http://pypi.python.org/pypi/wsgi-lag/>`_
:Development: `<https://github.com/2degrees/wsgi-lag>`_
:Author: `2degrees Limited <http://dev.2degreesnetwork.com/>`_

**wsgi-lag** makes it possible to audit the performance of WSGI applications by
recording the time spent processing requests on the server side.

More specifically, it offers an extensible WSGI middleware which stores the time
lag between the moment the application received the request and the moment it
returned a response.

Example
=======

To use this middleware, all you need is a callable which would record the
time lag and any other extra information from the WSGI environment you may want
to store.

.. code-block:: python
    
    from wsgilag import LagRecordingMiddleware
    
    # ...
    
    def record_lag_in_csv_file(lag_seconds, environ):
        with open('/tmp/lag-records.csv', 'a') as lag_file:
            path = environ['PATH_INFO']
            user_name = environ.get('REMOTE_USER')
            print >> lag_file, '%r, %d, %r' % (path, lag_seconds, user_name)
    
    application = LagRecordingMiddleware(application, record_lag_in_csv_file)


API documentation
=================

.. automodule:: wsgilag


Built-in lag recorders
----------------------

.. automodule:: wsgilag.recorders

MongoDB
~~~~~~~

.. automodule:: wsgilag.recorders.mongodb
