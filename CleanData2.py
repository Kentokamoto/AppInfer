# Custom Python file Load
import organizeData as od
import csv
from subprocess import Popen, PIPE,call
import os, errno
import sys

devices = [ "HTC One M8", "Nexus 6P", "Pixel" ]

# Create the csv file
def createCSVFile(app,index,device):
    for week in range(1,3):
        fileName = "./Data/Test2/Raw/" + device + "/" + app + "/"  +str(week) + "/" + app + "%02d"%index + ".pcapng"  #Wireshark File Name
        outputFile ="./Data/Test2/Clean/" + device + "/" + app + "/" + str(week) + "/" + app+"%02d"%index+".csv"  #CSV File Name
        
        # Check if the directory exists first before we begin to do fancy things
        dir = "./Data/Test2/Clean/" + device + "/" + app + "/" + str( week ) + "/"
        try:
            os.makedirs( dir )
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise 
        # Add the output of tcptrace to an csv file
        with open(outputFile,"w") as f: 
            try:
                cmd = ["tcptrace","-l","--csv",fileName]
                #Run Shell Command
                call(cmd,stdout=f)
                #Close File
                f.close()
            except IOError:
                print("Error(CreateCSV) Couldn't open file")
   #Organize csv so it can be read into pandas without problems

def moveComments(infoFile, appName, index, device):
    for week in range(1,3):
        # Move the top 8 lines to the info file and delete them from the csv File
        outputFile ="./Data/Test2/Clean/" + device + "/" + appName + "/" + str(week) + "/" + appName +"%02d"%index+".csv"  #CSV File Name
        lines = []
        with open( outputFile, "r" ) as f:
            try:
                lines = f.readlines()
                f.close()
            except:
                print( "Error(MoveComments1) Couldn't open file: %s"%outputFile )

        with open( outputFile, "w" ) as f:
            try:
                for i in range(8):
                    print(lines[i].rstrip(), file=infoFile)

                for i in range(8, len(lines)):
                    print(lines[i].rstrip(), file=f)

                f.close()
            except:
                print( "Error(MoveComments2) Couldn't open file: %s"%outputFile )


###############################
######### Run Program #########
###############################
app = sys.argv[1]
print(app)
for dev in devices:
    infoFileOpen = "./Data/Test2/Clean/"+ dev  + "/" +app + "/" + app +"_Info.txt"
    try:
        #Open the File
        extraInfoFile = open(infoFileOpen,"w")
    except IOError:
        print("Error(Main) Couldn't Open Info File: %s"%infoFileOpen)
    with extraInfoFile:
        with open("./Data/Test2/Clean/"+ dev + "/" + app + "/" + app + "_final.csv","w") as f:
            writer = csv.writer(f)
            for i in range(1,31):
                #Something's wrong with this instance so we're skipping it
                if app  == "WhatsApp" and (i == 4 and dev == "Pixel"):
                    print("Skipping")
                    continue

                createCSVFile(app,i,dev)
                moveComments(extraInfoFile,app,i,dev)
                
                data, name = od.cleanData(app, i ,dev)
                if i == 1:
                    writer.writerow(name)

                writer.writerow(data)
                
