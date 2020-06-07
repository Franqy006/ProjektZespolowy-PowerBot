#!/usr/bin/env python

import rospy
import time
import numpy as np

#Pobieranie typow wiadomosci z ROSa
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionResult

#Mozna przeksztalcic na flage, ktora zmienia inny robot
flag = 0

pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
pub1 = rospy.Publisher('move_base/result', MoveBaseActionResult, queue_size=10)

#Zmienne do przechowywania punktow zadawanych przez uzytkownika
#Osadzamy w nich punkty z 1 i z 2 sali
point_1x = -2.02
point_1y = -0.03
point_2x = 11.03
point_2y = 22.37
orient_1w = 0
orient_2w = 0


def callback(data):
    global flag, point_1x, point_1y, point_2x, point_2y, orient_1w, orient_2w

    #Wyswietlanie odpowiedniej informacji dla uzytkownika
    if(data.status.text == "Goal reached."):
        print("Cel osiagniety. Wybierz ponownie")
    elif(data.status.text == ""):
        print("Start Programu")
    else:
        print("Cel anulowany. Sprobuj jeszcze raz")

    #Zapewnienie, ze uzytkownik wybral dobra opcje
    while(flag!=1 and flag!=2):
        print("Wybierz sale, do ktorej chcesz jechac")
        print("Sala Pierwsza - Wybierz 1")
        print("Sala Druga - Wybierz 2")
        flag = input()
        print("")
        #orient_1w = input("Wspolrzedna orientacji:")

    #Wlasciwe publikowanie wiadomosci, w ktorej sa punkty z odpowiedniej sali
    if (flag==1):
        twist = PoseStamped()
        twist.header.frame_id = "map"
        twist.pose.position.x = point_1x
        twist.pose.position.y = point_1y
        twist.pose.orientation.z = 1
        twist.pose.orientation.w = 0.3 #orient_1w #Mozliwe zadawanie orientacji
        pub.publish(twist)
        flag=0
    elif (flag==2):
        twist = PoseStamped()
        twist.header.frame_id = "map"
        twist.pose.position.x = point_2x
        twist.pose.position.y = point_2y
        twist.pose.orientation.z = 1
        twist.pose.orientation.w = 0.3 #orient_2w   #Mozliwe zadawanie orientacji
        pub.publish(twist)
        flag=0
    

#Funkcja ktora subskrybuje i wysyla zawiadomienie do funkcji callback
def listener():
    global point_1x, point_1y, point_2x, point_2y, orient_1w, orient_2w
    
    rospy.Subscriber("move_base/result", MoveBaseActionResult, callback)
    rospy.spin()

    
if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True)
        data = MoveBaseActionResult()
        callback(data)  # Zapewnia uruchomienie sie petli i wyboru sal od razu

        listener()

            
    except rospy.ROSInterruptException:
        pass
    
        
