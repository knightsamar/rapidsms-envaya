from rapidsms.backends.http.views import GenericHttpBackendView
from .forms import EnvayaSMSBackendForm
from django.http import HttpResponse, HttpResponseBadRequest
from rapidsms.router import receive
import logging
import pprint
import json

logger = logging.getLogger('envayasms.views.EnvayaSMSBackendView')

class EnvayaSMSBackendView(GenericHttpBackendView):
    '''This handles the incoming message life cycle '''

    params = {
            #ref: http://sms.envaya.org/serverapi/

            #our name               : name passed by the envaya phone

            'identity_name'         : 'from',         #who sent the message?
            'text_name'             : 'message',      #what was the message?
#            'envaya_phone_number'   : 'phone_number', #which envaya phone forwarded us the msg?
#            'envaya_phone_log'      : 'log',          #any message log fwded by the envaya phone
#            'envaya_phone_connection': 'network',     #how is the envaya phone connected to our server?
#            'envaya_phone_version'  : 'version',      #version of the envaya software installed
#            'envaya_phone_now'      : 'now',          #the value of now (unix epoch) on the phone
#            'envaya_phone_power'    : 'power',        #The current power source of the Android phone
#            'envaya_phone_battery'  : 'battery',      #What is the source of the battery?
            }

    form_class =  EnvayaSMSBackendForm

    def form_valid(self, form):
        """
        If the form validated successfully, passes the message on to the
        router for processing.
        """
        data = form.get_incoming_data()
        logger.debug("data that we got is %s" % data)

        if data['action'] == 'incoming':
            receive(text = data['text'], connection = data['connection'])
            logger.info("Incoming message forwarded to router successfully!")

        elif data['action'] == 'outgoing':
            if len(data['events'][0]['messages']) > 1:
                logger.info("Outgoing message forwarded to EnvayaSMS Android app successfully")
            else:
                logger.info("No outgoing message to forward to EnvayaSMS Android app!")

        return HttpResponse(json.dumps({'events': data['events']}), content_type='application/json')

    def form_invalid(self, form):
        """
        If the form failed to validate, logs the errors and returns a bad
        response to the client.
        """

        logger.error("%s data:" % self.request.method)
        logger.error(pprint.pformat(form.data))
        errors = dict((k, v[0]) for k, v in form.errors.items())
        logger.error(unicode(errors))
        if form.non_field_errors():
            logger.error(form.non_field_errors())
        return HttpResponseBadRequest('form failed to validate')
