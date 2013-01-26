# yo
import urwid
import sys

file_name = sys.argv[1]
file_lines = open(file_name, "r").readlines()

def exit_on_q(key):
	""" default keyboard handler """
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()

def menu(title, choices):
	""" builds the menu out of lines of text """
	body = [urwid.Text(title), urwid.Divider()]
	for c in choices:
		button = urwid.Button(c)
		urwid.connect_signal(button, 'click', item_chosen, c)
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def open_location_or_ignore(button):
	exit_on_q('q')


def item_chosen(button, choice):
	""" performs action on a selected line """
	print(choice)
	open_location_or_ignore(button)

main = urwid.Padding(menu(file_name, file_lines), left=2, right=0)
urwid.MainLoop(main, palette=[('reversed', 'standout', '')], unhandled_input=exit_on_q).run()
