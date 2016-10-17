'''
Created on Oct 11, 2016

@author: tbeardjr
'''

import datetime as date
import re
import os.path as Path
from xml.dom import minidom
import Navigation.prod.SightingsXMLValidator as Validator
import math
import Angle as Angle


class Fix():
    def __init__(self, logFile="logFile.txt"):
        self.logFile = logFile
        self.sightingFileName = None
        if(not(isinstance(logFile, basestring))):
            raise ValueError("Fix.__init__:  Invalid logFile name. logFile name must be a string.")
        if(len(logFile) < 2):
            raise ValueError("Fix.__init__:  Invalid logFile name. logFile name length must be greater than one character long.")
        matchObject = re.match(r'.*\.txt$', logFile)
        if(matchObject == None):
            raise ValueError("Fix.__init__:  Invalid logFile name. logFile name extension must be '.txt'")
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        myLogFile = open(logFile, "a+") # Open file for appending and reading
        myLogFile.write("LOG: " + currentISODate + "-06:00 Start of Log\n")
        myLogFile.close()
        
    def setSightingFile(self, sightingFile):        
        if(not(isinstance(sightingFile, basestring))):
            raise ValueError("Fix.setSightingFile:  Invalid sightingFile name. sightingFile name must be a string.")
        if(len(sightingFile) < 2):
            raise ValueError("Fix.setSightingFile: Invalid filepath. Does not exist.")
        matchObject = re.match(r'.*\.xml', sightingFile)
        if(matchObject == None):
            raise ValueError("Fix.setSightingFile: Invalid sightingFile name. Must be of form 'f.xml'.")
        if(not(Path.exists(sightingFile))):
            raise ValueError("Fix.setSightingFile: Invalid filepath. Does not exist.")
        self.sightingFileName = sightingFile
        
    def getSightingFile(self):
        if(self.sightingFileName == None):
            raise ValueError("Fix.getSightingFile:  no sighting file has been set.")
        doc = minidom.parse(self.sightingFileName)
        sightings = doc.getElementsByTagName("sighting")
        lengthOfSightings = len(sightings)
        
        validator = Validator.SightingsXMLValidator()
        heights = validator.getElements(sightings, "height")
        temperatures = validator.getElements(sightings, "temperature")
        pressures = validator.getElements(sightings, "pressure")
        horizons = validator.getElements(sightings, "horizon")
        dates = validator.getElements(sightings, "date")
        times = validator.getElements(sightings, "time")
        observations = validator.getElements(sightings, "observation")
        bodies = validator.getElements(sightings, "body")
        
        if(len(dates) != lengthOfSightings or len(times) != lengthOfSightings 
           or len(observations) != lengthOfSightings or len(bodies) != lengthOfSightings):
            raise ValueError("Fix.getSightings: Invalid sighting file. The date, time, observation and body tags must be present.")
        
        validator.validateElements(dates, validator.validateDate)
        validator.validateElements(times, validator.validateTime)
        validator.validateElements(observations, validator.validateObservation)
        validator.validateElements(heights, validator.validateHeight)
        validator.validateElements(temperatures, validator.validateTemperature)
        validator.validateElements(pressures, validator.validatePressure)
        
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        myLogFile = open(self.logFile, "a+") # Open file for appending and reading
        myLogFile.write("LOG: " + currentISODate + "-06:00 Start of sighting file: " + self.sightingFileName + "\n")
        
        
        for i in range(len(sightings)):
            height = 0
            temperature = 0
            pressure = 0 
            horizon = ""
            body = sightings[i].getElementsByTagName("body")[0].childNodes[0].data
            theDate = sightings[i].getElementsByTagName("date")[0].childNodes[0].data
            time = sightings[i].getElementsByTagName("time")[0].childNodes[0].data
            observation = sightings[i].getElementsByTagName("observation")[0].childNodes[0].data
            
            heightElements = sightings[i].getElementsByTagName("height")
            if(len(heightElements) == 0):
                height = 0.0
            else:
                height = heightElements[0].childNodes[0].data
                
            temperatureElements = sightings[i].getElementsByTagName("temperature")
            if(len(temperatureElements) == 0):
                temperature = 72
            else:
                temperature = temperatureElements[0].childNodes[0].data
                
            pressureElements = sightings[i].getElementsByTagName("pressure")
            if(len(pressureElements) == 0):
                pressure = 1010 
            else:
                pressure = pressureElements[0].childNodes[0].data 
                       
            horizonElements = sightings[i].getElementsByTagName("horizon")
            if(len(horizonElements) == 0):
                horizon = "Natural"
            else:
                horizon = horizonElements[0].childNodes[0].data
                
            adjustedAltitude = self.__calculateAdjustedAltitude(str(horizon), int(temperature), int(pressure), float(height), str(observation)) 
            angle = Angle.Angle()
            angle.setDegrees(adjustedAltitude)
            myLogFile.write("LOG: " + str(currentISODate) + "-06:00 " + str(body) + " " + str(theDate) + " " + str(time) + " " + angle.getString() + "\n")
        
        myLogFile.write("LOG: " + currentISODate + "-06:00 End of sighting file: " + self.sightingFileName + "\n")    
        myLogFile.close()    
            
    def __calculateAdjustedAltitude(self, horizon, temperature, pressure, height, observedAltitude):
        angle = Angle.Angle()
        angle.setDegreesAndMinutes(observedAltitude)
        if(horizon == "Natural"):
            dip = (-0.97 * math.sqrt(height)) / 60
        else:
            dip = 0
        celsiusTemperature = (temperature - 32) / 1.8
        refraction =  (-0.00452 * pressure) / (273 + celsiusTemperature) / math.tan(math.radians(angle.getDegrees()))
        adjustedAltitude = float(angle.getDegrees()) + float(dip) + float(refraction)
        return round(adjustedAltitude, 2)
                    
        
        
        
            