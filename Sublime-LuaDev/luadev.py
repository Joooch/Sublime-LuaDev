import sublime, sublime_plugin, socket, os

def getcode(inst):
	return inst.view.substr(sublime.Region(0, inst.view.size()))

def getsource(inst):
	return os.path.basename(inst.view.file_name() or "Unnamed")

def send(inst, method, to=None):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("127.0.0.1", 27099))
	
	sock.sendall(
		method.encode() + b"\n" +
		getsource(inst).encode() + b"\n" +
		(to.encode() + b"\n" if to else b"") +
		getcode(inst).encode()
	)
	
	sock.close()

def sendmessage(inst, method, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("127.0.0.1", 27099))
	
	sock.sendall(
		method.encode() + b"\n" +
		message.encode()
	)
	
	sock.close()
class lua_send_selfCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		send(self, "self")

class lua_send_svCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		send(self, "sv")

class lua_send_shCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		send(self, "sh")

class lua_send_clCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		send(self, "cl")

class lua_send_entCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		send(self, "ent")

class lua_send_wepCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		send(self, "wep")

class lua_send_clientCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel("Which player?", "", self.on_done, None, None)
	
	def on_done(self, input):
		if len(input) <= 0:
			return
		send(self, "client", input)
