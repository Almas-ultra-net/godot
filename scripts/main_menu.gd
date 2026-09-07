extends Control
## Main menu / title screen. A focused start button and a quit button.
## Keyboard: Enter to start, Esc to quit.

@onready var start_button: Button = $Panel/Center/VBox/StartButton
@onready var quit_button: Button = $Panel/Center/VBox/QuitButton

func _ready() -> void:
	start_button.grab_focus()
	start_button.pressed.connect(_on_start)
	quit_button.pressed.connect(_on_quit)

func _on_start() -> void:
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func _on_quit() -> void:
	get_tree().quit()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact") or event.is_action_pressed("jump"):
		_on_start()
	if event.is_action_pressed("pause"):
		_on_quit()
