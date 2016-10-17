"""
    Created on Sept 10, 2016

    @author: Tarence Beard Jr.
"""
import re

class Angle():
    def __init__(self):
        self.degrees = 0
    
    def setDegrees(self, degrees=0):
        if(not(isinstance(degrees, int)) and not(isinstance(degrees, float))):
            raise ValueError("Angle.setDegrees:  degrees must be of type int or a float.")
        self.degrees = round(degrees, 9) % float(360)
        return self.degrees    
    
    def setDegreesAndMinutes(self, angleString):
        if(not(isinstance(angleString, basestring))):
            raise ValueError("Angle.setDegreesAndMinutes:  angleString must be of type string")
        
        angleStringMatchObject = re.match(r'^(-?[0-9]+)d([0-9]+(\.[0-9])?)$', angleString)
        if(angleStringMatchObject == None):
            raise ValueError("Angle.setDegreesAndMinutes:  angleString does not fit the required format")
        
        self.degrees = int(angleStringMatchObject.group(1)) % 360
        self.degrees = float(self.degrees)
        try:
            minutes = int(angleStringMatchObject.group(2))
        except:
            minutes = float(angleStringMatchObject.group(2))
            
        self.degrees+= float(float(minutes) / 60)
        
        return round(self.degrees, 9)
        
    
    def add(self, angle=None):
        if(angle == None):
            raise ValueError("Angle.add:  angle is null")
        if(not(isinstance(angle, Angle))):
            raise ValueError("Angle.add:  angle is not of type Angle")
        self.degrees+= angle.getDegrees() 
        self.degrees%= 360
        return self.degrees
    
    def subtract(self, angle=None):
        if(angle == None):
            raise ValueError("Angle.subtract:  angle is null")
        if(not(isinstance(angle, Angle))):
            raise ValueError("Angle.subtract:  angle is not of type Angle")
        self.degrees-= angle.getDegrees() 
        self.degrees%= 360
        return self.degrees
    
    def compare(self, angle=None):
        if(angle == None):
            raise ValueError("Angle.compare:  angle is null")
        if(not(isinstance(angle, Angle))):
            raise ValueError("Angle.compare:  angle is not of type Angle")
        if(self.getDegrees() > angle.getDegrees()):
            return 1
        elif(self.getDegrees() < angle.getDegrees()):
            return -1
        else:
            return 0
    
    def getString(self):
        minutes = (float(self.degrees - int(self.degrees))) * 60
        return str(int(self.degrees)) + "d" + str(round(minutes, 1))
    
    def getDegrees(self):
        return round(self.degrees, 9)