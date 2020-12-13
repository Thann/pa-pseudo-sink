#!/usr/bin/env python
# PulseAudio Pseudo Sink
# Creates a dummy output so you can isolate sounds from different applications.

import os
import gi
import re
import sys
import signal
import argparse
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk
from subprocess import run


class PseudoSink:
    def __init__(self, args=[]):
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname(__file__), "main.ui"))
        builder.connect_signals(self)
        self.window = builder.get_object("main-window")

        self.selected_output = None
        self.button_box = builder.get_object('button-box')

        # Check for preexisting sink
        sinks = run(['pactl', 'list', 'short', 'sinks'], capture_output=True)
        outputs = [l.split(b'\t')
                   for l in sinks.stdout.splitlines()
                   if b'alsa_output' in l]

        psink = [l.split(b'\t')
                 for l in sinks.stdout.splitlines()
                 if b'PseudoSink' in l]

        pcombo = [l.split(b'\t')
                  for l in sinks.stdout.splitlines()
                  if b'PseudoCombined' in l]

        selected = None
        if pcombo:
            print("PREVIOUSLY SETUP COMBO!", pcombo[0])
            modules = run(['pactl', 'list', 'short', 'modules'], capture_output=True)
            cmod = [l.split(b'\t', 2)
                    for l in modules.stdout.splitlines()
                    if b'PseudoCombined' in l]
            match = re.search(b"slaves=(\d+),", cmod[0][2])
            onum = match.group(1)
            selected = onum

        # Clear button box
        for btn in self.button_box.get_children():
            btn.destroy()

        # Build button box
        btn1 = None
        for o in outputs:
            # TODO: get human-readable name
            btn = Gtk.RadioButton.new_with_label_from_widget(btn1, o[1].decode('utf8'))
            if selected and o[0] == selected:
                btn.set_active(True)
            btn.connect('toggled', self.toggled)
            self.button_box.add(btn)
            if not btn1:
                btn1 = btn

        if not psink:
            # Create PseudoSink
            run(['pactl', 'load-module', 'module-null-sink', 'sink_name="PseudoSink"',
                 'sink_properties=device.description="PseudoSink"'], capture_output=True)

        if not selected:
            btn1.emit('toggled')
        self.window.show_all()

    def onDestroy(self, *args):
        # TODO: self.unload() ?
        Gtk.main_quit()

    def unload(self):
        modules = run(['pactl', 'list', 'short', 'modules'], capture_output=True)
        for line in modules.stdout.splitlines():
            s = l.split(b'\t', 1)
            if b'PseudoSink' in s[1] or b'PseudoCombined' in s[1]:
                run(['pactl', 'unload-module', s[0]], capture_output=True)

    def toggled(self, btn):
        if btn.get_active():
            modules = run(['pactl', 'list', 'short', 'modules'], capture_output=True)
            pcombo = [l.split(b'\t')
                      for l in modules.stdout.splitlines()
                      if b'PseudoCombined' in l]
            if pcombo:
                print('Deleting old combo:', pcombo)
                output2 = run(['pactl', 'unload-module', pcombo[0][0]], capture_output=True)

            sinks = run(['pactl', 'list', 'short', 'sinks'], capture_output=True)

            # Get sink numbers
            psink = None
            output = None
            for l in sinks.stdout.splitlines():
                s = l.split(b'\t')
                name = s[1].decode('utf8')
                if name == 'PseudoSink':
                    psink = s[0].decode('utf8')
                elif name == btn.get_label():
                    output = s[0].decode('utf8')

            # Create combined sink
            output2 = run(['pactl', 'load-module', 'module-combine-sink',
                          f'slaves={output},{psink}', 'sink_name=PseudoCombined'], capture_output=True)
            print("CREATE_COMBO_SYNC:", output2)


def start():
    win = PseudoSink(sys.argv)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, win.onDestroy)
    Gtk.main()

if __name__ == "__main__":
    start()
