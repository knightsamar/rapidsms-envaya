from rapidsms.backends.base import BackendBase
import logging
import requests
from .models import EnqueuedMessage

logger = logging.getLogger('envayasms.backend.EnvayaSMSBackend')

class EnvayaSMSBackend(BackendBase):
    '''This handles the outgoing part ONLY'''

    def configure(self, **kwargs):
        '''Handles specific configuration for this Backend'''
        super(EnvayaSMSBackend, self).configure(**kwargs)

    def send(self, id_, text, identities, context = {}):
        '''
        This handles the actual part of outgoing message cycle.
        What we actually do here, is enqueue the message to be sent when the Android app
        enquires about it.
        '''
        logger.debug("id is %s" % id_)
        logger.debug("text is %s" % text)
        logger.debug("identities is %s" % type(identities))
        logger.debug("context is %s " % context)

        for i in identities:
            m = EnqueuedMessage(
                msg_id   = id_ ,
                recipient= i,
                message  = text,
                )
            m.save()

    @property
    def model(self):
        """
        The model attribute is the RapidSMS model instance with this
        backend name. A new backend will automatically be created if
        one doesn't exist upon accessing this attribute.
        """
        from rapidsms.models import Backend
        backend, _ = Backend.objects.get_or_create(name=self.name)
        return backend
