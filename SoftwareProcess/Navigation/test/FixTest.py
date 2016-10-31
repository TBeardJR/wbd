'''
Created on Oct 11, 2016

@author: tbeardjr
'''
import unittest
import Navigation.prod.Fix as Fix
import os as OS
import os.path as Path


class FixTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        if(Path.exists("logFile.txt")):
            OS.remove("logFile.txt")
            
        if(Path.exists("testFile.txt")):
            OS.remove("testFile.txt")
            
        if(Path.exists("file.xml")):
            OS.remove("file.xml")
            
        if(Path.exists("sighting.xml")):
            OS.remove("sighting.xml")

        if(Path.exists("star.txt")):
            OS.remove("star.txt")
            
        if(Path.exists("ariesTest.txt")):
            OS.remove("ariesTest.txt")

    def testConstructor_InstantiateFix_ShouldBeInstantiated(self):
        logFileName = "testFile.txt"
        self.assertIsInstance(Fix.Fix(logFileName), Fix.Fix)
    
    def testConstructor_InstantiateFixWithNonExistentFile_ShouldCreateFile(self):
        logFileName = "testFile.txt"
        if(Path.exists(logFileName)):
            OS.remove(logFileName)
        Fix.Fix(logFileName)
        self.assertTrue(Path.exists(logFileName))
        
    def testConstructor_InstantiateFixWithExistingFile_ShouldOpenFile(self):
        logFileName = "testFile.txt"
        if(not(Path.exists(logFileName))):
            logFile = open(logFileName, "w") 
            logFile.close()
        Fix.Fix(logFileName)
        self.assertTrue(Path.exists(logFileName))
        
    def testConstructor_InstantiateFixWithNoFileNameSpecified_ShouldCreateFile(self):
        if(Path.exists("logFile.txt")):
            OS.remove("logFile.txt")
        Fix.Fix()
        self.assertTrue(Path.exists("logFile.txt"))
        
    def testConstructor_InstantiateFixWithShortName_ShouldThrowValueError(self):
        logFileName = "l"
        expectedDiag = "Fix.__init__:  Invalid logFile name. logFile name length must be greater than one character long."
        with self.assertRaises(ValueError) as context:
            Fix.Fix(logFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testConstructor_InstantiateFix_ShouldAppendToStartOfLogFileCorrectly(self):
        logFileName = "testFile.txt" 
        if(Path.exists(logFileName)):
            OS.remove(logFileName)
        Fix.Fix(logFileName)
        logFile = open(logFileName, "r")
        firstLine = logFile.readline().rstrip()
        self.assertRegexpMatches(firstLine, r'testFile.txt$')
        
    def testConstructor_InstantiateFixWithNonStringForFileName_ShouldThrowValueError(self):
        logFileName = 43
        expectedDiag = "Fix.__init__:  Invalid logFile name. logFile name must be a string."
        with self.assertRaises(ValueError) as context:
            Fix.Fix(logFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testConstructor_InstantiateFixWithWrongExtensionForFileName_ShouldThrowValueError(self):
        logFileName = "program.py"
        expectedDiag = "Fix.__init__:  Invalid logFile name. logFile name extension must be '.txt'"
        with self.assertRaises(ValueError) as context:
            Fix.Fix(logFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testConstructor_InitializeSightingFile_ShouldBeInitialized(self):
        logFileName = "testFile.txt"
        fix = Fix.Fix(logFileName)
        self.assertIsNone(fix.sightingFileName)
        
    def testSetSightingFile_InvalidFileFormat_ShouldThrowValueError(self):
        sightingFileName = "filexmd"
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setSightingFile: Invalid sightingFile name. Must be of form 'f.xml'."
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile(sightingFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testSetSightingFile_CorrectFileFormat_ShouldSetSightingFile(self):
        sightingFileName = "file.xml"
        logFileName = "testFile.txt"
        if(not(Path.exists(sightingFileName))):
            sightingFile = open(sightingFileName, "w") 
            sightingFile.close()
        fix = Fix.Fix(logFileName)        
        fix.setSightingFile(sightingFileName)
        self.assertEqual(fix.sightingFileName, sightingFileName)
        
    def testSetSightingFile_InvalidFilePath_ShouldThrowValueError(self):
        sightingFileName = "sighting.xml"
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setSightingFile: Invalid filepath. Does not exist."
        if(Path.exists(sightingFileName)):
            OS.remove(sightingFileName)
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile(sightingFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetSightingFile_ShortFileName_ShouldThrowValueError(self):
        sightingFileName = "f"
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setSightingFile: Invalid filepath. Does not exist."
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile(sightingFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testSetSightingFile_FileNameIsANumber_ShouldThrowValueError(self):
        sightingFileName = 3
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setSightingFile:  Invalid sightingFile name. sightingFile name must be a string."
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile(sightingFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testSetSightingFile_ValidFileName_ShouldAppendToLogFileCorrectly(self):
        sightingFileName = "file.xml"
        logFileName = "testFile.txt"
        if(Path.exists(logFileName)):
            OS.remove(logFileName)
        if(not(Path.exists(sightingFileName))):
            sightingFile = open(sightingFileName, "w") 
            sightingFile.close()
        fix = Fix.Fix(logFileName)        
        fix.setSightingFile(sightingFileName)
        logFile = open(logFileName, "r")
        logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        self.assertRegexpMatches(secondLine, r'file.xml$')
        
        
        
        
        
        
    def testSetStarFile_FileNameIsANumber_ShouldThrowValueError(self):
        starFileName = 3
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setStarFile:  Invalid starFile name. starFile name must be a string."
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def testSetStarFile_InvalidFileExtension_ShouldThrowValueError(self):
        starFileName = "star.py"
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setStarFile:  Invalid starFile name. starFile name must have the extension '.txt'."
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])    
        
    def testSetStarFile_FileNameToShort_ShouldThrowValueError(self):
        starFileName = "f.txt"
        logFileName = "testFile.txt"
        expectedDiag = "Fix.setStarFile:  Invalid starFile name. starFile name length must be greater than one."
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])   
        
    def testSetStarFile_SetStarFile_ShouldAppendToLogFileCorrectly(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(logFileName)):
            OS.remove(logFileName)
        if(not(Path.exists(starFileName))):
            starFile = open(starFileName, "w") 
            starFile.close()
        fix = Fix.Fix(logFileName)
        fix.setStarFile(starFileName)
        logFile = open(logFileName, "r")
        logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        self.assertRegexpMatches(secondLine, r'star.txt$')
        
    def testSetStarFile_InvalidMonthFormat_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid date in starFile. Must be of the form mm/dd/yy."
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    1lol    281d10.1    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def testSetStarFile_MonthTooLarge_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid month in starFile. Month (mm) must be in the range 01-12."
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    14/01/17    281d10.1    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testSetStarFile_MonthTooSmall_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid month in starFile. Month (mm) must be in the range 01-12."
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    00/01/17    281d10.1    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testSetStarFile_DayTooLarge_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid day in starFile. Day (dd) must be in the range 01-31."
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/32/17    281d10.1    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])    
        
    def testSetStarFile_DayTooSmall_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid day in starFile. Day (dd) must be in the range 01-31."
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/00/17    281d10.1    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetStarFile_IncorrectLongitudeFormat_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form xdy.y"
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    fail    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])    
        
    def testSetStarFile_LongitudeXTooLarge_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid degree portion of longitude in starFile. x must be in the range 0-360."
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    361d31.7    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
      
    def testSetStarFile_LongitudeYTooLarge_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid minute portion of longitude in starFile. y.y must be in the range 0.0-60.0"
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.4    -8d11.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        
    def testSetStarFile_InvalidLatitudeFormat_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form wdz.z"
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    fail\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetStarFile_LatitudeWIsTooLarge_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form wdz.z"
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    91d44.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetStarFile_LatitudeWIsTooSmall_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Incorrect format for degree portion of longitude in starFile. Must be of form wdz.z"
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -91d44.3\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetStarFile_LatitudeZIsTooLarge_ShouldThrowValueError(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        expectedDiag = "Fix.setStarFile:  Invalid minute portion of latitude in starFile. z.z must be in the range 0.0-60.0"
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.4\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setStarFile(starFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetStarFile_StarFileisValid_ShouldReturnAbsolutePathOfStarFile(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.0\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        absoluteFilePath = fix.setStarFile(starFileName)
        self.assertRegexpMatches(absoluteFilePath, r'star.txt$')
        
    def testSetStarFile_StarFileisValid_ShouldSetStarFile(self):
        starFileName = "star.txt"
        logFileName = "testFile.txt"
        if(Path.exists(starFileName)):
            OS.remove(starFileName)
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.0\n")
        starFile.close()
        fix = Fix.Fix(logFileName)
        fix.setStarFile(starFileName)
        self.assertEquals(fix.starFile, "star.txt")
        
        
        
        
        
        
    def testSetAriesFile_IncorrectFormatForHour_ShouldThrowValueError(self):
        ariesFileName = "ariesTest.txt"
        logFileName = "testFile.txt"
        if(Path.exists(ariesFileName)):
            OS.remove(ariesFileName)
        expectedDiag = "Fix.setAriesFile:  Invalid hour in ariesFile. Must be of the form hh."
        ariesFile = open(ariesFileName, "a+") 
        ariesFile.write("04/11/17    19    125d25.2\n")
        ariesFile.write("04/11/17    fail    140d27.7\n")
        ariesFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setAriesFile(ariesFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testSetAriesFile_HourTooLarge_ShouldThrowValueError(self):
        ariesFileName = "ariesTest.txt"
        logFileName = "testFile.txt"
        if(Path.exists(ariesFileName)):
            OS.remove(ariesFileName)
        expectedDiag = "Fix.setAriesFile:  Hour too large in ariesFile. Must be in the range 0-23."
        ariesFile = open(ariesFileName, "a+") 
        ariesFile.write("04/11/17    19    125d25.2\n")
        ariesFile.write("04/11/17    24    140d27.7\n")
        ariesFile.close()
        fix = Fix.Fix(logFileName)
        with self.assertRaises(ValueError) as context:
            fix.setAriesFile(ariesFileName)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
            
          
        
        
    def testGetSightingFile_SightingFileNotSet_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        fix = Fix.Fix(logFileName)        
        expectedDiag =  "Fix.getSightingFile:  no sighting file has been set."
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testGetSightingFile_StarFileNotSet_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        fix = Fix.Fix(logFileName)        
        expectedDiag =  "Fix.getSightings:  Star file not set."
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()     
        fix.setSightingFile(sightingFileName)
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testGetSightingFile_AriesFileNotSet_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        starFileName = "star.txt"
        sightingFileName = "sighting.xml"
        fix = Fix.Fix(logFileName)        
        expectedDiag =  "Fix.getSightings:  Aries file not set."
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()     
        fix.setSightingFile(sightingFileName)
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.0\n")
        starFile.close()
        fix.setStarFile(starFileName)        
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testGetSightingFile_MissingMandatoryTags_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        starFileName = "star.txt"
        ariesFileName = "ariesTest.txt"
        expectedDiag =  "Fix.getSightings: Invalid sighting file. The date, time, observation and body tags must be present."
        fix = Fix.Fix(logFileName)  
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()     
        fix.setSightingFile(sightingFileName)
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.0\n")
        starFile.close()
        fix.setStarFile(starFileName)
        ariesFile = open(ariesFileName, "a+") 
        ariesFile.write("04/11/17    19    125d25.2\n")
        ariesFile.write("04/11/17    23    140d27.7\n")
        ariesFile.close()
        fix.setAriesFile(ariesFileName)
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    
        
    
    
        
    def testGetSightingFile_WriteToLogFile_ShouldWriteToLogFile(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        starFileName = "star.txt"
        ariesFileName = "ariesTest.txt"
        fix = Fix.Fix(logFileName)    
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-03-01</date>")
        sightingFile.write("<time>23:40:01</time>")
        sightingFile.write("<observation>015d04.9</observation>")
        sightingFile.write("<body>Aldebaran</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>72</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Artificial</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-03-02</date>")
        sightingFile.write("<time>00:05:05</time>")
        sightingFile.write("<observation>045d15.2</observation>")
        sightingFile.write("<body>Peacock</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>71</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Natural</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()       
        fix.setSightingFile(sightingFileName)
        
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.0\n")
        starFile.close()
        fix.setStarFile(starFileName)
        ariesFile = open(ariesFileName, "a+") 
        ariesFile.write("04/11/17    19    125d25.2\n")
        ariesFile.write("04/11/17    23    140d27.7\n")
        ariesFile.close()
        fix.setAriesFile(ariesFileName)
        
        fix.getSightingFile()
        logFile = open(logFileName, "r")
        firstLine = logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        thirdLine = logFile.readline().rstrip()
        fourthLine = logFile.readline().rstrip()
        fifthLine = logFile.readline().rstrip()
        sixthLine = logFile.readline().rstrip()
        self.assertRegexpMatches(firstLine, r'logFile.txt$')
        self.assertRegexpMatches(secondLine, r'sighting.xml$')
        self.assertRegexpMatches(thirdLine, r'star.txt$')
        self.assertRegexpMatches(fourthLine, r'ariesTest.txt$')
        self.assertRegexpMatches(fifthLine, r'Start of sighting file: sighting.xml$')
        self.assertRegexpMatches(sixthLine, r'End of sighting file: sighting.xml$')  
        logFile.close()
     
    def testGetSightingFile_SightingErrors_ShouldWriteNumberOfErrorsToLogFile(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        starFileName = "star.txt"
        ariesFileName = "ariesTest.txt"
        fix = Fix.Fix(logFileName)    
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-03-01</date>")
        sightingFile.write("<time>23:40:01</time>")
        sightingFile.write("<observation>015d04.9</observation>")
        sightingFile.write("<body>Aldebaran</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>72</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Artificial</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-03-02dsf</date>")
        sightingFile.write("<time>00:05:05</time>")
        sightingFile.write("<observation>045d15.2</observation>")
        sightingFile.write("<body>Peacock</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>71</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Natural</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()       
        fix.setSightingFile(sightingFileName)
        
        starFile = open(starFileName, "a+") 
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.write("Rigel    01/01/17    360d60.0    -61d60.0\n")
        starFile.close()
        fix.setStarFile(starFileName)
        ariesFile = open(ariesFileName, "a+") 
        ariesFile.write("04/11/17    19    125d25.2\n")
        ariesFile.write("04/11/17    23    140d27.7\n")
        ariesFile.close()
        fix.setAriesFile(ariesFileName)
        
        fix.getSightingFile()
        logFile = open(logFileName, "r")
        firstLine = logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        thirdLine = logFile.readline().rstrip()
        fourthLine = logFile.readline().rstrip()
        fifthLine = logFile.readline().rstrip()
        sixthLine = logFile.readline().rstrip()
        seventhLine = logFile.readline().rstrip()
        self.assertRegexpMatches(firstLine, r'logFile.txt$')
        self.assertRegexpMatches(secondLine, r'sighting.xml$')
        self.assertRegexpMatches(thirdLine, r'star.txt$')
        self.assertRegexpMatches(fourthLine, r'ariesTest.txt$')
        self.assertRegexpMatches(fifthLine, r'Start of sighting file: sighting.xml$')
        self.assertRegexpMatches(sixthLine, r'End of sighting file: sighting.xml$')
        self.assertRegexpMatches(seventhLine, r'Sighting Errors:    2$')
        logFile.close()
        
    def testGetSightingFile_SortSightingsByDate_ShouldLogSightingsInCorrectOrder(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        starFileName = "star.txt"
        ariesFileName = "ariesTest.txt"
        fix = Fix.Fix(logFileName)    
        if(Path.exists("sighting.xml")):
            OS.remove("sighting.xml")
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-04-14</date>")
        sightingFile.write("<time>23:50:14</time>")
        sightingFile.write("<observation>015d04.9</observation>")
        sightingFile.write("<body>Pollux</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>72</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Artificial</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2017-04-17</date>")
        sightingFile.write("<time>09:30:30</time>")
        sightingFile.write("<observation>045d15.2</observation>")
        sightingFile.write("<body>Sirius</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>71</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Natural</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2011-04-17</date>")
        sightingFile.write("<time>10:30:30</time>")
        sightingFile.write("<observation>00d0.2</observation>")
        sightingFile.write("<body>Unknown</body>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()       
        fix.setSightingFile(sightingFileName)
        
        starFile = open(starFileName, "a+") 
        starFile.write("Pollux    01/01/17    243d25.2    27d59.0\n")
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.close()
        fix.setStarFile(starFileName)
        ariesFile = open(ariesFileName, "a+") 
        ariesFile.write("04/11/17    19    125d25.2\n")
        ariesFile.write("04/11/17    23    140d27.7\n")
        ariesFile.close()
        fix.setAriesFile(ariesFileName)
        
        fix.getSightingFile()
        logFile = open(logFileName, "r")
        firstLine = logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        thirdLine = logFile.readline().rstrip()
        fourthLine = logFile.readline().rstrip()
        fifthLine = logFile.readline().rstrip()
        sixthLine = logFile.readline().rstrip()
        seventhLine = logFile.readline().rstrip() 
        self.assertRegexpMatches(firstLine, r'logFile.txt$')
        self.assertRegexpMatches(secondLine, r'sighting.xml$')
        self.assertRegexpMatches(thirdLine, r'star.txt$')
        self.assertRegexpMatches(fourthLine, r'ariesTest.txt$')
        self.assertRegexpMatches(fifthLine, r'Start of sighting file: sighting.xml$')
        self.assertRegexpMatches(sixthLine, r'End of sighting file: sighting.xml$')
        self.assertRegexpMatches(seventhLine, r'Sighting Errors:    3$')
        logFile.close()
        
    def testGetSightingFile_LogLongitudeAndLatitude_ShouldLogLongitudeAndLatitude(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        starFileName = "star.txt"
        ariesFileName = "aries.txt"
        if(Path.exists("logFile.txt")):
            OS.remove("logFile.txt")
        fix = Fix.Fix(logFileName)    
        if(Path.exists("sighting.xml")):
            OS.remove("sighting.xml")
        
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2017-04-14</date>")
        sightingFile.write("<time>23:50:14</time>")
        sightingFile.write("<observation>015d04.9</observation>")
        sightingFile.write("<body>Pollux</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>72</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Artificial</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2017-04-09</date>")
        sightingFile.write("<time>09:30:30</time>")
        sightingFile.write("<observation>045d15.2</observation>")
        sightingFile.write("<body>Sirius</body>")
        sightingFile.write("<height>6.0</height>")
        sightingFile.write("<temperature>71</temperature>")
        sightingFile.write("<pressure>1010</pressure>")
        sightingFile.write("<horizon>Natural</horizon>")
        sightingFile.write("</sighting>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2011-04-17</date>")
        sightingFile.write("<time>10:30:30</time>")
        sightingFile.write("<observation>00d0.2</observation>")
        sightingFile.write("<body>Unknown</body>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()       
        fix.setSightingFile(sightingFileName)
        
        starFile = open(starFileName, "w") 
        starFile.write("Pollux    01/01/17    243d25.2    27d59.0\n")
        starFile.write("Sirius    01/01/17    258d31.7    -16d44.3\n")
        starFile.close()
        fix.setStarFile(starFileName)
        fix.setAriesFile(ariesFileName)
        
        fix.getSightingFile()
        logFile = open(logFileName, "r")
        firstLine = logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        thirdLine = logFile.readline().rstrip()
        fourthLine = logFile.readline().rstrip()
        fifthLine = logFile.readline().rstrip()
        sixthLine = logFile.readline().rstrip()
        seventhLine = logFile.readline().rstrip()
        eigthLine = logFile.readline().rstrip()
        ninethLine = logFile.readline().rstrip()     
        self.assertRegexpMatches(firstLine, r'logFile.txt$')
        self.assertRegexpMatches(secondLine, r'sighting.xml$')
        self.assertRegexpMatches(thirdLine, r'star.txt$')
        self.assertRegexpMatches(fourthLine, r'aries.txt$')
        self.assertRegexpMatches(fifthLine, r'Start of sighting file: sighting.xml$')
        self.assertRegexpMatches(sixthLine, r'Sirius 2017-04-09 09:30:30 45d12.0 -16d44.3 239d12.8$')
        self.assertRegexpMatches(seventhLine, r'Pollux 2017-04-14 23:50:14 15d1.2 27d59.0 84d33.3$')
        self.assertRegexpMatches(eigthLine, r'End of sighting file: sighting.xml$')
        self.assertRegexpMatches(ninethLine, r'Sighting Errors:    1$')
        logFile.close()
        OS.remove("logFile.txt")
        
