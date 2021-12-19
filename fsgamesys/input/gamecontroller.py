import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from typing_extensions import TypedDict

from fsgamesys.input.inputdevice import HatState

log = logging.getLogger(__name__)


class ParseError(Exception):
    pass


class GameControllerBindType(Enum):
    BUTTON = "BUTTON"
    AXIS = "AXIS"
    HAT = "HAT"


# class HatState(IntEnum):
#     CENTERED = 0
#     UP = 1
#     RIGHT = 2
#     DOWN = 4
#     LEFT = 8
#     RIGHTUP = 3
#     RIGHTDOWN = 6
#     LEFTUP = 9
#     LEFTDOWN = 12

# HatDirectionSdlConfig = Literal["up", "right", "down", "left"]


@dataclass
class GameControllerBind:
    # FIXME: Consider making this a read-only data class to make copying
    # gamecontrollerconfigs safer.
    type: GameControllerBindType
    button: int = -1
    axis: int = -1
    hat: int = -1
    axisDirection: int = 0
    axisInverted: bool = False
    hatMask: int = 0

    def getHatDirection(self) -> str:  # HatDirectionSdlConfig:
        if self.hatMask & HatState.UP:
            return "up"
        elif self.hatMask & HatState.RIGHT:
            return "right"
        elif self.hatMask & HatState.DOWN:
            return "down"
        elif self.hatMask & HatState.LEFT:
            return "left"
        else:
            raise ValueError(f"No hat direction (mask: {self.hatMask})")

    def getHatDirectionMask(self) -> int:
        if self.hatMask & HatState.UP:
            return 1
        elif self.hatMask & HatState.RIGHT:
            return 2
        elif self.hatMask & HatState.DOWN:
            return 4
        elif self.hatMask & HatState.LEFT:
            return 8
        else:
            raise ValueError(f"No hat direction (mask: {self.hatMask})")

    def toDescription(self) -> str:
        if self.type == GameControllerBindType.BUTTON:
            return f"Button {self.button + 1}"
        elif self.type == GameControllerBindType.AXIS:
            if self.axisDirection > 0:
                directionStr = "+"
            elif self.axisDirection < 0:
                directionStr = "-"
            else:
                directionStr = ""
            if self.axisInverted:
                invertedStr = " (inv)"
            else:
                invertedStr = ""
            return f"Axis {self.axis + 1}{directionStr}{invertedStr}"
        elif self.type == GameControllerBindType.HAT:
            return f"Hat {self.hat + 1} {self.getHatDirection()}"
        else:
            return "Unknown bind"

    def toString(self) -> str:
        if self.type == GameControllerBindType.BUTTON:
            return f"b{self.button}"
        elif self.type == GameControllerBindType.AXIS:
            if self.axisDirection > 0:
                directionStr = "+"
            elif self.axisDirection < 0:
                directionStr = "-"
            else:
                directionStr = ""
            if self.axisInverted:
                invertedStr = "~"
            else:
                invertedStr = ""
            return f"{directionStr}a{self.axis}{invertedStr}"
        elif self.type == GameControllerBindType.HAT:
            # direction: HatDirectionSdlConfig = self.getHatDirectionMask()
            return f"h{self.hat}.{self.getHatDirectionMask()}"
        else:
            return "Unknown bind"

    def toLegacyConfig(self) -> str:
        if self.type == GameControllerBindType.BUTTON:
            return f"button_{self.button}"
        elif self.type == GameControllerBindType.AXIS:
            if self.axisDirection > 0:
                directionStr = "_pos"
            elif self.axisDirection < 0:
                directionStr = "_neg"
            else:
                directionStr = ""
            # if self.axisInverted:
            #     invertedStr = "~"
            # else:
            #     invertedStr = ""
            return f"axis_{self.axis}{directionStr}"
        elif self.type == GameControllerBindType.HAT:
            # direction: HatDirectionSdlConfig = self.getHatDirectionMask()
            return f"hat_{self.hat}_{self.getHatDirection()}"
        else:
            return ""


# SDL_CONTROLLER_BUTTON_A
# SDL_CONTROLLER_BUTTON_B
# SDL_CONTROLLER_BUTTON_X
# SDL_CONTROLLER_BUTTON_Y
# SDL_CONTROLLER_BUTTON_BACK
# SDL_CONTROLLER_BUTTON_GUIDE
# SDL_CONTROLLER_BUTTON_START
# SDL_CONTROLLER_BUTTON_LEFTSTICK
# SDL_CONTROLLER_BUTTON_RIGHTSTICK
# SDL_CONTROLLER_BUTTON_LEFTSHOULDER
# SDL_CONTROLLER_BUTTON_RIGHTSHOULDER
# SDL_CONTROLLER_BUTTON_DPAD_UP
# SDL_CONTROLLER_BUTTON_DPAD_DOWN
# SDL_CONTROLLER_BUTTON_DPAD_LEFT
# SDL_CONTROLLER_BUTTON_DPAD_RIGHT
# SDL_CONTROLLER_AXIS_LEFTX
# SDL_CONTROLLER_AXIS_LEFTY
# SDL_CONTROLLER_AXIS_RIGHTX
# SDL_CONTROLLER_AXIS_RIGHTY
# SDL_CONTROLLER_AXIS_TRIGGERLEFT
# SDL_CONTROLLER_AXIS_TRIGGERRIGHT


class GameControllerItem(Enum):
    A = "A"
    BACK = "BACK"
    B = "B"
    DPAD_DOWN = "DPAD_DOWN"
    DPAD_LEFT = "DPAD_LEFT"
    DPAD_RIGHT = "DPAD_RIGHT"
    DPAD_UP = "DPAD_UP"
    GUIDE = "GUIDE"
    LEFTSHOULDER = "LEFTSHOULDER"
    LEFTSTICK = "LEFTSTICK"
    LEFTX = "LEFTX"
    LEFTX_NEG = "_LEFTX_NEG"
    LEFTX_POS = "_LEFTX_POS"
    LEFTY = "LEFTY"
    LEFTY_NEG = "_LEFTY_NEG"
    LEFTY_POS = "_LEFTY_POS"
    MISC1 = "MISC1"
    RIGHTSHOULDER = "RIGHTSHOULDER"
    RIGHTSTICK = "RIGHTSTICK"
    RIGHTX_NEG = "_RIGHTX_NEG"
    RIGHTX_POS = "_RIGHTX_POS"
    RIGHTX = "RIGHTX"
    RIGHTY_NEG = "_RIGHTY_NEG"
    RIGHTY_POS = "_RIGHTY_POS"
    RIGHTY = "RIGHTY"
    START = "START"
    TOUCHPAD = "TOUCHPAD"
    TRIGGERLEFT = "TRIGGERLEFT"
    TRIGGERRIGHT = "TRIGGERRIGHT"
    X = "X"
    Y = "Y"


# @dataclass
# class GameControllerMapping:
#     a: Optional[GameControllerBind] = None
#     b: Optional[GameControllerBind] = None
#     x: Optional[GameControllerBind] = None
#     y: Optional[GameControllerBind] = None
#     back: Optional[GameControllerBind] = None


# GameControllerMapping = Dict[GameControllerItem, GameControllerBind

configItemMapping = {
    "a": GameControllerItem.A,
    "back": GameControllerItem.BACK,
    "b": GameControllerItem.B,
    "dpdown": GameControllerItem.DPAD_DOWN,
    "dpleft": GameControllerItem.DPAD_LEFT,
    "dpright": GameControllerItem.DPAD_RIGHT,
    "dpup": GameControllerItem.DPAD_UP,
    "guide": GameControllerItem.GUIDE,
    "leftshoulder": GameControllerItem.LEFTSHOULDER,
    "leftstick": GameControllerItem.LEFTSTICK,
    "lefttrigger": GameControllerItem.TRIGGERLEFT,
    "leftx": GameControllerItem.LEFTX,
    "lefty": GameControllerItem.LEFTY,
    "misc1": GameControllerItem.MISC1,
    "rightshoulder": GameControllerItem.RIGHTSHOULDER,
    "rightstick": GameControllerItem.RIGHTSTICK,
    "righttrigger": GameControllerItem.TRIGGERRIGHT,
    "rightx": GameControllerItem.RIGHTX,
    "righty": GameControllerItem.RIGHTY,
    "start": GameControllerItem.START,
    "touchpad": GameControllerItem.TOUCHPAD,
    "x": GameControllerItem.X,
    "y": GameControllerItem.Y,
}


class GameControllerMapping:
    def __init__(self) -> None:
        self.guid = ""
        self.name = ""
        self.source = ""
        self.platform = ""
        self.binds: Dict[GameControllerItem, GameControllerBind] = {}
        self.extra = ""

        # self.deviceName: Optional[str] = None
        # self.numAxes: Optional[int] = None
        # self.numBalls: Optional[int] = None
        # self.numButtons: Optional[int] = None
        # self.numHats: Optional[int] = None

    def copy(self) -> "GameControllerMapping":
        new = GameControllerMapping()
        new.guid = self.guid
        new.name = self.name
        new.source = self.source
        new.platform = self.platform
        new.binds = self.binds.copy()
        new.extra = self.extra
        return new

    @classmethod
    def fromString(
        cls, mappingStr: str, strict: bool = False
    ) -> "GameControllerMapping":
        log.debug("Parse mapping %r", mappingStr)
        mapping = GameControllerMapping()
        parts = mappingStr.split(",")
        if len(parts) < 2:
            log.warning("Ignored mapping for %r (too few parts)", mappingStr)
            if strict:
                raise Exception("Too few parts")
            return mapping
        mapping.guid = parts[0].lower()
        mapping.name = parts[1].strip()
        for part in parts[2:]:
            if not part:
                continue
            try:
                itemStr, bindStr = part.split(":")
                item = cls.parseItem(itemStr)
                bind = cls.parseBind(bindStr, strict=strict)
                if item and bind:
                    mapping.binds[item] = bind
            except Exception as e:
                log.exception("Exception while parsing mapping part %r", part)
                if strict:
                    raise ParseError(e)
        return mapping

    @classmethod
    def parseItem(cls, itemStr: str) -> Optional[GameControllerItem]:
        assert itemStr
        return configItemMapping.get(itemStr, None)

    @classmethod
    def parseBind(cls, bindStr: str, strict: bool = False) -> Optional[GameControllerBind]:
        if not bindStr:
            return None
        first = bindStr[0]
        bindStr = bindStr[1:]
        if first in "a+-":
            bind = GameControllerBind(GameControllerBindType.AXIS)
            if first == "+":
                bind.axisDirection = 1
            elif first == "-":
                bind.axisDirection = -1
            if bind.axisDirection:
                assert bindStr[0] == "a"
                bindStr = bindStr[1:]
            if bindStr.endswith("~"):
                bind.axisInverted = True
                bindStr = bindStr[:-1]
            bind.axis = int(bindStr)
            return bind
        elif first == "b":
            bind = GameControllerBind(GameControllerBindType.BUTTON)
            bind.button = int(bindStr)
            return bind
        elif first == "h":
            bind = GameControllerBind(GameControllerBindType.HAT)
            hat, direction = bindStr.split(".")
            bind.hat = int(hat)
            if direction == "1":
                bind.hatMask = HatState.UP
            elif direction == "2":
                bind.hatMask = HatState.RIGHT
            elif direction == "4":
                bind.hatMask = HatState.DOWN
            elif direction == "8":
                bind.hatMask = HatState.LEFT
            else:
                log.warning("Unrecognized hat direction/mask (%r)", bindStr)
                if strict:
                    raise ParseError(bindStr)
            return bind
        return None

    def toString(self) -> str:
        parts: List[str] = []
        parts.append(self.guid)
        parts.append(self.name.replace(",", "%2C"))

        # for itemName, item in configItemMapping.items():
        for configName in sorted(configItemMapping):
            item = configItemMapping[configName]
            if item in self.binds:
                parts.append(f"{configName}:{self.binds[item].toString()}")
        parts.append(f"platform:{self.platform}")
        return ",".join(parts)
        # return "FIXME: {}".format(self.binds)

    def __str__(self) -> str:
        return self.toString()

    def __repr__(self) -> str:
        return "<GameControllerMapping {}>".format(self.toString())


class GameControllerConfig(TypedDict):
    pass


class GameController:
    pass
