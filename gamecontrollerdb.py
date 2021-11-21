#!/usr/bin/env python3

import os


def main() -> None:
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
                    if line.endswith(","):
                        line = line[:-1]
                    platform = line.split(",")[-1]
                    assert platform.startswith("platform:")
                    platform = platform[len("platform:") :]
                    if (guid, platform.lower()) not in mappings:
                        mappings[(guid, platform.lower())] = line
    with open("gamecontrollerdb.txt", "w", newline="\n") as f:
        for key in sorted(mappings.keys()):
            f.write(mappings[key])
            f.write("\n")


if __name__ == "__main__":
    main()
