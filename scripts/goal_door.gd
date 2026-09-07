extends Area2D
## Goal door: completes the level when the player enters it.
## Plays a chime, and tells GameManager to advance.

@export var level_id: int = 1
var _finished: bool = false

func _ready() -> void:
	add_to_group("goal")
	collision_layer = 0
	collision_mask = 1
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node) -> void:
	if _finished:
		return
	if body.is_in_group("player"):
		_finished = true
		_play_sfx()
		var gm := get_node_or_null("/root/GameManager")
		if gm and gm.has_method("notify_level_complete"):
			gm.notify_level_complete()

func _play_sfx() -> void:
	var ap := AudioStreamPlayer.new()
	ap.name = "Sfx"
	add_child(ap)
	var path := "res://assets/audio/goal.wav"
	if ResourceLoader.exists(path):
		ap.stream = load(path)
		ap.volume_db = -6.0
		ap.play()
