#!/usr/bin/env python
#encoding: utf8
import rospy, actionlib
from std_msgs.msg import UInt16
from pimouse_ros.msg import MusicAction, MusicResult, MusicFeedback

def write_freq(hz=0):
    bfile = "/dev/rtbuzzer0"
    try:
       with open(bfile,"w") as f:
           f.write(str(hz) + "\n")
    except IOError:
        rospy.logerr("cant't write to " + bfile)

def recv_buzzer(data):
    write_freq(data.data)

def exec_music(goal):
    r = MusicResult()                                   #ｲﾝｽﾀﾝｽ
    fb = MusicFeedback()                                #ｲﾝｽﾀﾝｽ

    for i, f in enumerate(goal.freqs):                  #i=順番 f=要素
        fb.remaining_steps = len(goal.freqs) -1
        music.publish_feedback(fb)

        if music.is_preempt_requested():
            write_freq(0)
            r.finish = False
            music.set_preempted(r)
            return

        write_freq(f)
        rospy.sleep(1.0 if i >= len(goal.durations) else goal.durations[i])

    r.finished = True
    music.set_succeeded(r)

if __name__ == '__main__':
    rospy.init_node('buzzer')
    rospy.Subscriber("buzzer", UInt16, recv_buzzer)
    music = actionlib.SimpleActionServer('music', MusicAction, exec_music, False)
    music.start()
    rospy.on_shutdown(write_freq)
    rospy.spin()


