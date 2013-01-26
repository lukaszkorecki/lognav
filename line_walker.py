# ListWalker compatibile class, adopted from http://excess.org/urwid/browser/examples/edit.py

import urwid

class LineWalker(urwid.ListWalker):
	"""ListWalker-compatible class for lazily reading file contents."""

	def __init__(self, name, on_click_callback):
		self.file = open(name)
		self.lines = []
		self.focus = 0
		self.on_click_callback = on_click_callback

	def get_focus(self):
		return self._get_at_pos(self.focus)

	def set_focus(self, focus):
		self.focus = focus
		self._modified()

	def get_next(self, start_from):
		return self._get_at_pos(start_from + 1)

	def get_prev(self, start_from):
		return self._get_at_pos(start_from - 1)

	def read_next_line(self):
		"""Read another line from the file."""

		next_line = self.file.readline()

		if not next_line or next_line[-1:] != '\n':
			# no newline on last line of file
			self.file = None
		else:
			# trim newline characters
			next_line = next_line[:-1]

		expanded = next_line.expandtabs()

		button = urwid.Button(expanded)
		urwid.connect_signal(button, 'click', self.on_click_callback, expanded)
		self.lines.append(urwid.AttrMap(button, None, focus_map='reversed'))
		return next_line


	def _get_at_pos(self, pos):
		"""Return a widget for the line number passed."""

		if pos < 0:
			# line 0 is the start of the file, no more above
			return None, None

		if len(self.lines) > pos:
			# we have that line so return it
			return self.lines[pos], pos

		if self.file is None:
			# file is closed, so there are no more lines
			return None, None

		assert pos == len(self.lines), "out of order request?"

		self.read_next_line()

		return self.lines[-1], pos

	def combine_focus_with_prev(self):
		"""Combine the focus edit widget with the one above."""

		above, ignore = self.get_prev(self.focus)
		if above is None:
			# already at the top
			return

		focus = self.lines[self.focus]
		above.set_edit_pos(len(above.edit_text))
		above.set_edit_text(above.edit_text + focus.edit_text)
		del self.lines[self.focus]
		self.focus -= 1

	def combine_focus_with_next(self):
		"""Combine the focus edit widget with the one below."""

		below, ignore = self.get_next(self.focus)
		if below is None:
			# already at bottom
			return

		focus = self.lines[self.focus]
		focus.set_edit_text(focus.edit_text + below.edit_text)
		del self.lines[self.focus+1]
