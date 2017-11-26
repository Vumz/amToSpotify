import plistlib

xmlItunes = "itunes Music Library.xml"
itunesLib = plistlib.readPlist(xmlItunes)

with open("failure.txt", "w") as fail:
    with open("success.txt", "w") as success:
        for track, details in itunesLib['Tracks'].items():
            try:
                if (details.get("Kind") == "Apple Music AAC audio file"):
                    success.write(details.get("Name").encode("ascii", "ignore") + " , " + details.get("Artist").encode("ascii", "ignore") + "\n")
            except:
                fail.write(details.get("Name").encode("ascii", "ignore") + " , " + details.get("Artist").encode("ascii", "ignore") + "\n")
                print "something went wrong with the iTunes library XML parsing"

