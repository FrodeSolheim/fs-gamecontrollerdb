#!/usr/bin/env python3

import os


def main():
    mappings = {}
    for fileName in sorted(os.listdir("Data/GameControllerDB"), reverse=True):
        print(fileName)
        with open(os.path.join("Data/GameControllerDB", fileName), "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if len(line) > 32 and line[32] == ",":
                    guid = line[:32]
                    if guid not in mappings:
                        mappings[guid] = line
                        # print(guid)
    with open("gamecontrollerdb.txt", "w", newline="\n") as f:
        for guid in sorted(mappings.keys()):
            f.write(mappings[guid])
            f.write("\n")


if __name__ == "__main__":
    main()
