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

from nose.tools import eq_

from wsgilag.recorders import BaseEnvironLagRecorder


__all__ = ['TestBaseEnvironLagRecorder']


class TestBaseEnvironLagRecorder(object):
    
    def test_missing_keys(self):
        recorder = _MockEnvironLagRecorder('REMOTE_USER', 'PATH')

        environ = {'PATH': '/'}
        environ_subset = environ.copy()   # Before any potential modification
        recorder(0, environ)
        
        eq_(environ_subset, recorder.environ_subset)
    
    def test_exact_keys(self):
        recorder = _MockEnvironLagRecorder('REMOTE_USER', 'PATH')

        environ = {'PATH': '/', 'REMOTE_USER': 'jsmith'}
        environ_subset = environ.copy()   # Before any potential modification
        recorder(0, environ)
        
        eq_(environ_subset, recorder.environ_subset)
    
    def test_unnecessary_keys(self):
        recorder = _MockEnvironLagRecorder('PATH')

        environ = {'PATH': '/', 'REMOTE_USER': 'jsmith'}
        recorder(0, environ)
        
        eq_({'PATH': '/'}, recorder.environ_subset)
    
    def test_lag(self):
        recorder = _MockEnvironLagRecorder('PATH')

        lag_seconds = 13
        recorder(lag_seconds, {})
        
        eq_(lag_seconds, recorder.lag_seconds)


class _MockEnvironLagRecorder(BaseEnvironLagRecorder):
    
    def __init__(self, *environ_keys):
        super(_MockEnvironLagRecorder, self).__init__(*environ_keys)
        
        self.environ_subset = None
    
    def record_lag(self, lag_seconds, environ_subset):
        self.lag_seconds = lag_seconds
        self.environ_subset = environ_subset
