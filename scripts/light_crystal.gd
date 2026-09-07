extends Area2D
## A collectible light crystal. Adds score when picked up, then disappears.
## Bobs gently and plays a pickup sound.

@export var value: int = 1
var collected: bool = false

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	add_to_group("collectible")
	collision_layer = 0
	collision_mask = 1
	body_entered.connect(_on_body_entered)
	_play_idle()

func _on_body_entered(body: Node) -> void:
	if collected:
		return
	if body.is_in_group("player"):
		collected = true
		var gm := get_node_or_null("/root/GameManager")
		if gm and gm.has_method("add_score"):
			gm.add_score(value)
		_play_sfx()
		queue_free()

func _play_sfx() -> void:
	var ap := AudioStreamPlayer.new()
	ap.name = "Sfx"
	add_child(ap)
	var path := "res://assets/audio/pickup.wav"
	if ResourceLoader.exists(path):
		ap.stream = load(path)
		ap.volume_db = -4.0
		ap.play()

func _play_idle() -> void:
	var base_y := sprite.position.y
	var tween := create_tween()
	tween.set_loops()
	var bob_up := tween.tween_property(sprite, "position:y", base_y - 6.0, 0.9)
	bob_up.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	var bob_down := tween.tween_property(sprite, "position:y", base_y, 0.9)
	bob_down.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
