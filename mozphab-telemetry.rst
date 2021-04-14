################################
MozPhab Data Collection
################################

Mozphab is collecting user data to make data-driven decisions.

Data collection is automatically enabled for Mozilla employees, with the ability to
opt out. Non-employees can opt in or opt out at any time.

You are able to manually opt out of telemetry by changing the `telemetry.enabled` 
setting in the MozPhab's configuration file `<HOME_DIR>/.moz-phab-config`.

.. code-block:: ini

    [telemetry]
    enabled = True


For information about the data collected see:
https://github.com/mozilla-conduit/review/blob/master/TELEMETRY.md.
