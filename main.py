import strings
import os
import sys
import argparse

def desktop_toggle(state=None, running_on_desktop=None):
    # If the state is true enable desktop.
    if state == None: pass

    # Here we handle the desktop / cli change taking a effect.
    if running_on_desktop:
        if state:
            os.system('pkexec systemctl set-default multi-user')
        else:
            os.system('pkexec systemctl set-default graphical.target')
    else:
        pass

# Check where we are running. If it's a desktop show the GUI other wise it's a cli interface.
if os.environ['XDG_SESSION_TYPE'] == 'tty':
    parser = argparse.ArgumentParser(description=strings.help_text)

    parser.add_argument('-mode', metavar='mode', type=int, nargs='+',
                    help='1 for desktop, or 2 for cli on boot.')
    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    desktop_toggle(args.mode, running_on_desktop=False)

    #print(args)
else:
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    class Main_Window(Gtk.Window):
        def __init__(self):
            super().__init__(title="OB: Desktop Switcher")
            self.set_default_size(640, 480)
            self.set_border_width(12)

            self._grid = Gtk.Grid()
            self._enable_btn = Gtk.Button(label="Enable")

            #set_focus_vadjustment(Gtk.Align.START)
            self._disable_btn = Gtk.Button(label="Disable")

            self._enable_btn.connect("clicked", self.on_enable_button_clicked)
            self._disable_btn.connect("clicked", self.on_disable_button_clicked)

            self._grid.attach(Gtk.Label(label=strings.help_text), 0, 0, 1, 1)
            self._grid.attach(self._enable_btn, 0, 1, 1, 1)
            self._grid.attach(self._disable_btn, 1, 1, 1, 1)
            self.add(self._grid)

        def on_enable_button_clicked(self, widget):
            desktop_toggle(True, running_on_desktop=True)

        def on_disable_button_clicked(self, widget):
            desktop_toggle(False, running_on_desktop=True)


    win = Main_Window()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
