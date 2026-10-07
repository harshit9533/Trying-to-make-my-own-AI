from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()

print(device)

print(type(device))

print(dir(device))