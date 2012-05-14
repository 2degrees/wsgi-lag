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
"""Tests for the MongoDB-based lag recorder."""

from nose.tools import assert_dict_contains_subset
from nose.tools import assert_in
from nose.tools import eq_
from pymongo import Connection as PymongoConnection
from pymongo.errors import AutoReconnect as PymongoAutoReconnect

from wsgilag.recorders.mongodb import MongodbEnvironLagRecorder

from tests.utils import LoggingHandlerFixture


__all__ = ['TestMongodbEnvironLagRecorder']


class TestMongodbEnvironLagRecorder(object):
    
    #{ Fixture handling
    
    @classmethod
    def setup_class(cls):
        cls.connection = PymongoConnection()
        cls.database = cls.connection['wsgilag-tests']
    
    @classmethod
    def teardown_class(cls):
        cls.connection.drop_database(cls.database)
        cls.connection.disconnect()
    
    def setup(self):
        self.collection = self.database['fixture']
        
        self.logging_handler_fixture = LoggingHandlerFixture('wsgilag')
    
    def teardown(self):
        self.database.drop_collection(self.collection)
        
        self.logging_handler_fixture.undo()
    
    #}
    
    def test_autoreconnect(self):
        """
        Critical log entries are issued when the connection to MongoDB is lost.
        
        """
        recorder = MongodbEnvironLagRecorder(
            _UnusablePymongoCollection(), 'PATH', 'REMOTE_USER')
        
        lag_seconds = 2.5
        environ = {'PATH': '/', 'REMOTE_USER': 'jsmith'}
        recorder(lag_seconds, environ)
        
        log_messages = self.logging_handler_fixture.handler.messages
        critical_log_messages = log_messages['critical']
        eq_(1, len(critical_log_messages))
        assert_in('foobar', critical_log_messages[0])
        assert_in(str(lag_seconds), critical_log_messages[0])
        assert_in('PATH', critical_log_messages[0])
        assert_in('REMOTE_USER', critical_log_messages[0])
        assert_in('jsmith', critical_log_messages[0])
    
    def test_recording(self):
        recorder = MongodbEnvironLagRecorder(
            self.collection, 'PATH', 'REMOTE_USER')
        
        environ = {'PATH': '/', 'REMOTE_USER': 'jsmith'}
        recorder(2.5, environ)
        
        eq_(1, self.collection.count())
        
        mongo_document = self.collection.find_one()
        assert_dict_contains_subset(environ, mongo_document)


class _UnusablePymongoCollection(object):
    
    def insert(self, *args, **kwargs):
        raise PymongoAutoReconnect('foobar')

