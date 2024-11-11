
# import music stuff

from defs import *

# import textual

from textual.app import App, ComposeResult
from textual.widgets import *
from textual.containers import *
from textual.screen import *

class MenuScreen(Screen):
	def compose(self) -> ComposeResult:
		yield Header()

		yield Footer()

class MusicApp(App):
	CSS_PATH = 'style.tcss'
	def on_mount(self) -> None:
		self.push_screen(MenuScreen())

if __name__ == '__main__':
	app = MusicApp()
	app.run()