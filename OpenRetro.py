#!/usr/bin/env python3
import os
import sys
import traceback
from typing import Dict, List, Optional, Tuple
from typing_extensions import TypedDict

# Read "common" controllers (often simulated by other controllers) first,
# then we can check that other controllers are compatible (using a subset)
# of the mapping of the genuine controllers

priority_list = [
    "PS3 Controller.txt",
    "PS4 Controller.txt",
    "PS4 Controller [v2].txt",
    "Switch Pro Controller.txt",
    "Xbox 360 Controller.txt",
    "Xbox 360 Controller [Wireless Receiver].txt",
    "Xbox Controller.txt [Series X].txt",
    "Xbox One Controller.txt",
    "Xbox One Controller [2013].txt",
    "Xbox One Controller [2016 S].txt",
]


class Mapping(TypedDict):
    guid: str
    name: str
    platform: str
    mapping: Dict[str, str]


def addFromLine(
    mappings: Dict[Tuple[str, str], Mapping],
    errors: List[str],
    fileName: str,
    line: str,
    mapping: Optional[Dict[str, str]] = None,
):
    if line.startswith("axes:"):
        return
    if line.endswith(","):
        line = line[:-1]
    parts = line.split(",")
    guid = parts.pop(0)
    name = parts.pop(0)
    platform = parts.pop()
    mappingKey = (guid, platform)
    new: Mapping = {
        "guid": guid,
        "name": name,
        "platform": platform,
        "mapping": {},
    }
    for part in parts:
        key, value = part.split(":")
        new["mapping"][key] = value
        if mapping is not None:
            mapping[key] = value

    if mappingKey in mappings:
        old = mappings[mappingKey]
        # Some Xbox-compatible controllers have only dpad but report this as
        # axes. Allow this exception and handle as compatible mapping.
        dpad_using_axes = False
        # ps4 = "PS4 Controller" in file_name
        ps4 = guid in ["030000004c050000c405000000016800"]
        mac_swith_pro = guid in ["030000007e0500000920000001006800"]
        if mac_swith_pro:
            # Same exceptions
            ps4 = True
        for key, new_value in new["mapping"].items():
            old_value = old["mapping"].get(key, "[N/A]")
            if key == "dpup" and new_value == "-a1" and old_value == "h0.1":
                dpad_using_axes = True
            elif (
                key == "dpright" and new_value == "+a0" and old_value == "h0.2"
            ):
                dpad_using_axes = True
            elif (
                key == "dpdown" and new_value == "+a1" and old_value == "h0.4"
            ):
                dpad_using_axes = True
            elif (
                key == "dpleft" and new_value == "-a0" and old_value == "h0.8"
            ):
                dpad_using_axes = True
            elif (
                ps4
                and key == "dpup"
                and new_value == "-a1"
                and old_value == "b11"
            ):
                dpad_using_axes = True
            elif (
                ps4
                and key == "dpright"
                and new_value == "+a0"
                and old_value == "b14"
            ):
                dpad_using_axes = True
            elif (
                ps4
                and key == "dpdown"
                and new_value == "+a1"
                and old_value == "b12"
            ):
                dpad_using_axes = True
            elif (
                ps4
                and key == "dpleft"
                and new_value == "-a0"
                and old_value == "b13"
            ):
                dpad_using_axes = True
            elif new_value != old_value:
                errors.append(
                    "Incompatible config: {} -- {}:{} vs existing {}:{}".format(
                        line, key, new_value, key, old_value
                    )
                )
                return
        if dpad_using_axes:
            print(" - '{}' uses axes for d-pad (allowed)".format(new["name"]))
        return

    if os.path.basename(fileName) == "gamecontrollerdb.txt":
        # Keep using name from mapping entry
        pass
    else:
        # Override controller name from file name
        name = os.path.splitext(os.path.basename(fileName))[0]
        name = name.split("[")[0].strip()
        new["name"] = name
    mappings[mappingKey] = new

    # Sanity checking, for example: make sure leftstick is mapped to a
    # button press and not an axis.
    if os.path.basename(fileName) == "gamecontrollerdb.txt":
        return
    for key in ["leftstick", "rightstick"]:
        value = new["mapping"].get(key, "")
        if value and not value.startswith("b"):
            errors.append(
                "{} is not mapped from button ({})".format(key, value)
            )


def addFromFile(
    mappings: Dict[Tuple[str, str], Mapping],
    errors: List[str],
    fileName: str,
    singleController: bool = False,
):
    print(fileName)
    markdown = fileName.endswith(".md")
    modeMap: Dict[str, List[Dict[str, str]]] = {}
    with open(fileName, "r") as f:
        mode = ""
        for line in f:
            line = line.strip()
            if line.startswith("#") and "-usb" in line:
                mode = line.split("-usb")[-1]
            elif line.startswith("#") and "-bt" in line:
                mode = line.split("-bt")[-1]
            if mode.startswith("-"):
                mode = mode[1:]

            # if markdown and not line.startswith(" "):
            #     continue
            # if not line.startswith("03") and not line.startswith("05"):
            #     continue
            first_32 = line[:32]
            if not len(first_32) == 32:
                continue
            hex_32 = False
            for c in first_32:
                if c not in "0123456789abcdef":
                    break
            else:
                hex_32 = True
            if not hex_32:
                continue
            # if line.startswith("05"):
            #     pass
            # if not line:
            #     continue
            # if line.startswith("#"):
            #     continue
            # if line.startswith("("):
            #     continue

            mapping: Dict[str, str] = {}
            try:
                addFromLine(mappings, errors, fileName, line, mapping)
            except:
                traceback.print_exc()
                errors.append("ERROR in {}: {}".format(fileName, line))
            else:
                if singleController:
                    # print(mode, mapping)
                    modeMap.setdefault(mode, []).append(mapping)
                    # print("mode:", mode)
    if singleController:
        allOk = True
        exceptions = False
        for mode in modeMap.keys():
            m1 = modeMap[mode].pop(0)
            # print(mapping)
            for m2 in modeMap[mode]:
                # if mode == "xinput" and m1[]
                m1_mod, exceptions_1 = fixMapping(m1, mode)
                m2_mod, exceptions_2 = fixMapping(m2, mode)
                if exceptions_1 or exceptions_2:
                    exceptions = True
                if m1_mod != m2_mod:
                    print("")
                    print(
                        "Mismatch in",
                        fileName,
                        "mode =",
                        mode if mode else "(default)",
                    )
                    print("")
                    print(m1)
                    print("\ndoes not equal\n")
                    print(m2)
                    print("")
                    allOk = False
        if allOk:
            if exceptions:
                print(" - XInput exceptions allowed")
            print(" - all mappings with same mode match")


def fixMapping(m, mode):
    m2 = m.copy()
    exceptions = False
    if (
        mode == "xinput"
        and m.get("guide", "") == "b8"
        and m.get("leftstick", "") == "b9"
        and m.get("rightstick", "") == "b10"
    ):
        m2["guide"] = "b10"
        m2["leftstick"] = "b8"
        m2["rightstick"] = "b9"
        exceptions = True
    return m2, exceptions


sdlLicense = """\
Simple DirectMedia Layer
Copyright (C) 1997-2020 Sam Lantinga <slouken@libsdl.org>

This software is provided 'as-is', without any express or implied
warranty.  In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution."""

ignoredWarnings = [
    # Missing guide button locally.
    "Incompatible config: 05000000050b00000045000040000000,ASUS Gamepad,a:b0,b:b1,back:b9,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b6,leftshoulder:b4,leftstick:b7,lefttrigger:a5,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b8,righttrigger:a4,rightx:a2,righty:a3,start:b10,x:b2,y:b3,platform:Linux -- guide:b6 vs existing guide:[N/A]",
    # Using "SEGA" mapping locally.
    "Incompatible config: 03000000a30600000901000000010000,Saitek P880,a:b2,b:b3,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b4,leftstick:b8,lefttrigger:b6,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b9,righttrigger:b7,rightx:a3,righty:a2,x:b0,y:b1,platform:Linux -- leftshoulder:b4 vs existing leftshoulder:b6",
    # Ignoring possibly mixup between 8BitDo SN30 (locally) and 8BitDo SN30
    # Pro (gamecontrollerdb) for now.
    "Incompatible config: 03000000c82d00001290000011010000,8BitDo SN30 Pro,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a3,righty:a4,start:b11,x:b4,y:b3,platform:Linux -- dpdown:h0.4 vs existing dpdown:+a1",
    "Incompatible config: 05000000c82d00006228000000010000,8BitDo SN30 Pro,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a2,righty:a3,start:b11,x:b4,y:b3,platform:Linux -- dpdown:h0.4 vs existing dpdown:+a1",
    "Incompatible config: 03000000c82d00002028000000000000,8BitDo N30,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b2,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a2,righty:a5,start:b11,x:b4,y:b3,platform:Windows -- dpdown:h0.4 vs existing dpdown:+a1",
    # Ignoring guide button mismatch for now.
    "Incompatible config: 03000000550900001072000011010000,NVIDIA Controller,a:b0,b:b1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b13,leftshoulder:b4,leftstick:b8,lefttrigger:a5,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b9,righttrigger:a4,rightx:a2,righty:a3,start:b7,x:b2,y:b3,platform:Linux -- guide:b13 vs existing guide:b15",
    # 8BitDo SFC30 Gamepad: I mapped against d-pad and not axes. Maybe submit
    # fix / at least discuss.
    "Incompatible config: 05000000c82d00003028000000010000,8Bitdo SFC30 GamePad,a:b1,b:b0,back:b10,leftshoulder:b6,leftx:a0,lefty:a1,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Linux -- leftx:a0 vs existing leftx:[N/A]",
    # Joy-Con... don't want to deal with these right now.
    "Incompatible config: 050000007e0500000620000001000000,Joy-Con (L),+leftx:h0.2,+lefty:h0.4,-leftx:h0.8,-lefty:h0.1,a:b0,b:b1,back:b13,leftshoulder:b4,leftstick:b10,rightshoulder:b5,start:b8,x:b2,y:b3,platform:Linux -- back:b13 vs existing back:b8",
    # Needs be to be filed against upstream / SDL2 :-/
    "Incompatible config: 03000000a00500003232000000000000,8Bitdo Zero GamePad,a:b0,b:b1,back:b10,dpdown:+a2,dpleft:-a0,dpright:+a0,dpup:-a2,leftshoulder:b6,rightshoulder:b7,start:b11,x:b3,y:b4,platform:Windows -- dpdown:+a2 vs existing dpdown:+a1",
    # Xbox 360 controllers use both buttons and a hat, so both configs work.
    "Incompatible config: 030000005e040000a102000000010000,X360 Wireless Controller,a:b0,b:b1,back:b6,dpdown:b14,dpleft:b11,dpright:b12,dpup:b13,guide:b8,leftshoulder:b4,leftstick:b9,lefttrigger:a2,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b10,righttrigger:a5,rightx:a3,righty:a4,start:b7,x:b2,y:b3,platform:Linux -- dpdown:b14 vs existing dpdown:h0.4",
    # Speed-Link Competition Pro, second button as B/East or X/West?
    "Incompatible config: 030000000b0400003365000000010000,Competition Pro,a:b0,b:b1,back:b2,leftx:a0,lefty:a1,start:b3,platform:Linux -- b:b1 vs existing b:[N/A]",
    # Silence for now...
    "Incompatible config: 030000005509000000b4000000000000,USB gamepad,a:b10,b:b11,back:b5,dpdown:b1,dpleft:b2,dpright:b3,dpup:b0,guide:b14,leftshoulder:b8,leftstick:b6,lefttrigger:a4,leftx:a0,lefty:a1,rightshoulder:b9,rightstick:b7,righttrigger:a5,rightx:a2,righty:a3,start:b4,x:b12,y:b13,platform:Windows -- a:b10 vs existing a:b0",
    "Incompatible config: 03000000c82d00000650000001000000,8BitDo M30,a:b0,b:b1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b8,lefttrigger:b9,leftx:a0,lefty:a1,rightshoulder:b6,righttrigger:b7,start:b11,x:b3,y:b4,platform:Mac OS X -- dpdown:h0.4 vs existing dpdown:+a1",
    "Incompatible config: 03000000c82d00000161000000010000,8BitDo SN30 Pro,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b2,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a2,righty:a5,start:b11,x:b4,y:b3,platform:Mac OS X -- righty:a5 vs existing righty:a3",
    "Incompatible config: 03000000c82d00001590000011010000,8BitDo N30 Pro 2,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a2,righty:a3,start:b11,x:b4,y:b3,platform:Linux -- dpleft:h0.8 vs existing dpleft:+a5",
    "Incompatible config: 05000000c82d00006528000000010000,8BitDo N30 Pro 2,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a2,righty:a3,start:b11,x:b4,y:b3,platform:Linux -- lefttrigger:b8 vs existing lefttrigger:a5",
]


def main() -> None:
    fileNames: List[Tuple[int, str]] = []
    for fileName in os.listdir("OpenRetro"):
        if fileName in [".gitignore"]:
            continue
        elif fileName.endswith(".swp"):
            continue
        elif fileName.endswith(".txt") or fileName.endswith(".md"):
            fileNames.append(
                (
                    0 if fileName in priority_list else 1,
                    os.path.join("OpenRetro", fileName),
                )
            )
        else:
            print("")
            print("ERROR: Unrecognized file", fileName)
            print("")
            sys.exit(1)
    fileNames.sort()

    mappings: Dict[Tuple[str, str], Mapping] = {}
    errors: List[str] = []

    for fileName2 in fileNames:
        addFromFile(mappings, errors, fileName2[1], singleController=True)

    if errors:
        print("")
        print("There were errors:")
        for error in errors:
            print(error)
        print("")
        sys.exit(1)

    # with open("gamecontrollerdb_split.txt", "w", newline="\n") as f:
    #     for mapping_id in sorted(mappings.keys()):
    #         info = mappings[mapping_id]
    #         f.write("{},\n".format(info["guid"]))
    #         f.write("{},\n".format(info["name"]))
    #         for key in sorted(info["mapping"].keys()):
    #             value = info["mapping"][key]
    #             f.write("{}:{},\n".format(key, value))
    #         f.write("{},\n".format(info["platform"]))

    with open(sys.argv[1], "w") as f:
        for mapping_id in sorted(mappings.keys()):
            info = mappings[mapping_id]
            f.write("{},".format(info["guid"]))
            f.write("{},".format(info["name"]))
            for key in sorted(info["mapping"].keys()):
                value = info["mapping"][key]
                f.write("{}:{},".format(key, value))
            f.write("{},\n".format(info["platform"]))

    addFromFile(mappings, errors, "SDL_GameControllerDB/gamecontrollerdb.txt")
    if errors:
        print("")
        print("There were warnings:")
        ignore_count = 0
        for error in errors:
            if error in ignoredWarnings:
                ignore_count += 1
            else:
                print(error)
        if ignore_count > 0:
            print("... ignored {} warning(s)".format(ignore_count))
        print("")

    with open("fsemu-sdlgamecontrollerdb.c", "w", newline="\n") as f:
        f.write("#define FSEMU_INTERNAL\n")
        f.write('#include "fsemu-sdlgamecontrollerdb.h"\n')
        f.write("\n")
        f.write("#include <stddef.h>\n")
        f.write("\n")
        f.write(
            "// Mappings are sourced from - and prioritized - in this order:\n"
        )
        f.write("// 1. Verified configurations by FSEMU contributors\n")
        f.write("// 2. The SDL project itself\n")
        f.write("// 3. https://github.com/gabomdq/SDL_GameControllerDB\n")
        f.write("//\n")
        f.write(
            "// The list is auto-generated and sorted by platform and GUID.\n"
        )
        f.write(
            "// The following license applies specifically to this file:\n"
        )
        f.write("//\n")
        for line in sdlLicense.split("\n"):
            f.write("// {}".format(line).strip() + "\n")
        f.write("\n")
        f.write("// clang-format off\n")
        f.write("const char *fsemu_sdlgamecontrollerdb_mappings[] = {\n")
        for platform in ["Linux", "Mac OS X", "Windows"]:
            platform_define = "FSEMU_OS_" + platform.upper()
            if platform_define == "FSEMU_OS_MAC OS X":
                platform_define = "FSEMU_OS_MACOS"
            f.write("#ifdef {}\n".format(platform_define))
            for mapping_id in sorted(mappings.keys()):
                info = mappings[mapping_id]
                if info["platform"] != "platform:{}".format(platform):
                    continue
                f.write('"')
                f.write("{},".format(info["guid"]))
                # f.write("{},".format(info["name"]))
                f.write('"\n"{},"\n"'.format(info["name"]))
                for key in sorted(info["mapping"].keys()):
                    value = info["mapping"][key]
                    f.write("{}:{},".format(key, value))
                f.write('",\n')
            f.write("#endif\n")
        f.write("NULL\n")
        f.write("};\n")
        f.write("// clang-format on\n")


if __name__ == "__main__":
    main()
