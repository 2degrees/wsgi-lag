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

from logging import getLogger

from pymongo.errors import AutoReconnect as PymongoAutoReconnect

from wsgilag.recorders import BaseEnvironLagRecorder


__all__ = ['MongodbEnvironLagRecorder']


_LOGGER = getLogger(__name__)


class MongodbEnvironLagRecorder(BaseEnvironLagRecorder):
    """MongoDB-based :mod:`wsgilag` recorder."""
    
    def __init__(self, mongodb_collection, *environ_keys):
        super(MongodbEnvironLagRecorder, self).__init__(*environ_keys)
        
        self.mongodb_collection = mongodb_collection
    
    def record_lag(self, lag_seconds, environ_subset):
        mongodb_document = {'lag_seconds': lag_seconds}
        mongodb_document.update(environ_subset)
        
        try:
            self.mongodb_collection.insert(mongodb_document)
        except PymongoAutoReconnect as exc:
            _LOGGER.critical(
                'Could not log request-response lag %r: "%s"',
                mongodb_document,
                exc,
                )
