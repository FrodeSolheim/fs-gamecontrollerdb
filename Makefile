all: \
		Data/GameControllerDB/25-SDL_GameControllerDB.txt \
		Data/GameControllerDB/50-SDL2.txt

Data:
	mkdir -p Data

Data/GameControllerDB: Data
	mkdir -p Data/GameControllerDB

Data/GameControllerDB/25-SDL_GameControllerDB.txt: \
		SDL_GameControllerDB.txt \
		Data/GameControllerDB
	cp SDL_GameControllerDB.txt $@
	unix2dos $@

Data/GameControllerDB/50-SDL2.txt: \
		SDL/SDL_gamecontrollerdb.h SDL.py \
		Data/GameControllerDB
	python3 SDL.py $@
	unix2dos $@
