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

from abc import ABCMeta
from abc import abstractmethod


__all__ = ['BaseEnvironLagRecorder']


class BaseEnvironLagRecorder(object):
    """
    Optional base class for lag recorders which need to receive a subset of the
    items in the WSGI environment.
    
    """
    
    __metaclass__ = ABCMeta
    
    def __init__(self, *environ_keys):
        """
        
        ``environ_keys`` are the keys for the WSGI environment subset to be
        passed on to :meth:`record_lag`.
        
        """
        self.environ_keys = environ_keys
    
    def __call__(self, lag_seconds, environ):
        environ_subset = {}
        for environ_key in self.environ_keys:
            if environ_key in environ:
                environ_subset[environ_key] = environ[environ_key]
        
        self.record_lag(lag_seconds, environ_subset)
    
    @abstractmethod
    def record_lag(self, lag_seconds, environ_subset):
        """Record the ``lag_seconds`` and the ``environ_subset`` for a lag."""
        pass
