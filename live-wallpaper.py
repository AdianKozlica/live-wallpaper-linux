#!/usr/bin/python3

import gi
import os
import sys
import magic

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gdk, Gst, GstVideo
from urllib.request import pathname2url
from urllib.parse import urljoin

class VideoPlayer(Gtk.Window):
    def __init__(self, file_path: str):
        super().__init__(title="Live Wallpaper")
        self.set_focus(None)
        self.maximize()
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)
        
        # Initialize GStreamer
        Gst.init(None)

        self.pipeline = Gst.ElementFactory.make("playbin", "player")

        # Create a GTK Video area and add to the window
        self.video_area = Gtk.DrawingArea()
        self.video_area.set_double_buffered(True)
        self.add(self.video_area)

        # Connect the video_area's "realize" signal to handle the video overlay
        self.video_area.connect("realize", self.on_realize)

        # Set the URI of the video
        self.pipeline.set_property('uri', file_path)

        self.pipeline.set_property('volume', 0.0) # Mute audio

        # Start playing
        self.pipeline.set_state(Gst.State.PLAYING)

        # Cleanup on window close
        self.connect("delete-event", self.on_delete_event)

        # Setup loop on EOS
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos)

    def on_realize(self, widget):
        # We need to make sure the widget is realized, i.e., it has a window and is part of the windowing system
        window = widget.get_window()

        if not window:
            sys.stderr.write("Widget is not realized!\n")

        # Make sure we have a native window for the video overlay to work
        if not window.ensure_native():
            sys.stderr.write("Couldn't create native window needed for video overlay!\n")

        # Retrieve the XID of the widget's window, which is needed for the video overlay
        win_id = window.get_xid()

        # Pass the XID to the GStreamer pipeline so it knows where to render the video
        overlay = self.pipeline.get_by_interface(GstVideo.VideoOverlay)
        if overlay:
            overlay.set_window_handle(win_id)
        else:
            sys.stderr.write("Failed to overlay the video on the window.\n")

    def on_delete_event(self, widget, event):
        # Stop the GStreamer pipeline when the window is closed
        self.pipeline.set_state(Gst.State.NULL)

    def on_eos(self, bus, msg):
        # Handle End of Stream message to loop playback
        self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)

def main(file_path: str):
    app = VideoPlayer(file_path)
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Missing filename!\n")
        exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        sys.stderr.write("Invalid video file!\n")
        exit(1)

    absolute_file_path = os.path.abspath(filename)
    file_mime = magic.from_file(absolute_file_path, mime=True)

    if not file_mime.startswith("video/"):
        sys.stderr.write("File is not a video!\n")
        exit(1)

    file_url = urljoin('file://', pathname2url(absolute_file_path))
    main(file_url)