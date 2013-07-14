#!/usr/bin/python3

from gi.repository import Gtk, Gdk

UI_INFO = """
<ui>
	<menubar name="MenuBar">
		<menu action="ConnectionsMenu">
			<menuitem action="ConnectionNew" />
		</menu>
	</menubar>
</ui>
"""

class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Pipe")
		self.button = Gtk.Button(label="Test")

		self.set_default_size(400,300)

		self.store = Gtk.ListStore(str, str, str)
		self.store.append(["Test", "192.168.128.1", "Verbunden"])
		self.store.append(["Test", "192.168.123.2", ""])
		
		self.view = Gtk.TreeView(self.store)
		self.view.append_column(Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=0))
		self.view.append_column(Gtk.TreeViewColumn("IP-Adresse", Gtk.CellRendererText(), text=1))
		self.view.append_column(Gtk.TreeViewColumn("Status", Gtk.CellRendererText(), text=2))
		
		action_group = Gtk.ActionGroup("actions")
		action_connection = Gtk.Action("ConnectionsMenu", "Verbindungen", None, None)
		action_group.add_action(action_connection)
		action_new_connection = Gtk.Action("ConnectionNew", "Neue Verbindung", None, None)
		action_new_connection.connect("activate", self.on_menu_connect)
		action_group.add_action(action_new_connection)

		uimanager = Gtk.UIManager()
		uimanager.add_ui_from_string(UI_INFO)
		uimanager.insert_action_group(action_group, 1)

		menubar = uimanager.get_widget("/MenuBar")
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box.pack_start(menubar, False, False, 0)
		box.pack_start(self.view, True, True, 0)

		self.button.connect("clicked", self.button_clicked)
		self.add(box)
		self.connect("delete-event", Gtk.main_quit)
		self.show_all()
	def button_clicked(self, widget):
		print("Test")

	def on_menu_connect(self, widget):
		print("Test")
