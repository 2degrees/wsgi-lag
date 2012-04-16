##############################################################################
#
# Copyright (c) 2012, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
# All Rights Reserved.
#
# This file is part of wsgi-lag <https://github.com/2degrees/wsgi-lag>,
# which is subject to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

from time import time


__all__ = ['LagRecordingMiddleware']


class LagRecordingMiddleware(object):
    """
    WSGI middleware that records the lag between requests and their respective
    responses.
    
    The "lag" is defined as the time elapsed between the ingress of a request
    and the return of a response. Consequently, this lag excludes the time the
    server/gateway spends iterating over the response -- This difference will
    be negligible, except in the case of responses in the form of generators.
    
    """
    
    def __init__(self, app, lag_recorder, minimum_lag_seconds=0.0):
        """
        
        :param app: The WSGI application
        :param lag_recorder: Callable that records the lag between requests
            and their respective responses
        :param minimum_lag_seconds: Minimum number of seconds required to
            record the lag between a request and its response
        :type minimum_lag_seconds: :class:`float`
        
        """
        super(LagRecordingMiddleware, self).__init__()
        
        self.app = app
        self.lag_recorder = lag_recorder
        self.minimum_lag_seconds = minimum_lag_seconds
    
    def __call__(self, environ, start_response):
        start_time_seconds = time()
        
        response = self.app(environ, start_response)
        
        lag_seconds = time() - start_time_seconds
        if self.minimum_lag_seconds < lag_seconds:
            self.lag_recorder(lag_seconds, environ)
        
        return response
