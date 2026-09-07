extends CharacterBody2D
## Guard: patrols back and forth, and chases only when the player is lit
## (standing in light and not covered by a shadow). Touching the player
## while chasing catches them and restarts the level.
##
## The guard has a FOV cone: it only detects the player when the player is
## lit, within detection_radius, AND in front of the guard's current facing.

enum State { IDLE, PATROL, CHASE }

@export var patrol_speed: float = 70.0
@export var chase_speed: float = 135.0
@export var detection_radius: float = 250.0
@export var gravity: float = 1600.0
@export_range(0.0, 600.0) var patrol_min: float = 0.0
@export_range(0.0, 600.0) var patrol_max: float = 0.0
@export var catch_distance: float = 34.0
@export var fov_degrees: float = 120.0

var state: int = State.PATROL
var player: Node = null
var face_dir: int = -1      # the direction the guard is currently looking/moving
var _patrol_dir: int = -1
var _det_radius_sq: float = 0.0

func _ready() -> void:
	add_to_group("enemy")
	player = get_tree().get_first_node_in_group("player")
	_det_radius_sq = detection_radius * detection_radius
	if patrol_max == 0.0 and patrol_min == 0.0:
		patrol_min = position.x - 140.0
		patrol_max = position.x + 140.0
	face_dir = _patrol_dir

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += gravity * delta

	var lit := false
	var dx := 0.0
	var dist_sq := INF

	if player:
		lit = player.get("is_lit") == true
		dx = player.global_position.x - global_position.x
		dist_sq = (player.global_position - global_position).length_squared()

	# Detect the player only when lit, in range, and in front of the guard.
	var visible := lit and dist_sq <= _det_radius_sq and _in_fov()

	if visible:
		state = State.CHASE
		face_dir = 1 if dx >= 0.0 else -1
		if dist_sq <= catch_distance * catch_distance:
			_catch_player()
			return
	else:
		state = State.PATROL

	match state:
		State.CHASE:
			velocity.x = face_dir * chase_speed
			$Sprite2D.flip_h = face_dir < 0
		_:
			velocity.x = _patrol_dir * patrol_speed
			if global_position.x <= patrol_min:
				_patrol_dir = 1
			elif global_position.x >= patrol_max:
				_patrol_dir = -1
			face_dir = _patrol_dir
			$Sprite2D.flip_h = _patrol_dir < 0

	move_and_slide()

func _in_fov() -> bool:
	if player == null:
		return false
	var to_player := player.global_position - global_position
	if to_player.length() < 1.0:
		return true
	var facing := Vector2(face_dir, 0.0)
	var cos_angle := to_player.normalized().dot(facing)
	var half := deg_to_rad(fov_degrees * 0.5)
	return cos_angle >= cos(half)

func _catch_player() -> void:
	var gm := get_node_or_null("/root/GameManager")
	if gm and gm.has_method("notify_caught"):
		gm.notify_caught()
