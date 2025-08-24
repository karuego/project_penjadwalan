run: py

py:
	@python main.py

qt:
	@qml6 -I qml "qml/Main.qml"

qt-watch:
	@watchexec -w qml -r -- qml6 -I qml "qml/Main.qml"
