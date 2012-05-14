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

from time import sleep

from nose.tools import eq_
from nose.tools import ok_

from wsgilag import LagRecordingMiddleware


__all__ = ['TestLagRecordingMiddleware']


class TestLagRecordingMiddleware(object):
    
    def test_response_returned(self):
        """The wrapped application's response is returned unaltered."""
        middleware = LagRecordingMiddleware(_MOCK_WSGI_APP, _MockLagRecorder())
        
        path_info = '/'
        environ = {'PATH_INFO': path_info}
        
        response = middleware(environ, None)
        eq_(path_info, response)
    
    def test_recording(self):
        """
        The lag recorder is called when the minimum required lag has been
        exceeded.
        
        """
        lag_recorder = _MockLagRecorder()
        middleware = LagRecordingMiddleware(_SLOW_WSGI_APP, lag_recorder)
        
        environ = {'PATH_INFO': '/'}
        middleware(environ, None)
        
        ok_(0 < lag_recorder.lag_seconds)
    
    def test_lag_under_minimum(self):
        """
        The lag recorder isn't called when the minimum required lag hasn't been
        exceeded.
        
        """
        lag_recorder = _MockLagRecorder()
        middleware = LagRecordingMiddleware(_MOCK_WSGI_APP, lag_recorder, 3600)
        
        environ = {'PATH_INFO': '/'}
        middleware(environ, None)
        
        ok_(lag_recorder.lag_seconds is None)


#{ Utilities


_MOCK_WSGI_APP = lambda environ, start_response: environ['PATH_INFO']


_SLOW_WSGI_APP = lambda environ, start_response: sleep(1)


class _MockLagRecorder(object):
    
    def __init__(self):
        super(_MockLagRecorder, self).__init__()
        
        self.lag_seconds = None
    
    def __call__(self, lag_seconds, request):
        self.lag_seconds = lag_seconds


#}
