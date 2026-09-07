extends "res://scripts/light_source.gd"
## A movable hand lantern. It is a light source like the campfire, but
## represents a light that can be toggled/relocated by puzzles. For now it
## simply reuses the base light with a tighter, warmer glow.

var carried: bool = false

func _ready() -> void:
	light_radius = 150.0
	light_energy = 1.4
	light_color = Color(1.0, 0.86, 0.6)
	super._ready()
