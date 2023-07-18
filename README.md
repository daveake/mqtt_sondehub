MQTT Sondehub Gateway
====================

Provides a means of passing UKHAS balloon telemetry from an MQTT broker to Sondehub so the balloon appears on the [Sondehub map](https://amateur.sondehub.org/).

This is intended for use with devices such as my GPS/LTE backup tracker than sends its GPS position to an MQTT broker via a mobile phone (LTE) connection.

If you have your own tracker receiving system that outputs telemetry to an MQTT broker then you can also use it.

Sending to an MQTT broker is simple and can be done on lowly microcontrollers, so it can make sense to use MQTT as an intermediary rather than sending directly to Sondehub.  However for some use cases - e.g. your tracker is a Raspberry Pi with LTE modem - then you may prefer to write to Sondehub directly.

Dependencies
============

This gateway is written in Python and has been tested on a Raspberry Pi.  It should work on any computer that runs Python however.

It uses the [paho-mqtt](https://pypi.org/project/paho-mqtt/) and [Sondehub](https://pypi.org/project/sondehub/) libraries:

	pip install paho-mqtt
	pip install sondehub



MQTT
============

You need an MQTT broker that the telemetry is being uploaded to.

That broker needs a folder where the telemetry for one or more trackers will be stored.

In that folder, each tracker should create its own node, with the same name as the tracker callsign.

That node should contain a single value named "sentence", containing the UKHAS format position of the tracker.

That sentence should contain the callsign, an (ignored) counter, an (ignored, currently) timestamp, latitude, longitude and altitude.  Further fields including any CRC are ignored.

So for example you could use a path of:

payloads/

which contains an entry

MQTT

with a single value of

sentence = $MQTT,123,10:11:12,55.123,-2.90,128



Usage
=======

	python mqtt_sondehub.py <gateway_callsign> <mqtt_broker> <mqtt_path> [<mqtt_username> <mqtt_password>]

The gateway can uplink messages to the tracker.  Currently this is restricted to time-based uplink slots using "UplinkTime" and "UplinkCycle".

- gateway_callsign: set to MQTT_GATEWAY or whatever you want; this appears as the receiver on the Sondehub map.
- mqtt_broker: this is the hostname or IP address for the MQTT broker that is receiving your telemetry
- mqtt_path: this is the path to the telemetry on the server
- mqtt_username and mqtt_password are only required if your MQTT broker requires them.

