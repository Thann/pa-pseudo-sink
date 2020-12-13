# PulseAudio Pseudo Sink
Creates a dummy output so you can isolate sounds from different applications.

### Usage
When streaming with OBS. Set the "Desktop Audio" to "PseudoSink",
then use something like `pavucontrol` to direct applications to "PseudoSink" if you want it to only beheard on stream.
Select "Combined Output" if you want to stream AND hear it.

