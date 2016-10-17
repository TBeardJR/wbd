'''
Created on Oct 16, 2016

@author: tbeardjr
'''

import re

class SightingsXMLValidator():
    def __init__(self):
        '''
        Constructor
        '''
    def getElements(self, sightings, attributeName):
        values = []
        for sighting in sightings:
            if(len(sighting.getElementsByTagName(attributeName)) == 0):
                continue
            valueObj = sighting.getElementsByTagName(attributeName)[0]
            values.append(valueObj)
        
        return values
    
    def validateElements(self, elements, validatorFunction):
        for element in elements:
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    validatorFunction(str(node.data))
    
    def validateDate(self, date):
        matchObject = re.match(r'^\d{4}-\d{2}-\d{2}$', date)  
        if(matchObject == None):
            raise ValueError("Fix.getSightings:  Invalid date. Must be of format yyyy-mm-dd.")   
        
    def validateTime(self, time):
        matchObject = re.match(r'^\d{2}:\d{2}:\d{2}$', time)  
        if(matchObject == None):
            raise ValueError("Fix.getSightings: Invalid time Must be of format hh:mm:ss.")  
        
    def validateObservation(self, oberservation):
        matchObject = re.match(r'^(\d+)d(\d+\.\d+)$', oberservation)  
        if(matchObject == None):
            raise ValueError("Fix.getSightings: Invalid Observation string. Must be of form xdy.y")
        x = int(matchObject.group(1))
        y = float(matchObject.group(2))
        if(x < 0 or x > 89):
            raise ValueError("Fix.getSightings: Invalid Observation string. x must be greater than or equal to 0 and less than 90")  
        if(y < 0.0 or y >= 60.0):
            raise ValueError("Fix.getSightings: Invalid Observation string. x must be greater than or equal to 0.0 and less than 60.0")   
        
    def validateHeight(self, height):
        height = float(height)
        if(height < 0.0):
            raise ValueError("Fix.getSightings: Invalid height. Must be greater than 0")
        return height
    
    def validateTemperature(self, temperature):
        temperature = int(temperature)
        if(temperature < -20 or temperature > 120):
            raise ValueError("Fix.getSightings: Invalid temperature. Must be greater than or equal to -20 and less than or equal to 120")
        return temperature
    
    def validatePressure(self, pressure):
        pressure = int(pressure)
        if(pressure < 100 or pressure > 1100):
            raise ValueError("Fix.getSightings: Invalid pressure. Must be greater than or equal to 100 and less than or equal to 1100")
        return pressure
    
    
                     