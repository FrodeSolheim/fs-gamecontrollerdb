import sys
from typing import Dict


class Mapping:
    guid: str = ""
    name: str = ""
    mapping: Dict[str, str] = {}
    hint: str = ""
    platform: str = ""


mappingKeys = set(
    [
        "a",
        "b",
        "back",
        "dpdown",
        "dpleft",
        "dpright",
        "dpup",
        "guide",
        "leftshoulder",
        "leftstick",
        "lefttrigger",
        "leftx",
        "lefty",
        "rightshoulder",
        "rightstick",
        "righttrigger",
        "rightx",
        "righty",
        "start",
        "x",
        "y",
        "+leftx",
        "+lefty",
        "+rightx",
        "+righty",
        "-leftx",
        "-lefty",
        "-rightx",
        "-righty",
        # ???
        "misc1",
        "paddle1",
        "paddle2",
        "paddle3",
        "paddle4",
    ]
)


def parseMapping(line: str, platform: str) -> Mapping:
    mapping = Mapping()
    assert line.startswith('"')
    line = line[1:]
    line = line.split("/*", 1)[0]
    line = line.split("//", 1)[0]
    parts = line.split(",")
    mapping.guid = parts.pop(0)
    mapping.name = parts.pop(0)
    for part in parts:
        part = part.strip(' "')
        if not part:
            continue
        # print(part)
        key, value = part.split(":", 1)
        if key == "hint":
            mapping.hint = value
        elif key in mappingKeys:
            mapping.mapping[key] = value
        else:
            raise Exception(f"Unexpected part {part!r}")
    mapping.platform = platform
    return mapping


def formatMapping(mapping: Mapping) -> str:
    parts = []
    parts.append(mapping.guid)
    parts.append(mapping.name)
    for key in sorted(mapping.mapping.keys()):
        value = mapping.mapping[key]
        parts.append(f"{key}:{value}")
    # FIXME: Include hint?
    parts.append(f"platform:{mapping.platform}")
    parts.append("")
    return ",".join(parts)


def main() -> None:
    mappings = {}
    with open("SDL/SDL_gamecontrollerdb.h", "r") as f:
        platform = ""
        for line in f:
            line = line.strip()
            if line.startswith("#if") or line.startswith("#el"):
                if "SDL_JOYSTICK_DINPUT" in line:
                    platform = "Windows"
                elif "__MACOSX__" in line:
                    platform = "MacOSX"
                elif "__LINUX__" in line:
                    platform = "Linux"
                else:
                    platform = ""
                continue
            elif line.startswith("#endif"):
                platform = ""
                continue
            if not line.startswith('"'):
                continue
            if not platform:
                continue
            print(platform, line)
            mapping = parseMapping(line, platform)
            if mapping.guid == "xinput":
                # Ignore this one, for now at least
                continue
            mappings[mapping.guid] = mapping

    with open(sys.argv[1], "w") as f:
        for guid in sorted(mappings.keys()):
            f.write(formatMapping(mappings[guid]))
            f.write("\n")
        count = len(mappings.keys())
        print(f"Wrote {count} mappings")


if __name__ == "__main__":
    main()
