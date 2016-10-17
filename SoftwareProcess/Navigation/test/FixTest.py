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
        self.assertRegexpMatches(firstLine, r'Start of Log$')
        
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
        
    def testGetSightingFile_SightingFileNotSet_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        fix = Fix.Fix(logFileName)        
        expectedDiag =  "Fix.getSightingFile:  no sighting file has been set."
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testGetSightingFile_MissingMandatoryTags_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        expectedDiag =  "Fix.getSightings: Invalid sighting file. The date, time, observation and body tags must be present."
        fix = Fix.Fix(logFileName)  
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
        
    def testGetSightingFile_DateInWrongFormat_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        expectedDiag =  "Fix.getSightings:  Invalid date. Must be of format yyyy-mm-dd."
        fix = Fix.Fix(logFileName)    
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>16-12_31</date>")
        sightingFile.write("<time>23:40:01</time>")
        sightingFile.write("<observation>045d15.2</observation>")
        sightingFile.write("<body>Aldebaran</body>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()    
        fix.setSightingFile(sightingFileName)
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def testGetSightingFile_TimeInWrongFormat_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        expectedDiag =  "Fix.getSightings: Invalid time Must be of format hh:mm:ss."
        fix = Fix.Fix(logFileName)    
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-03-01</date>")
        sightingFile.write("<time>520:9999:24</time>")
        sightingFile.write("<observation>045d15.2</observation>")
        sightingFile.write("<body>Aldebaran</body>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()       
        fix.setSightingFile(sightingFileName)
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def testGetSightingFile_ObservationInWrongFormat_ShouldThrowValueError(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
        expectedDiag =  "Fix.getSightings: Invalid Observation string. Must be of form xdy.y"
        fix = Fix.Fix(logFileName)    
        sightingFile = open(sightingFileName, "a+") # Open file for appending and reading
        sightingFile.write("<fix>")
        sightingFile.write("<sighting>")
        sightingFile.write("<date>2016-03-01</date>")
        sightingFile.write("<time>23:40:01</time>")
        sightingFile.write("<observation>f34dd4.2</observation>")
        sightingFile.write("<body>Aldebaran</body>")
        sightingFile.write("</sighting>")
        sightingFile.write("</fix>")
        sightingFile.close()       
        fix.setSightingFile(sightingFileName)
        with self.assertRaises(ValueError) as context:
            fix.getSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        
    def testGetSightingFile_WriteToLogFile_ShouldWriteToLogFile(self):
        logFileName = "logFile.txt"
        sightingFileName = "sighting.xml"
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
        fix.getSightingFile()
        logFile = open(logFileName, "r")
        firstLine = logFile.readline().rstrip()
        secondLine = logFile.readline().rstrip()
        thirdLine = logFile.readline().rstrip()
        fourthLine = logFile.readline().rstrip()
        fifthLine = logFile.readline().rstrip()
        self.assertRegexpMatches(firstLine, r'Start of Log$')
        self.assertRegexpMatches(secondLine, r'Start of sighting file: sighting.xml$')
        self.assertRegexpMatches(thirdLine, r'Aldebaran 2016-03-01 23:40:01 15d1.2$')
        self.assertRegexpMatches(fourthLine, r'Peacock 2016-03-02 00:05:05 45d12.0$')
        self.assertRegexpMatches(fifthLine, r'End of sighting file: sighting.xml$')
        
