extends CharacterBody2D
## Player controller: a 2D side-scrolling platformer with jump, drop-through,
## coyote time and jump buffering for a smooth, polished feel.
##
## Light/shadow mechanic: the player is "lit" while inside any light zone
## (group "light_zone") AND not inside any shadow zone (group "shadow_zone").
## Enemies only detect the player when `is_lit` is true.

@export var move_speed: float = 240.0
@export var jump_velocity: float = -560.0
@export var gravity: float = 1600.0
@export var max_fall_speed: float = 900.0
@export var drop_duration: float = 0.32
@export var one_way_layer: int = 4  # collision layer used by one-way platforms
@export var coyote_time: float = 0.1
@export var jump_buffer_time: float = 0.12
@export var squash_scale: float = 0.85

var is_lit: bool = false
var in_light: bool = false
var in_shadow: bool = false
var _facing: int = 1
var _drop_timer: float = 0.0
var _coyote: float = 0.0
var _jump_buffer: float = 0.0
var _was_on_floor: bool = false

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	add_to_group("player")

func _physics_process(delta: float) -> void:
	# --- gravity & terminal velocity ---
	if not is_on_floor():
		velocity.y = minf(velocity.y + gravity * delta, max_fall_speed)
	else:
		velocity.y = minf(velocity.y, 0.0)

	# --- coyote time ---
	_coyote = coyote_time if is_on_floor() else _coyote - delta

	# --- jump buffer ---
	if Input.is_action_just_pressed("jump"):
		_jump_buffer = jump_buffer_time
	else:
		_jump_buffer = maxf(_jump_buffer - delta, 0.0)

	# --- jump (honors buffer + coyote) ---
	if _jump_buffer > 0.0 and _coyote > 0.0 and _drop_timer <= 0.0:
		velocity.y = jump_velocity
		_jump_buffer = 0.0
		_coyote = 0.0
		_do_squash()

	# --- drop through one-way platforms: hold DOWN + press JUMP while on floor ---
	if Input.is_action_pressed("move_down") and Input.is_action_just_pressed("jump") and is_on_floor():
		_start_drop()

	# --- horizontal movement ---
	var dir := Input.get_axis("move_left", "move_right")
	velocity.x = dir * move_speed
	if absf(dir) > 0.01:
		_facing = int(signf(dir))
		sprite.flip_h = dir < 0.0

	_update_drop(delta)

	# --- flag for squash on landing ---
	var was_on_floor := is_on_floor()
	move_and_slide()
	if not was_on_floor and is_on_floor():
		_do_squash()

	_update_lit()

func _start_drop() -> void:
	_drop_timer = drop_duration
	set_collision_mask_value(one_way_layer, false)

func _update_drop(delta: float) -> void:
	if _drop_timer <= 0.0:
		return
	_drop_timer -= delta
	if _drop_timer <= 0.0:
		set_collision_mask_value(one_way_layer, true)

func _update_lit() -> void:
	in_light = _overlaps_group("light_zone")
	in_shadow = _overlaps_group("shadow_zone")
	is_lit = in_light and not in_shadow

func _overlaps_group(group: String) -> bool:
	for area in get_tree().get_nodes_in_group(group):
		if area is Area2D and area.overlaps_body(self):
			return true
	return false

func _do_squash() -> void:
	sprite.scale.y = squash_scale
	var tween := create_tween()
	tween.tween_property(sprite, "scale:y", 1.0, 0.18) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
