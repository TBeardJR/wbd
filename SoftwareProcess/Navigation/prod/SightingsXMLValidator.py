'''
Created on Oct 16, 2016

@author: tbeardjr
'''

import re

class SightingsXMLValidator():
    def __init__(self, lengthOfSightings):
        self.invalid = False
        self.sightingErrors = [False]*lengthOfSightings
        self.numberOfSightingErrors = 0
        
    def getElements(self, sightings, attributeName):
        values = []
        for sighting in sightings:
            if(len(sighting.getElementsByTagName(attributeName)) == 0):
                continue
            valueObj = sighting.getElementsByTagName(attributeName)[0]
            values.append(valueObj)
        
        return values
    
    def validateElements(self, elements, validatorFunction):
        counter = 0;
        for element in elements:
            nodes = element.childNodes
            if(self.sightingErrors[counter] == False):
                for node in nodes:
                    if node.nodeType == node.TEXT_NODE:
                        validatorFunction(str(node.data))
                        if(self.invalid == True):
                            self.sightingErrors[counter] = self.invalid
                            self.invalid = False    
                            self.numberOfSightingErrors+=1                    
                            break
            counter+=1
    
    def validateDate(self, date):
        matchObject = re.match(r'^\d{4}-\d{2}-\d{2}$', date)  
        if(matchObject == None):
            self.invalid = True   
        
    def validateTime(self, time):
        matchObject = re.match(r'^\d{2}:\d{2}:\d{2}$', time)  
        if(matchObject == None):
            self.invalid = True  
        
    def validateObservation(self, oberservation):
        matchObject = re.match(r'^(\d+)d(\d+\.\d+)$', oberservation)  
        if(matchObject == None):
            self.invalid = True
        x = int(matchObject.group(1))
        y = float(matchObject.group(2))
        if(x < 0 or x > 89):
            self.invalid = True  
        if(y < 0.0 or y >= 60.0):
            self.invalid = True  
        
    def validateHeight(self, height):
        height = float(height)
        if(height < 0.0):
            self.invalid = True  
        return height
    
    def validateTemperature(self, temperature):
        temperature = int(temperature)
        if(temperature < -20 or temperature > 120):
            self.invalid = True  
        return temperature
    
    def validatePressure(self, pressure):
        pressure = int(pressure)
        if(pressure < 100 or pressure > 1100):
            raise ValueError("Fix.getSightings: Invalid pressure. Must be greater than or equal to 100 and less than or equal to 1100")
        return pressure
    
    
                     