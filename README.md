# PulseAudio Pseudo Sink
Creates a dummy output so you can isolate sounds from different applications.

Requires: PulseAudio, Python & GTK  
Install: `pip install git+git://github.com/thann/pa-pseudo-sink --user`  
Run: `pseudo-sink`

### Usage
When streaming with OBS, Set the "Desktop Audio" to "PseudoSink",  
then use something like `pavucontrol` to direct applications to "PseudoSink"
if you want them to only be heard on stream.  
Select "Simultaneous" output if you want to stream AND hear them.

In The GUI, choose which audio device you want to "combine" with the PseudoSync,
so you can hear the apps that are sent to the "Simultaneous" output.

