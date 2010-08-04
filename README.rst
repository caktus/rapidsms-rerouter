-*- restructuredtext -*-

rapidsms-rerouter
=================

rerouter allows messages originating from one backend to be sent out on a
separate backend. This functionality is mostly intended to support `RapidSMS
<http://www.rapidsms.org/>`_ installations that use different backends for
Mobile Originated (MO) and Mobile Terminated (MT) `SMS
<http://en.wikipedia.org/wiki/SMS>`_ communication. For example, rerouter can
be used to send an SMS response through `Clickatell
<http://www.clickatell.com/>`_ from a `Twilio <http://www.twilio.com>`_
originated message.

Future Enhancements
-------------------

 * Allow more discrete routing logic through a customized function call
   defined in settings.py

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
