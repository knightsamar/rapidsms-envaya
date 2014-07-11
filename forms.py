from django import forms

from rapidsms.backends.http.forms import BaseHttpForm
import logging

logger = logging.getLogger(__name__)

class EnvayaSMSBackendForm(BaseHttpForm):
    '''handles validation and cleaning up of incoming message'''

    def __init__(self, *args, **kwargs):
        """
        Saves the identify (phone number) and text field names on self, calls
        super(), and then adds the required fields.
        """
        # defaults to "text" and "identity"
   
        self.text_name = kwargs.pop('text_name', 'text')
        self.identity_name = kwargs.pop('identity_name', 'identity')
         
        super(EnvayaSMSBackendForm, self).__init__(*args, **kwargs)
        
        #What fields are we expecting?
        self.fields[self.text_name] = forms.CharField()
        self.fields[self.identity_name] = forms.CharField() 
        self.fields['phone_number'] = forms.CharField() #which envaya phone forwarded us the msg?
#        self.fields['log'] = forms.CharField() #any message log fwded by the envaya phone
#        self.fields['network'] = forms.CharField() #type of network between server and envaya phone
        self.fields['action'] = forms.CharField() #what is the action?

    def get_incoming_data(self):
        """
        Returns the connection and text for this message, based on the field
        names passed to __init__().
        """
        print "Getting incoming data to put in the form"

        fields = self.cleaned_data.copy()
        
        action = self.cleaned_data['action']
        
        print "Fields that we got are ", fields
        return_data = {}
        #determine our further PoA based on the action varible passed by envaya phone
        import pdb
        pdb.set_trace()

        if action == 'incoming':
            logger.info("We have an incoming message!")

            return_data['text']        = self.cleaned_data[self.text_name]
            return_data['connection']  = self.lookup_connections([self.identity_name])[0]
            return_data['from_phone']  = self.cleaned_data['phone_number']
            return return_data

        elif action == 'send_status':
            pass
        elif action == 'device_status':
            pass
        elif action == 'forward_sent':
            pass
        elif action == 'amqp_started':
            pass

        return {}

