import keyboard
import time
from enum import IntEnum


# CONSTANTS
class SpecialKeys(IntEnum):
	BACKSPACE = 0x4a
	NEXT = 0x4e
	ENTER = 0x1c
	SPACE = 0x52
	CAPS = 0x53
	NUM_LOCK = 0x45


__special_keys = [0x4a, 0x4e, 0x1c, 0x52, 0x53]
__keypad = {
	0x47: [',', '.'],  # NUMPAD 7
	0x48: ['A', 'B', 'C'],  # NUMPAD 8
	0x49: ['D', 'E', 'F'],  # NUMPAD 9
	0x4b: ['G', 'H', 'I'],  # NUMPAD 4
	0x4c: ['J', 'K', 'L'],  # NUMPAD 5
	0x4d: ['M', 'N', 'O'],  # NUMPAD 6
	0x4f: ['P', 'Q', 'R', 'S'],  # NUMPAD 1
	0x50: ['T', 'U', 'V'],  # NUMPAD 2
	0x51: ['W', 'X', 'Y', 'Z'],  # NUMPAD 3
	0x35: ['\'', '"'],
	0x37: ['!', '?']
}
__time_cooldown = 1
__time_last_press = 0
__caps_lock = False

# DATA
__current = {
	"code": None,
	"time": 0,
	"character_id": -1
}


def get_capslock_state():
	from win32api import GetKeyState
	from win32con import VK_CAPITAL
	return GetKeyState(VK_CAPITAL)


def reset():
	__current["code"] = None
	__current["time"] = None
	__current["character_id"] = -1


def write():
	global __time_last_press
	_write = __keypad[__current["code"]][__current["character_id"] % len(__keypad[__current["code"]])]
	if __caps_lock:
		_write = _write.upper()
	else:
		_write = _write.lower()
	keyboard.write(_write)
	print("Write %s" % _write)
	reset()
	__time_last_press = 0


def handle_event(callback):
	global __time_last_press, __caps_lock

	if callback.event_type != "up":
		return
	else:
		pass
		# print("name: %s / scan code: %s / time: %s" % (callback.name, hex(callback.scan_code), callback.time))

	if callback.scan_code in __special_keys:
		# CAPS lock
		if callback.scan_code == SpecialKeys.CAPS:
			__caps_lock = not __caps_lock
		# Del
		if callback.scan_code == SpecialKeys.BACKSPACE:
			_code = 0x0e
			if __current["code"] is None:
				keyboard.send(_code)
			else:
				reset()
		# Next
		if callback.scan_code == SpecialKeys.NEXT:
			if __current["code"] is not None:
				write()
		# Enter: Acts like Next first, if something is in current
		if callback.scan_code == SpecialKeys.ENTER:
			if __current["code"] is not None:
				write()
			keyboard.send(0x1c)
		# Space
		if callback.scan_code == SpecialKeys.SPACE:
			if __current["code"] is not None:
				write()
			keyboard.send(0x39)
		# ToDo: Numlock
		return

	if callback.scan_code not in __keypad:
		return

	__time_last_press = callback.time

	if __current["code"] == callback.scan_code:
		pass
	elif __current["code"] is not None:
		write()
		pass
	else:
		pass

	__current["code"] = callback.scan_code
	__current["character_id"] += 1
	__current["time"] = callback.time


def keypad_process():
	while True:
		time.sleep(0.1)
		if __time_last_press > 0 and time.time() - __time_last_press > __time_cooldown:
			if __current["code"] is not None:
				write()


if __name__ == "__main__":
	#my_hook = keyboard.hook(handle_event, suppress=True)
	for _code in __special_keys:
		keyboard.hook_key(_code, handle_event, suppress=True)
	for _code in __keypad:
		keyboard.hook_key(_code, handle_event, suppress=True)
	keypad_process()
