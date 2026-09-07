extends Node2D
## A drifting cloud. It carries a "shadow zone" below it. While the player is
## inside that shadow they are considered hidden (is_lit = false) even if they
## are standing in the light.
##
## The cloud bobs gently, and its shadow follows it. A soft dark overlay can be
## toggled on the shadow Zone for visual feedback (optional).

@export var speed: float = 45.0
@export var patrol_left: float = 200.0
@export var patrol_right: float = 700.0
@export var shadow_width: float = 150.0
@export var shadow_height: float = 420.0
@export var shadow_offset_y: float = 340.0
@export var bob_amplitude: float = 6.0
@export var bob_speed: float = 1.2

var _dir: int = 1
var _t: float = 0.0

func _ready() -> void:
	add_to_group("cloud")
	_create_shadow()

func _physics_process(delta: float) -> void:
	_t += delta * bob_speed
	position.x += _dir * speed * delta
	if position.x <= patrol_left:
		_dir = 1
	elif position.x >= patrol_right:
		_dir = -1
	# soft vertical bob
	position.y = position.y + sin(_t) * bob_amplitude * delta
	if has_node("ShadowZone"):
		$ShadowZone.global_position = global_position + Vector2(0, shadow_offset_y)

func _create_shadow() -> void:
	var zone := Area2D.new()
	zone.name = "ShadowZone"
	zone.add_to_group("shadow_zone")
	zone.collision_layer = 0
	zone.collision_mask = 1
	var rect := RectangleShape2D.new()
	rect.size = Vector2(shadow_width, shadow_height)
	var cs := CollisionShape2D.new()
	cs.shape = rect
	zone.add_child(cs)
	add_child(zone)
	zone.global_position = global_position + Vector2(0, shadow_offset_y)
