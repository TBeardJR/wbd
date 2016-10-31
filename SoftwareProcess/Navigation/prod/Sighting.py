'''
Created on Oct 30, 2016

@author: tbeardjr
'''

class Sighting():
    def __init__(self, currentISODate, body, theDate, time, angleString):
        self.__currentISODate = currentISODate
        self.__body = body
        self.__theDate = theDate
        self.__time = time
        self.__angleString = angleString

    def get_current_isodate(self):
        return self.__currentISODate


    def get_body(self):
        return self.__body


    def get_the_date(self):
        return self.__theDate


    def get_time(self):
        return self.__time


    def get_angle_string(self):
        return self.__angleString