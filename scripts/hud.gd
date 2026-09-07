extends CanvasLayer
## Heads-up display: score, an interact hint, a flexible status line and a
## subtle vignette/legend.

var _elapsed: float = 0.0
var _running: bool = true

@onready var score_label: Label = $ScoreLabel
@onready var hint_label: Label = $HintLabel
@onready var status_label: Label = $StatusLabel
@onready var timer_label: Label = $TimerLabel

func _ready() -> void:
	add_to_group("hud")
	update_score(GameManager.score)
	hint_label.text = "A/D move   Space jump   Down+Space drop   E interact"
	status_label.text = ""
	start_timer()

func _process(delta: float) -> void:
	if _running:
		_elapsed += delta
	timer_label.text = "Time: %02d:%02d" % [int(_elapsed) / 60, int(_elapsed) % 60]

func start_timer() -> void:
	_elapsed = 0.0
	_running = true

func update_score(value: int) -> void:
	score_label.text = "Light Shards: %d" % value

func show_status(text: String, duration: float = 2.0) -> void:
	status_label.text = text
	var tween := create_tween()
	tween.tween_interval(duration)
	tween.tween_callback(func() -> void:
		status_label.text = ""
	)

func stop_timer() -> void:
	_running = false
