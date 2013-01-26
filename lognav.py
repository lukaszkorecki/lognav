# yo
import urwid
import line_walker
import sys

file_name = sys.argv[1]



def exit_on_q(key):
	""" default keyboard handler """
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()

def menu(title, file_walker):
	""" builds the menu out of lines of text """
	return urwid.ListBox(file_walker)

def open_location_or_ignore(button):
	exit_on_q('q')


def item_chosen(button, choice):
	""" performs action on a selected line """
	response = urwid.Text([u'You chose ', choice, u'\n'])
	done = urwid.Button(u'Ok')
	urwid.connect_signal(done, 'click', exit_on_q)
	main.original_widget = urwid.Filler(urwid.Pile([response,
		urwid.AttrMap(done, None, focus_map='reversed')]))

walker = line_walker.LineWalker(file_name, item_chosen)

main = urwid.Padding(menu(file_name, walker), left=2, right=0)
urwid.MainLoop(main, palette=[('reversed', 'standout', '')], unhandled_input=exit_on_q).run()
