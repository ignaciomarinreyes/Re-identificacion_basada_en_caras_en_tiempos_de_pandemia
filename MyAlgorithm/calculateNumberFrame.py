# Tasa de fotogramas por segundo, 50

tframe = 50
hours= 1
minutes= 53
seconds = 36

totalSeconds = seconds + minutes * 60 + hours *3600
numberFrame = totalSeconds * tframe
print("Number Frame: " + str(numberFrame))