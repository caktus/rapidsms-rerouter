import unittest

from django.conf import settings

from nose.tools import assert_equals, assert_true

from rapidsms.router import Router
from rapidsms.models import Connection, Backend
from rapidsms.messages.outgoing import OutgoingMessage
from rapidsms.tests.harness import MockBackend

from rerouter.app import Rerouter


class MockRouter(Router):
    def start(self):
        self.running = True
        self.accepting = True
        self._start_all_backends()
        self._start_all_apps()

    def stop(self):
        self.running = False
        self.accepting = False
        self._stop_all_backends()


class MockOutgoingMessage(OutgoingMessage):
    def send_now(self):
        return True


backend_model = Backend.objects.create(name='backend1')
backend_model2 = Backend.objects.create(name='backend2')
router = MockRouter()
backend = MockBackend(name=backend_model.name, router=router)
router.backends['backend1'] = backend
router.apps.append(Rerouter(router))
router.start()


def test_backend_reroute():
    """ Make sure the outgoing phase correctly reroutes a message """
    settings.REROUTE = {'backend1': 'backend2'}
    conn = Connection.objects.create(backend=backend_model,
                                     identity='1112229999')
    message = MockOutgoingMessage(conn, 'test')
    assert_equals(message.connection.backend.name, 'backend1')
    assert_true(router.outgoing(message), True)
    assert_equals(message.connection.backend.name, 'backend2')
