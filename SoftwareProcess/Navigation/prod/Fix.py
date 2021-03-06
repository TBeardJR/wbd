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
import Sighting as Sighting
from operator import itemgetter, attrgetter


class Fix():
    def __init__(self, logFile="logFile.txt"):
        self.logFile = logFile
        self.sightingFileName = None
        self.starFile = None
        self.ariesFile = None
        if(not(isinstance(logFile, basestring))):
            raise ValueError("Fix.__init__:  Invalid logFile name. logFile name must be a string.")
        if(len(logFile) < 2):
            raise ValueError("Fix.__init__:  Invalid logFile name. logFile name length must be greater than one character long.")
        matchObject = re.match(r'.*\.txt$', logFile)
        if(matchObject == None):
            raise ValueError("Fix.__init__:  Invalid logFile name. logFile name extension must be '.txt'")
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        myLogFile = open(logFile, "a+") # Open file for appending and reading
        myLogFile.write("LOG: " + currentISODate + "-06:00 Log File: " + Path.abspath(logFile) + "\n")
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
        
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        myLogFile = open(self.logFile, "a+") # Open file for appending and reading
        myLogFile.write("LOG: " + currentISODate + "-06:00 Sighting File: " + Path.abspath(sightingFile) + "\n")
        myLogFile.close()
        
        self.sightingFileName = sightingFile
        
    def setAriesFile(self, ariesFile):
        if(not(isinstance(ariesFile, basestring))):
            raise ValueError("Fix.setStarFile:  Invalid starFile name. starFile name must be a string.")
        dateMatchObject = re.match(r'.*\.txt', ariesFile)
        if(dateMatchObject == None):
            raise ValueError("Fix.setStarFile:  Invalid starFile name. starFile name must have the extension '.txt'.")
        if(len(ariesFile) < 6):
            raise ValueError("Fix.setStarFile:  Invalid starFile name. starFile name length must be greater than one.")
        
        with open(ariesFile) as f:
            for line in f:
                ariesDate, hour, angle = line.split()
                dateMatchObject = re.match(r'(\d\d)\/(\d\d)\/(\d\d)', str(ariesDate))
                if(dateMatchObject == None):
                    raise ValueError("Fix.setAriesFile:  Invalid date in ariesFile. Must be of the form mm/dd/yy.")
                month = int(dateMatchObject.group(1))
                if(month > 12 or month < 1):
                    raise ValueError("Fix.setAriesFile:  Invalid month in ariesFile. Month (mm) must be in the range 01-12.")
                day = int(dateMatchObject.group(2))
                if(day > 31 or day < 1):
                    raise ValueError("Fix.setAriesFile:  Invalid day in ariesFile. Day (dd) must be in the range 01-31.")
                
                hourMatchObject = re.match(r'\d\d?', str(hour))
                if(hourMatchObject == None):
                    raise ValueError("Fix.setAriesFile:  Invalid hour in ariesFile. Must be of the form hh.")
                hourValue = int(hourMatchObject.group(0))
                if(hourValue > 23):
                    raise ValueError("Fix.setAriesFile:  Hour too large in ariesFile. Must be in the range 0-23.")
                
                angleMatchObject = re.match(r'^([0-9]+)d([0-9]+(\.[0-9])?)$', str(angle))
                if(angleMatchObject == None):
                    raise ValueError("Fix.setAriesFile:  Incorrect format for angle in ariesFile. Must be of form xdy.y")
                x = int(angleMatchObject.group(1))
                if(x > 360):
                    raise ValueError("Fix.setAriesFile:  Invalid angle in ariesFile. x must be in the range 0-360.")
                y = float(angleMatchObject.group(2))
                if(y > 60.0):
                    raise ValueError("Fix.setAriesFile:  Invalid angle in ariesFile. y.y must be in the range 0.0-60.0")
        
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        myLogFile = open(self.logFile, "a+") # Open file for appending and reading
        myLogFile.write("LOG: " + currentISODate + "-06:00 Aries file: " + Path.abspath(ariesFile) + "\n")
        myLogFile.close()
        
        self.ariesFile = ariesFile
        
        return Path.abspath(ariesFile)
        
        
    def setStarFile(self, starFile):
        if(not(isinstance(starFile, basestring))):
            raise ValueError("Fix.setStarFile:  Invalid starFile name. starFile name must be a string.")
        dateMatchObject = re.match(r'.*\.txt', starFile)
        if(dateMatchObject == None):
            raise ValueError("Fix.setStarFile:  Invalid starFile name. starFile name must have the extension '.txt'.")
        if(len(starFile) < 6):
            raise ValueError("Fix.setStarFile:  Invalid starFile name. starFile name length must be greater than one.")
        
        with open(starFile) as f:
            for line in f:
                body, starDate, longitude, latitude = line.split()
                dateMatchObject = re.match(r'(\d\d)\/(\d\d)\/(\d\d)', str(starDate))
                if(dateMatchObject == None):
                    raise ValueError("Fix.setStarFile:  Invalid date in starFile. Must be of the form mm/dd/yy.")
                month = int(dateMatchObject.group(1))
                if(month > 12 or month < 1):
                    raise ValueError("Fix.setStarFile:  Invalid month in starFile. Month (mm) must be in the range 01-12.")
                day = int(dateMatchObject.group(2))
                if(day > 31 or day < 1):
                    raise ValueError("Fix.setStarFile:  Invalid day in starFile. Day (dd) must be in the range 01-31.")
                
                longitudeMatchObject = re.match(r'^([0-9]+)d([0-9]+(\.[0-9])?)$', str(longitude))
                if(longitudeMatchObject == None):
                    raise ValueError("Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form xdy.y")
                x = int(longitudeMatchObject.group(1))
                if(x > 360):
                    raise ValueError("Fix.setStarFile:  Invalid degree portion of longitude in starFile. x must be in the range 0-360.")
                y = float(longitudeMatchObject.group(2))
                if(y > 60.0):
                    raise ValueError("Fix.setStarFile:  Invalid minute portion of longitude in starFile. y.y must be in the range 0.0-60.0")
                
                latitudeMatchObject = re.match(r'^(-?[0-9]+)d([0-9]+(\.[0-9])?)$', str(latitude))
                if(latitudeMatchObject == None):
                    raise ValueError("Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form wdz.z")
                w = int(latitudeMatchObject.group(1))
                if(w > 90 or w < -90):
                    raise ValueError("Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form wdz.z")
                z = float(latitudeMatchObject.group(2))
                if(z > 60.0):
                    raise ValueError("Fix.setStarFile:  Invalid minute portion of latitude in starFile. z.z must be in the range 0.0-60.0")
                
        
        currentISODate = date.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%z")
        myLogFile = open(self.logFile, "a+") # Open file for appending and reading
        myLogFile.write("LOG: " + currentISODate + "-06:00 Star file: " + Path.abspath(starFile) + "\n")
        myLogFile.close()
        
        self.starFile = starFile
        
        return Path.abspath(starFile)
        
   
    def getSightings(self, assumedLatitude="0d0.0", assumedLongitude="0d0.0"):
        if(not(isinstance(assumedLatitude, basestring))):
            raise ValueError("Fix.getSightings:  Invalid assumeLatitude. Must be a string.")
        assumedLatitudeMatchObject = re.match(r'^([NS])?(-?[0-9]+)d([0-9]+(\.[0-9])?)$', assumedLatitude)
        if(assumedLatitudeMatchObject == None):
            raise ValueError("Fix.getSightings:  Invalid assumedLatitude form. Must be of form hxdy.y or (if h is missing) xdy.y.")
        h = "";
        xLatitudeValue = int(assumedLatitudeMatchObject.group(2))
        yLatitudeValue = float(assumedLatitudeMatchObject.group(3))
        if(assumedLatitudeMatchObject.group(1) == None):            
            if(xLatitudeValue != 0 or yLatitudeValue != 0.0):
                raise ValueError("Fix.getSightings:  Invalid assumedLatitude. Must be 0d0.0 if h is missing.")
        else:
            h = str(assumedLatitudeMatchObject.group(1))
        
        if(h != "" and h != "N" and h != "S"):
            raise ValueError("Fix.getSightings:  Invalid h. Must be 'N', 'S' or empty string")
        if(xLatitudeValue < 0 or xLatitudeValue >= 90):
            raise ValueError("Fix.getSightings:  Invalid x in assumedLatitude. Must be in range 0 <= x < 90")
        if(yLatitudeValue < 0.0 or yLatitudeValue >= 60.0):
            raise ValueError("Fix.getSightings:  Invalid y in assumedLatitude. Must be in range 0.0 <= y < 60.0")
        
        if(not(isinstance(assumedLongitude, basestring))):
            raise ValueError("Fix.getSightings:  Invalid assumedLongitude. Must be a string.")
        assumedLongitudeMatchObject = re.match(r'^(-?[0-9]+)d([0-9]+(\.[0-9])?)$', assumedLongitude)
        if(assumedLongitudeMatchObject == None):
            raise ValueError("Fix.getSightings:  Invalid assumedLongitude form. Must be of form xdy.y.")
        xLongitudeValue = int(assumedLongitudeMatchObject.group(1))
        yLongitudeValue = float(assumedLongitudeMatchObject.group(2))
        if(xLongitudeValue < 0 or xLongitudeValue >= 360):
            raise ValueError("Fix.getSightings:  Invalid x in assumedLongitude. Must be in range 0 <= x < 360")
        if(yLongitudeValue < 0.0 or yLongitudeValue >= 60.0):
            raise ValueError("Fix.getSightings:  Invalid y in assumedLongitude. Must be in range 0.0 <= y < 60.0")
          
        if(self.sightingFileName == None):
            raise ValueError("Fix.getSightings:  no sighting file has been set.")
        if(self.starFile == None):
            raise ValueError("Fix.getSightings:  Star file not set.")
        if(self.ariesFile == None):
            raise ValueError("Fix.getSightings:  Aries file not set.")
        doc = minidom.parse(self.sightingFileName)
        sightings = doc.getElementsByTagName("sighting")
        lengthOfSightings = len(sightings)
        sightingList = []
        
        validator = Validator.SightingsXMLValidator(lengthOfSightings)
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
        
        
        adjustedAltitude = 0.0
        
        for i in range(len(sightings)):
            if(validator.sightingErrors[i] == False):
                height, temperature, pressure, horizon, body, theDate, time, observation = self.__setSightingAttributes(sightings, i)
                                    
                adjustedAltitude = self.__calculateAdjustedAltitude(str(horizon), int(temperature), int(pressure), float(height), str(observation)) 
                angle = Angle.Angle()
                angle.setDegrees(adjustedAltitude)
                sighting = Sighting.Sighting(str(currentISODate), str(body), str(theDate), str(time), angle.getString())
                sightingList.append(sighting)
                
        sightingList = sorted(sightingList, key=attrgetter('_Sighting__theDate'))
        sum1 = 0
        sum2 = 0
                
        for sighting in sightingList:
            geographicPositionLatitude, geographicPositionLongitude = self.__calculateGeographicalPosition(self.starFile, sighting, self.ariesFile, validator)
            if(geographicPositionLatitude != "" and geographicPositionLongitude != ""):
                adjustedDistance = self.__calculateAdjustedDistance(geographicPositionLatitude, geographicPositionLongitude, assumedLatitude, assumedLongitude, adjustedAltitude)
                azimuthAdjustment = self.__calculateAzimuthAdjustment(geographicPositionLatitude, assumedLatitude, adjustedDistance)
                sum1 = sum1 + (adjustedDistance * math.cos(azimuthAdjustment))
                sum2 = sum2 + (adjustedDistance * math.sin(azimuthAdjustment))
                angle = Angle.Angle()
                angle.setDegrees(azimuthAdjustment)
                myLogFile = open(self.logFile, "a+") 
                myLogFile.write("LOG: " + str(sighting.get_current_isodate()) + "-06:00 " + str(sighting.get_body()) + " " + str(sighting.get_the_date()) + " " + str(sighting.get_time()) + " " + sighting.get_angle_string() + " " + 
                                str(geographicPositionLatitude) + " " + str(geographicPositionLongitude) + " " + assumedLatitude + " " + assumedLongitude + " " + angle.getString() + " " + str(adjustedDistance) + "\n")
                myLogFile.close()
        
        
        assumedLatitude = assumedLatitude[1:]
        angle = Angle.Angle()
        angle.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeNumerical = angle.getDegrees()
        angle1 = Angle.Angle()
        angle1.setDegreesAndMinutes(assumedLongitude)
        assumedLongitudeNumerical = angle1.getDegrees()
        
        approximateLatitude = assumedLatitudeNumerical + (sum1 / 60)
        approximateLongitude = assumedLongitudeNumerical + (sum2 / 60)
        approximateLongitudeAngle = Angle.Angle()
        approximateLongitudeAngle.setDegrees(approximateLongitude)
        approximateLatitudeAngle = Angle.Angle()
        approximateLatitudeAngle.setDegrees(approximateLatitude)
                
        
        myLogFile = open(self.logFile, "a+")  
        myLogFile.write("LOG: " + currentISODate + "-06:00 Sighting Errors:    " + str(validator.numberOfSightingErrors) + "\n") 
        myLogFile.write("LOG: " + currentISODate + "-06:00 Approximate latitude:    " + h + approximateLatitudeAngle.getString() + "    Approximate longitude:    " + approximateLongitudeAngle.getString() + "\n")  
        myLogFile.close()    
        
        return (approximateLatitude, approximateLongitude)
            
    def __calculateAdjustedDistance(self, geographicPositionLatitude, geographicPositionLongitude, assumedLatitude, assumedLongitude, adjustedAltitude):
        assumedLatitude = assumedLatitude[1:]
        assumedLatitudeAngle = Angle.Angle()
        assumedLatitudeAngle.setDegreesAndMinutes(assumedLatitude)
        
        assumedLatitudeNumerical = assumedLatitudeAngle.getDegrees()
        assumedLongitudeAngle = Angle.Angle()
        assumedLongitudeAngle.setDegreesAndMinutes(assumedLongitude)        
        assumedLongitudeNumerical = assumedLongitudeAngle.getDegrees()
        
        geographicPositionLongitudeAngle = Angle.Angle()
        geographicPositionLongitudeAngle.setDegreesAndMinutes(geographicPositionLongitude)        
        geographicPositionLongitudeNumerical = geographicPositionLongitudeAngle.getDegrees()
        
        geographicPositionLatitudeAngle = Angle.Angle()
        geographicPositionLatitudeAngle.setDegreesAndMinutes(geographicPositionLatitude)
        geographicPositionLatitdueNumerical = geographicPositionLatitudeAngle.getDegrees()
        
        LHA = geographicPositionLongitudeAngle.subtract(assumedLongitudeAngle)
        
        correctedAltitude = math.degrees(math.asin((math.sin(math.radians(geographicPositionLatitdueNumerical)) * math.sin(math.radians(assumedLatitudeNumerical)))
                                      + (math.cos(math.radians(geographicPositionLatitdueNumerical)) * math.cos(math.radians(assumedLatitudeNumerical)) * math.cos(math.radians(LHA)))))
        
        angle1 = Angle.Angle()
        angle1.setDegrees(adjustedAltitude)
        
        angle2 = Angle.Angle()
        angle2.setDegrees(correctedAltitude)
        
        
        adjustedDistance = angle1.subtract(angle2)
        return round(adjustedDistance, 2)
    
    def __calculateAzimuthAdjustment(self, geographicPositionLatitude, assumedLatitude, adjustedDistance):
        assumedLatitude = assumedLatitude[1:]
        angle = Angle.Angle()
        angle.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeNumerical = angle.getDegrees()
        angle2 = Angle.Angle()
        angle2.setDegreesAndMinutes(geographicPositionLatitude)
        geographicPositionLatitdueNumerical = angle2.getDegrees()
        azimuthAdjustment = math.acos((math.sin(math.radians(float(geographicPositionLatitdueNumerical))) - math.sin(math.radians(float(assumedLatitudeNumerical))) - math.sin(math.radians(float(adjustedDistance))))
                                      / math.cos(math.radians(float(assumedLatitudeNumerical))) * math.cos(math.radians(float(adjustedDistance))))
       
        return azimuthAdjustment
    
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
    
    def __calculateGeographicalPosition(self, starFileName, sighting, ariesFileName, validator):
        declination = ""
        sideHourAngle = Angle.Angle()
        greenwichHourAngle1 = ""
        greenwichHourAngle2 = ""
        hours, minutes, seconds = sighting.get_time().split(':')
        with open(starFileName, "r") as f:
            for line in f:
                body, starDate, longitude, latitude = line.split()                
                if(body == sighting.get_body()):
                    declination = latitude
                    sideHourAngle.setDegreesAndMinutes(longitude)
                    break
                    
        with open(ariesFileName, "r") as f:
            foundGreenwichHourAngle = False
            for line in f:
                the_date, hour, angle = line.split()
                dateArray1 = str(the_date).split('/')
                dateArray2 = sighting.get_the_date().split('-')
                temp = dateArray2[0]
                dateArray2[0] = dateArray2[2]
                dateArray2[2] = temp[2:]
                temp2 = dateArray2[0]
                dateArray2[0] = dateArray2[1]
                dateArray2[1] = temp2
                dateObj1 = date.date(int(dateArray1[2]), int(dateArray1[0]), int(dateArray1[1]))
                dateObj2 = date.date(int(dateArray2[2]), int(dateArray2[0]), int(dateArray2[1]))
                
                if(foundGreenwichHourAngle == True):
                    greenwichHourAngle2 = angle
                    break                
                if(dateObj1 == dateObj2 and int(hours) == int(hour)):
                    greenwichHourAngle1 = angle
                    foundGreenwichHourAngle = True
        if(foundGreenwichHourAngle == True and declination != ""):
            
            s = (int(minutes) * 60) + int(seconds)
            angle1 = Angle.Angle()
            angle2 = Angle.Angle()
            angle1.setDegreesAndMinutes(greenwichHourAngle1)
            angle2.setDegreesAndMinutes(greenwichHourAngle2)
            degrees = abs(angle2.subtract(angle1))
            angle3 = Angle.Angle()
            angle3.setDegrees(degrees * (float(s)/3600))
            degrees2 = angle3.add(angle1)
            greenwichHourAngle = Angle.Angle()
            greenwichHourAngle.setDegrees(degrees2)
            
            degreesLongitude = greenwichHourAngle.add(sideHourAngle)
            greenwichHourAngleObservation = Angle.Angle()
            greenwichHourAngleObservation.setDegrees(degreesLongitude)
            return (declination, greenwichHourAngleObservation.getString())
            
        else:
            validator.numberOfSightingErrors+=1
            
        return ("", "")
            
            
    def __setSightingAttributes(self, sightings, index):
        height = 0
        temperature = 0
        pressure = 0 
        horizon = ""
        body = sightings[index].getElementsByTagName("body")[0].childNodes[0].data
        theDate = sightings[index].getElementsByTagName("date")[0].childNodes[0].data
        time = sightings[index].getElementsByTagName("time")[0].childNodes[0].data
        observation = sightings[index].getElementsByTagName("observation")[0].childNodes[0].data
        
        heightElements = sightings[index].getElementsByTagName("height")
        if(len(heightElements) == 0):
            height = 0.0
        else:
            height = heightElements[0].childNodes[0].data
            
        temperatureElements = sightings[index].getElementsByTagName("temperature")
        if(len(temperatureElements) == 0):
            temperature = 72
        else:
            temperature = temperatureElements[0].childNodes[0].data
            
        pressureElements = sightings[index].getElementsByTagName("pressure")
        if(len(pressureElements) == 0):
            pressure = 1010 
        else:
            pressure = pressureElements[0].childNodes[0].data 
                   
        horizonElements = sightings[index].getElementsByTagName("horizon")
        if(len(horizonElements) == 0):
            horizon = "Natural"
        else:
            horizon = horizonElements[0].childNodes[0].data
            
        return (height, temperature, pressure, horizon, body, theDate, time, observation)
    
                
     
    
                

    
    
        