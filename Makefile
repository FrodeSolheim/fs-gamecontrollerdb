all: \
		Data/GameControllerDB/25-SDL_GameControllerDB.txt \
		Data/GameControllerDB/50-SDL2.txt \
		Data/GameControllerDB/75-OpenRetro.txt \
		gamecontrollerdb.txt

Data/GameControllerDB/25-SDL_GameControllerDB.txt: \
		SDL_GameControllerDB/gamecontrollerdb.txt
	mkdir -p Data/GameControllerDB
	cp SDL_GameControllerDB/gamecontrollerdb.txt $@
	unix2dos $@

Data/GameControllerDB/50-SDL2.txt: \
		SDL/SDL_gamecontrollerdb.h \
		SDL.py
	mkdir -p Data/GameControllerDB
	python3 SDL.py $@
	unix2dos $@

Data/GameControllerDB/75-OpenRetro.txt: \
		OpenRetro/*.txt \
		OpenRetro.py
	mkdir -p Data/GameControllerDB
	python3 OpenRetro.py $@
	unix2dos $@

gamecontrollerdb.txt: \
		Data/GameControllerDB/25-SDL_GameControllerDB.txt \
		Data/GameControllerDB/50-SDL2.txt \
		Data/GameControllerDB/75-OpenRetro.txt \
		gamecontrollerdb.py
	python3 gamecontrollerdb.py

update-fsgamesys:
	mkdir -p fsgamesys/input
	cp ../fs-uae-launcher/fsgamesys/input/inputdevice.py fsgamesys/input/
	cp ../fs-uae-launcher/fsgamesys/input/gamecontroller.py fsgamesys/input/
