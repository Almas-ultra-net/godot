extends Area2D
## Base class for any light source (campfire, lantern, etc.).
## Maintains a "light_zone" group marking the area that makes the player
## visible to enemies, plus a soft PointLight2D to light the scene.
##
## The lit region is a circle defined by `light_radius`. `PointLight2D` shows
## the visible glow. The player is considered lit while overlapping this Area2D
## (see player.gd).

@export var light_radius: float = 180.0
@export var light_energy: float = 1.5
@export var light_color: Color = Color(1.0, 0.82, 0.55)
@export var flicker: bool = true
@export var flicker_amount: float = 0.08
@export var start_enabled: bool = true

var enabled: bool = true

@onready var _light: PointLight2D = $PointLight2D

func _ready() -> void:
	add_to_group("light_zone")
	enabled = start_enabled
	_ensure_collision()
	_ensure_point_light()
	set_enabled(enabled)

func _process(_delta: float) -> void:
	if not enabled or not flicker:
		return
	if not _light:
		return
	# Subtle fire flicker via energy noise.
	var t := Time.get_ticks_msec() * 0.001
	var n := sin(t * 12.0) * 0.5 + sin(t * 27.0 + 1.3) * 0.35 + sin(t * 5.0 + 2.1) * 0.15
	_light.energy = light_energy * (1.0 + n * flicker_amount)

func _ensure_collision() -> void:
	# The Area2D's collision shape defines the lit region.
	for c in get_children():
		if c is CollisionShape2D:
			return
	var shape := CircleShape2D.new()
	shape.radius = light_radius
	var cs := CollisionShape2D.new()
	cs.shape = shape
	add_child(cs)
	collision_layer = 0
	collision_mask = 1

func _ensure_point_light() -> void:
	# Children added at runtime; look up lazily in case scene already has one.
	var light := PointLight2D.new()
	light.name = "PointLight2D"
	light.texture = load("res://assets/sprites/light_mask.png")
	light.energy = light_energy
	light.color = light_color
	light.texture_scale = light_radius / 128.0
	light.blend_mode = PointLight2D.BLEND_MODE_ADD
	add_child(light)

func set_enabled(value: bool) -> void:
	enabled = value
	for c in get_children():
		if c is PointLight2D:
			c.visible = enabled
		elif c is CollisionShape2D:
			c.disabled = not enabled
