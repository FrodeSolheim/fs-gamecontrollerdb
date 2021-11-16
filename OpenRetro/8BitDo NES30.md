# 8BitDo NES30

FIXME: Name, NES30 vs N30 or something like that?

Looks like there is maybe only one USB mode, but four BT modes:
- Switch mode simulates Joy-Con controllers?
- XInput mode simulates Xbox One Controller
- macOS mode simulates PS4 Controller
- "DirectInput" mod

The device can switch how the d-pad is mapped: SELECT + left/down/right. It
seems to be mapped to axis 0/1 by default, so the mapping is created
accordingly. Another way would be to map axis -> axis and hat -> hat.

## linux-bt-dinput

    05000000c82d00002028000000010000,8Bitdo NES30 GamePad,a:b1,b:b0,back:b10,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b6,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Linux,
    axes:6,balls:0,buttons:16,hats:1,

##  linux-bt-macos

[64115.203415] sony 0005:054C:05C4.001E: unknown main item tag 0x0
[64115.410325] sony 0005:054C:05C4.001E: Failed to get calibration data from Dualshock 4
[64115.411019] sony 0005:054C:05C4.001E: hidraw3: BLUETOOTH HID v81.00 Gamepad [Wireless Controller] on 5c:f3:70:68:d3:fe
[64115.411024] sony 0005:054C:05C4.001E: failed to claim input

## linux-bt-switch

Not responding

## linux-bt-xinput

    050000005e040000e002000003090000,8Bitdo NES30 GamePad(x),a:b0,b:b1,back:b6,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b4,rightshoulder:b5,start:b7,x:b2,y:b3,platform:Linux,
    axes:6,balls:0,buttons:11,hats:1,

## linux-usb

    03000000c82d000012ab000010010000,NES30              NES30 Joystick,a:b1,b:b0,back:b10,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b6,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Linux,
    axes:4,balls:0,buttons:12,hats:1,

## macos-bt-dinput

    03000000c82d00002028000000010000,8Bitdo NES30 GamePad,a:b1,b:b0,back:b10,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b6,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Mac OS X,
    axes:6,balls:0,buttons:16,hats:1,

## macos-bt-macos

    030000004c050000c405000000016800,PS4 Controller,a:b0,b:b1,back:b4,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b9,rightshoulder:b10,start:b6,x:b2,y:b3,platform:Mac OS X,
    axes:6,balls:0,buttons:16,hats:0,

## macos-bt-switch

Not responding

# 030000007e0500000720000001000000,Pro Controller,platform:Mac OS X

## macos-bt-xinput

    030000005e040000e002000003090000,8Bitdo NES30 GamePad(x),a:b0,b:b1,back:b6,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b4,rightshoulder:b5,start:b7,x:b2,y:b3,platform:Mac OS X,
    axes:6,balls:0,buttons:11,hats:1,

## macos-usb-dinput

    03000000c82d000012ab000001000000,NES30 Joystick,a:b1,b:b0,back:b10,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b6,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Mac OS X,
    axes:4,balls:0,buttons:12,hats:1,

## windows-bt-dinput

    03000000c82d00002028000000000000,Bluetooth Wireless Controller   ,a:b1,b:b0,back:b10,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b6,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Windows,
    axes:6,balls:0,buttons:16,hats:1,

## windows-bt-macos

Not detected

## windows-bt-switch

Not detected

## windows-bt-xinput

    030000005e040000e002000000007801,XInput Controller #1,a:b0,b:b1,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b4,rightshoulder:b5,x:b2,y:b3,platform:Windows,
    axes:6,balls:0,buttons:11,hats:1,

## windows-bt-xinput-disabled

Not responding

## windows-usb 

    03000000c82d000012ab000000000000,NES30 Joystick,a:b1,b:b0,back:b10,dpdown:+a1,dpleft:-a0,dpright:+a0,dpup:-a1,leftshoulder:b6,rightshoulder:b7,start:b11,x:b4,y:b3,platform:Windows,
    axes:4,balls:0,buttons:12,hats:1,
