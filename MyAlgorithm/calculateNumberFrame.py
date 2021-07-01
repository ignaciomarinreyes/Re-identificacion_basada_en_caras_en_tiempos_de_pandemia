# Tasa de fotogramas por segundo, 50

tframe = 50
hours= 0
minutes= 9
seconds = 10

totalSeconds = seconds + minutes * 60 + hours *3600
numberFrame = totalSeconds * tframe
print("Number Frame: " + str(numberFrame))