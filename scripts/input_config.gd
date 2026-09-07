extends Node
## Autoload that registers the input actions used by the game.
## Doing this in code keeps project.godot simple and robust across versions.

func _enter_tree() -> void:
	# action -> array of keys
	var actions := {
		"move_left": [KEY_A, KEY_LEFT],
		"move_right": [KEY_D, KEY_RIGHT],
		"move_up": [KEY_W, KEY_UP],
		"move_down": [KEY_S, KEY_DOWN],
		"jump": [KEY_SPACE, KEY_Z],
		"interact": [KEY_E, KEY_ENTER],
		"toggle_light": [KEY_F, KEY_X],
		"pause": [KEY_ESCAPE],
	}

	for action in actions:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for key in actions[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = key
			if not _action_has_key(action, key):
				InputMap.action_add_event(action, ev)

func _action_has_key(action: String, key: int) -> bool:
	for ev in InputMap.action_get_events(action):
		if ev is InputEventKey and ev.physical_keycode == key:
			return true
	return false
