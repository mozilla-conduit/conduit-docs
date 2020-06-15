# MozPhab data collection

Mozphab is collecting user data to make data-driven decisions.

Data collection is automatically enabled for Mozilla employees, with the ability to
 opt out. Non-employees can opt in or opt out at any time.

You are able to manually opt out of telemetry by changing the `telemetry.enabled` 
setting in the MozPhab's configuration file `<HOME_DIR>/.moz-phab-config`.

```
[telemetry]
enabled = True
```

In-detail [description of the collected data](https://github.com/mozilla-conduit/review/blob/master/TELEMETRY.md)
