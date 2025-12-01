[confirm: "Continue?"]
@foo PARAM_1="hello" PARAM_2="world":
	echo {{ PARAM_1 }} {{ PARAM_2 }}

run: py

py:
	uv run myapp

watch:
	@watchexec -w src/myapp -r -- uv run myapp

py-watch:
	@watchexec -w src/myapp -r -- uv run myapp

debug:
	@uv run python -m myapp

qt:
	@qml6 -I src/myapp/qml "src/myapp/qml/Main.qml"

qt-watch:
	@watchexec -w src/myapp/qml -r -- qml6 -I src/myapp/qml "src/myapp/qml/Main.qml"

[group('lint')]
lint-py:
	#

[group('lint')]
lint-qt:
	qmllint src/myapp/qml/Main.qml
