################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, math, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import serial
import time

sout = None

def swrite(msg):
    global sout
    sout.write(msg)
    print(msg)

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        self.next_update = time.time()
        self.update_interval = 1.0/10.0
        self.last_r = 0
        self.last_g = 0
        self.last_b = 0
        self.last_m = 0
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if(time.time() >= self.next_update):
            self.next_update += self.update_interval
            out_str = "{r:%d,g:%d,b:%d,m:%d}" % (self.last_r,self.last_g,self.last_b,self.last_m)
            swrite(out_str)

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            # fingers = hand.fingers
            # if not fingers.is_empty:
            #     # Calculate the hand's average finger tip position
            #     avg_pos = Leap.Vector()
            #     for finger in fingers:
            #         avg_pos += finger.tip_position
            #     avg_pos /= len(fingers)
            #     print "Hand has %d fingers, average finger tip position: %s" % (
            #           len(fingers), avg_pos)

            # # Get the hand's sphere radius and palm position
            # print "Hand sphere radius: %f mm, palm position: %s" % (
            #       hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            x = hand.palm_position.x
            y = hand.palm_position.y
            z = hand.palm_position.z
            d = math.sqrt(x*x+y*y+z*z)

            self.last_r = 255 if math.fabs(x) > 255 else math.fabs(x)
            self.last_g = 255 if math.fabs(y) > 255 else math.fabs(y)
            self.last_b = 255 if math.fabs(z) > 255 else math.fabs(z)
            self.last_m = 255 if math.fabs(d/2) > 255 else math.fabs(d/2)

            # print "(%d, %d, %d) -> distance: %d" % (x, y, z, d)

            # # Calculate the hand's pitch, roll, and yaw angles
            # print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #     direction.pitch * Leap.RAD_TO_DEG,
            #     normal.roll * Leap.RAD_TO_DEG,
            #     direction.yaw * Leap.RAD_TO_DEG)

            # Gestures

            # for gesture in frame.gestures():

            #     if gesture.state == Leap.Gesture.STATE_STOP:
            #         print "*** Gesture completed ***"

            #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
            #         circle = CircleGesture(gesture)

            #         # Determine clock direction using the angle between the pointable and the circle normal
            #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
            #             clockwiseness = "clockwise"
            #         else:
            #             clockwiseness = "counterclockwise"

            #         # Calculate the angle swept since the last frame
            #         swept_angle = 0
            #         if circle.state != Leap.Gesture.STATE_START:
            #             previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
            #             swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

            #         print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            #     if gesture.type == Leap.Gesture.TYPE_SWIPE:
            #         swipe = SwipeGesture(gesture)
            #         print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 swipe.position, swipe.direction, swipe.speed)

            #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
            #         keytap = KeyTapGesture(gesture)
            #         print "Key Tap id: %d, %s, position: %s, direction: %s" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 keytap.position, keytap.direction )

            #     if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
            #         screentap = ScreenTapGesture(gesture)
            #         print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
            #                 gesture.id, self.state_string(gesture.state),
            #                 screentap.position, screentap.direction )
        else:
            self.last_r = 0
            self.last_g = 0
            self.last_b = 0
            self.last_m = 0

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            # print ""
            pass

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():

    global sout
    port_name = raw_input("Enter Arduino port name: ")
    sout = serial.Serial(port_name, 9600, timeout=0)
    print("Initializing...")
    time.sleep(3)

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

    swrite("{r:0,g:0,b:0,m:0}")


if __name__ == "__main__":
    main()
