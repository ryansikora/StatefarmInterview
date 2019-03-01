#This program reads a file of Zebra Movements and graphs the distance traveled
#It also makes a bar graph of all zebra's daily average distance traveled

from math import *
import pylab
import random

#The distance formula used to find the distance between 2 latitude and longitude points
def distance(long1, lat1, long2, lat2):
    l1 = radians (float(long1))
    l2 = radians (float(long2))
    p1 = radians(float(lat1))
    p2 = radians(float(lat2))
    dp = p2-p1
    dl = l2-l1
    a = sin(dp/2)**2 + cos(p1) * cos(p2) * sin(dl/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    d = 6371*c
    return d

#calculates the amount of days between 2 time periods in seconds
#Used when finding the average distance traveled per day
#Unix timestamps record time in seconds since Janurary 1st, 1970    
def days(t1,t2):    
    totsec = t2-t1  
    day = totsec/86400
    return day 

#Setting up dictionaries and lists for analysis   
zebra = {}    #dictionary that links zebras to timestamps, longitude, latitude  
distances = []  #list of avg daily distances, used for bar graph
colorline = {}  #dictionary used to store a zebra's color for the line graph
colorbar = []   #list used to store a zebra's color for the bar graph

#reads the ZebraBotswana.txt file and makes dictionary entries for each unique zebra
intext = open('ZebraBotswana.txt','r') 
for line in intext:     #grabs the uniqie zebra names from .txt file
    word = line.split(',')
    for i in word:
        if word[3][0:5] not in zebra.keys():
            zebra[word[3][0:5]] = []

#reads the ZebraBotswana.txt file and inserts each zebras recorded timestamp, longitude, and latitude into dictionary
intext = open('ZebraBotswana.txt','r')
for line in intext: #inserts timestamp, longitude, and latitude into dictionary
    itext = line[:-1]
    ittext = itext.split(',')
    w,x,y,z = float(ittext[0]),ittext[1],ittext[2],ittext[3]
    zebra[z].append((w,x,y))
intext.close()

#assigns a random RGB color to each zebra to be used in the line and bar graph
for z in zebra.keys():
    newColor=(random.random(),random.random(),random.random())
    colorline[z] = newColor
    colorbar.append(newColor)
    
#calculates each zebra's average daily distance traveled
for z in zebra:
    dist = 0
    zeblen = len(zebra[z])
    for i in range(zeblen-1):
        d = distance(zebra[z][i][1],zebra[z][i][2],zebra[z][i+1][1],zebra[z][i+1][2])
        dist = dist + d
    avgdist = dist/days(float(zebra[z][0][0]),zebra[z][-1][0])
    distances.append(avgdist)

#setting up the line graph 
pylab.figure(1) 
for z in zebra:
    longitude = []
    latitude = []
    for i in zebra[z]:
        longitude.append(i[1]) 
        latitude.append(i[2])
    pylab.plot(longitude,latitude, color = colorline[z], label= z)

pylab.xlabel("Latitude")
pylab.ylabel("Longitude")
pylab.title("Zebras' Movement")
pylab.legend(loc="best")
pylab.show()

#setting up the bar graph
pylab.figure(2)
q=pylab.arange(len(distances))
pylab.bar(q,distances,0.6,color=colorbar)
pylab.xticks(q,zebra.keys())
pylab.xlabel("Zebra Number")
pylab.ylabel("Average km per day")
pylab.title("Zebras' Travelling per Day")
pylab.show() 





    




    