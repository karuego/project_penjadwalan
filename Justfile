[confirm: "Continue?"]
@foo PARAM_1="hello" PARAM_2="world":
	echo {{ PARAM_1 }} {{ PARAM_2 }}

run: py

py:
	@python main.py

qt:
	@qml6 -I qml "qml/Main.qml"

qt-watch:
	@watchexec -w qml -r -- qml6 -I qml "qml/Main.qml"

[group('lint')]
lint-py:
	#

[group('lint')]
lint-qt:
	qmllint qml/Main.qml
