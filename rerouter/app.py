from django.conf import settings

from rapidsms.apps.base import AppBase
from rapidsms.models import Connection, Backend


class Rerouter(AppBase):
    def outgoing(self, msg):
        if hasattr(settings, 'REROUTE'):
            backend = msg.connection.backend
            if backend.name in settings.REROUTE:
                name = settings.REROUTE[backend.name]
                try:
                    to_backend = Backend.objects.get(name=name)
                except Backend.DoesNotExist:
                    self.error('%s backend does not exist' % name)
                    return False
                connection, created = Connection.objects.get_or_create(
                    backend=to_backend,
                    identity=msg.connection.identity,
                    contact=msg.connection.contact,
                )
                msg._connection = connection
                self.debug('Rerouted %s from %s to %s' % (msg, backend.name,
                                                          name))
