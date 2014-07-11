from rapidsms.backends.base import BackendBase

class EnvayaSMSBackend(BackendBase):
    '''This handles the outgoing part ONLY'''

    '''def configure(**kwargs):
        print kwargs
        pass;
    '''

    def send(id_, text, identities, context = {}):
        print id
        print text
        print identities
        print context
        pass;
