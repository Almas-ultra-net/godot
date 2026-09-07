extends Node
## Global game state: score, caught/win flow, HUD helpers and level management.
## Registered as the autoload singleton "GameManager".

signal player_caught
signal level_complete

var score: int = 0
var level: int = 1
var max_level: int = 3
var _reset_id: int = 0

func _ready() -> void:
	add_to_group("game_manager")
	# Reset per-level state at launch.
	score = 0

func add_score(value: int = 1) -> void:
	score += value
	_update_hud()

func reset_level_state() -> void:
	# Reset per-entry state when a level loads.
	score = 0
	_update_hud()
	if get_tree().current_scene:
		# Let the HUD restart its timer via a custom call if present.
		var hud := get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("start_timer"):
			hud.start_timer()

func notify_caught() -> void:
	emit_signal("player_caught")
	print("You were caught in the light!")
	_hud_status("Caught! Restarting...")
	_reset_id += 1
	var rid := _reset_id
	get_tree().create_timer(0.9).timeout.connect(_reload.bind(rid))

func _reload(rid: int) -> void:
	if rid == _reset_id:
		get_tree().reload_current_scene()

func notify_level_complete() -> void:
	emit_signal("level_complete")
	print("Level %d complete! Shards: %d" % [level, score])
	_hud_status("Level complete!", 1.2)
	if level < max_level:
		level += 1
	else:
		level = 1
	get_tree().create_timer(1.5).timeout.connect(_next_level)

func _next_level() -> void:
	get_tree().reload_current_scene()

func _hud_status(text: String, dur: float = 2.0) -> void:
	var hud := get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("show_status"):
		hud.show_status(text, dur)

func _update_hud() -> void:
	var hud := get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("update_score"):
		hud.update_score(score)
