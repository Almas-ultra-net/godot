extends StaticBody2D
## A stone pillar: a solid obstacle that also blocks light and casts a real
## shadow using a generated LightOccluder2D polygon.

@export var occluder_size: Vector2 = Vector2(44, 120)

func _ready() -> void:
	add_to_group("occluder")
	_create_occluder()

func _create_occluder() -> void:
	var occ := LightOccluder2D.new()
	var poly := OccluderPolygon2D.new()
	var hw := occluder_size.x * 0.5
	var hh := occluder_size.y * 0.5
	poly.polygon = PackedVector2Array([
		Vector2(-hw, -hh),
		Vector2(hw, -hh),
		Vector2(hw, hh),
		Vector2(-hw, hh),
	])
	occ.occluder = poly
	occ.position = Vector2(0, -60)  # align with the sprite visual
	add_child(occ)
