[confirm: "Continue?"]
@foo PARAM_1="hello" PARAM_2="world":
	echo {{ PARAM_1 }} {{ PARAM_2 }}

run: py

py:
	@python main.py

qt:
	@qml6 -I qml "qml/Main.qml"

qt-watch:
	@watchexec -w qml -r -- just qt

lint: lint-qt lint-py

lint-py:
	#

lint-qt:
	qmllint qml/Main.qml
