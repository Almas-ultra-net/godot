extends "res://scripts/light_source.gd"
## A fixed, always-available campfire. Inherits all light behaviour from
## light_source.gd and just tweaks the defaults.

func _ready() -> void:
	light_radius = 200.0
	light_energy = 1.7
	light_color = Color(1.0, 0.75, 0.45)
	super._ready()
