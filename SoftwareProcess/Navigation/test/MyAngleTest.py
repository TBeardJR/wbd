import Navigation.prod.Angle as Angle

angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()
angle4 = Angle.Angle()

angle1Degrees = angle1.setDegreesAndMinutes("45d0.0")
angle2Degrees = angle2.setDegrees(-19.5);
angle3Degrees = angle3.setDegreesAndMinutes("0d30.0");

addedDegrees1 = angle1.add(angle2)
addedDegrees2 = angle2.add(angle3)

subtractedDegrees = angle4.subtract(angle1)

angle1.setDegrees(40.0)
angle2.setDegrees(45.123)

comparison = angle1.compare(angle2)

angle1String = angle1.getString()
angle2String = angle2.getString()

print(angle2String)