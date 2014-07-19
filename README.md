#envayasms

RapidSMS Backend for EnvayaSMS Android App

Installation
============

Check out http://rapidsms.readthedocs.org/en/latest/main/installation.html for how to install RapidSMS.

Then, in your project directory:

```
$ git clone git://github.com/dimagi/rapidsms-envaya.git
```

In settings.py:

Add `"envayasms"` to the list `INSTALLED_APPS`.

Add the following to `INSTALLED_BACKENDS`:

```
    'envayasms': {
        "ENGINE": "envayasms.backend.EnvayaSMSBackend",
    }
```

Run the following again to set up the database:

```
$ python manage.py syncdb
```

Finally, set up EnvayaSMS on an Android phone. See http://sms.envaya.org/install/ for how to install EnvayaSMS on a real phone, or http://sms.envaya.org/test/ for how to test on your local machine. EnvayaSMS has some great documentation on how to further set up EnvayaSMS.

Once you have EnvayaSMS running, set URL to point to the machine running RapidSMS, matching exactly the URL set above. Do the same with the password, if it is set in RapidSMS. (The password feature won't work unless you set the URL correctly.)

And now enjoy sending SMSes through EnvayaSMS!
