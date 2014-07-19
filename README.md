#envayasms

RapidSMS Backend for EnvayaSMS Android App

Installation
============

Check out http://rapidsms.readthedocs.org/en/latest/main/installation.html for how to install RapidSMS.

Then, in your project directory:

```
$ git clone git://github.com/knightsamar/rapidsms-envaya.git
$ mv rapidsms-envaya envayasms
```

The *second* command is necessary because the original fork has a dash in it's name which breaks the importing as a package in Python.

In `settings.py` put:

Add `"envayasms"` to the list `INSTALLED_APPS`.

Add the following to `INSTALLED_BACKENDS`:

```
    'envayasms': {
        "ENGINE": "envayasms.backend.EnvayaSMSBackend",
    }
```

In `urls.py` put:

```
urlpatterns = patterns('',
    (r'^envaya_nexmo/', include('envaya_nexmo.urls')),
)
```

Run the following now to set up the database:

```
$ python manage.py syncdb
```

Finally, set up **EnvayaSMS on an Android phone**. See http://sms.envaya.org/install/ for how to install EnvayaSMS on a real phone, or http://sms.envaya.org/test/ for how to test on your local machine. EnvayaSMS has some great documentation on how to further set up EnvayaSMS.

Once you have the EnvayaSMS Android app running, set URL to point to the `http://YOUR.SERVER.IP.ADDRESS:PORT/envaya_nexmo/`

And now enjoy sending and receiving SMSes through EnvayaSMS!


Setting up logging
==================

This is an optional step. Setting up logging properly will help you troubleshoot any issues. 

To setup the logger, add the following to your `settings.py` in the **LOGGING** section.

```
        'envayasms' : {
            'handlers' : ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
```
This will direct all the logger messages to rapidsms-debug.log (or the relevant file configured in the handlers dictionary in your LOGGING settings.

How does it work?
=================

There are 3 players in the whole scene:

1. EnvayaSMS Django app for RapidSMS (this application!)
1. Your RapidSMS app (which also includes RapidSMS itself)
1. EnvayaSMS Android app (which runs on the phone)

####Outgoing message cycle

The outgoing message cycle works as follows:

1. Message is received by the `send` method of the EnvayaSMSBackend from `backend.py`
1. The message is then queued inside the database to be sent.
1. When an EnvayaSMS Android app running on a phone polls for messages using the 'outgoing' action, message are sent to the phone, to be actually delivered.
1. When a message is sent by the phone, the Android app updates (in the next polling) informs about it's status to the EnvayaSMS app.
1. The EnvayaSMS app updates the status of the message in the database, accordingly.


####Incoming message cycle

The incoming message cycle works as follows:

1. Message is received by the EnvayaSMS Android app.
1. The message is then forwarded to the EnvayaSMS Django app at the URL configured in the Android app, which is actually a view implementation of EnvayaSMSBackendView (and a form behind it) from `views.py`
1. The EnvayaSMS Django app validates it and sends it to the router for further processing.

