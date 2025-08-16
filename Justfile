run: py

py:
	@python main.py

qt:
	@watchexec -w qml -r -- qml6 -I qml "qml/Main.qml"

qt-watch:
	@qml6 -I qml "qml/Main.qml"
