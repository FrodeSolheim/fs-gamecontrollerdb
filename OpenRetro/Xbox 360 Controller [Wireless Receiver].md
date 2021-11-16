# Xbox 360 Controller [Wireless Receiver]

There does not seem to be any difference in behavior ID if white controllers or
newer black controllers are used with the receiver. Tested with full black,
black/grey and white controllers

## linux-usb-xinput

Note for Linux: D-pad registers as both a hat (h0) and buttons (b11..b14).
While other controllers in "Xinput mode", e.g. 8BitDo SN30 Pro (6,0,11,1) only
uses d-pad and has 4 less buttons. Logitech F510 (6,0,11,1) also has 11 buttons
and 1 hat. PowerA Mini Pro EX (6,0,11,1) likewise.

    030000005e040000a102000000010000,Xbox 360 Wireless Receiver,a:b0,b:b1,back:b6,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b8,leftshoulder:b4,leftstick:b9,lefttrigger:a2,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b10,righttrigger:a5,rightx:a3,righty:a4,start:b7,x:b2,y:b3,platform:Linux,
    axes:6,balls:0,buttons:15,hats:1,

With buttons instead of hat
// 030000005e040000a102000000010000,Xbox 360 Wireless Receiver,a:b0,b:b1,back:b6,dpdown:b14,dpleft:b11,dpright:b12,dpup:b13,guide:b8,leftshoulder:b4,leftstick:b9,lefttrigger:a2,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b10,righttrigger:a5,rightx:a3,righty:a4,start:b7,x:b2,y:b3,platform:Linux,
// axes:6,balls:0,buttons:15,hats:1,

##  windows-usb-xinput

    030000005e040000a102000000007801,XInput Controller #1,a:b0,b:b1,back:b6,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b10,leftshoulder:b4,leftstick:b8,lefttrigger:a2,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b9,righttrigger:a5,rightx:a3,righty:a4,start:b7,x:b2,y:b3,platform:Windows,
    axes:6,balls:0,buttons:11,hats:1,

## windows-usb-xinput-disabled

FIXME: Incorrect axis mapping!!
Left trigger axis from 0 -> pos, right trigger (same axis) 0 -> neg

    030000005e040000a102000000000000,Controller (Xbox 360 Wireless Receiver for Windows),a:b0,b:b1,back:b6,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,leftshoulder:b4,leftstick:b8,lefttrigger:+a2,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b9,righttrigger:-a2,rightx:a3,righty:a4,start:b7,x:b2,y:b3,platform:Windows,
    axes:5,balls:0,buttons:10,hats:1,
