extends Area2D
## An interactable lever that toggles the nearest light source on/off.
## Player stands in range and presses the "interact" action (E).
## Plays a click sound, animates the handle, and shows a hint when in range.

var toggled: bool = false

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	add_to_group("interactable")
	collision_layer = 0
	collision_mask = 1

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact") and _player_in_range():
		_toggle()

func _player_in_range() -> bool:
	for body in get_overlapping_bodies():
		if body is Node and body.is_in_group("player"):
			return true
	return false

func _toggle() -> void:
	toggled = not toggled
	var light := _find_nearest_light()
	if light and light.has_method("set_enabled"):
		var currently_on: bool = light.enabled if ("enabled" in light) else true
		light.set_enabled(not currently_on)
		_play_sfx(not currently_on)
	# Animate the handle flip.
	var tween := create_tween()
	var target := -0.35 if toggled else 0.35
	tween.tween_property(sprite, "rotation", target, 0.16) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _play_sfx(on: bool) -> void:
	var ap := _sfx_player()
	if ap == null:
		return
	var path := "res://assets/audio/toggle_off.wav" if not on else "res://assets/audio/toggle_on.wav"
	if ResourceLoader.exists(path):
		ap.stream = load(path)
		ap.play()

func _sfx_player() -> AudioStreamPlayer:
	if has_node("Sfx"):
		return $Sfx
	var ap := AudioStreamPlayer.new()
	ap.name = "Sfx"
	add_child(ap)
	return ap

func _find_nearest_light() -> Node:
	var best: Node = null
	var best_dist := INF
	for l in get_tree().get_nodes_in_group("light_zone"):
		if l == self:
			continue
		var d := global_position.distance_squared_to(l.global_position)
		if d < best_dist:
			best_dist = d
			best = l
	return best
