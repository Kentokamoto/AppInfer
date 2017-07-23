# Custom Python file Load
import organizeData as od
import csv
from subprocess import Popen, PIPE,call

# Create the csv file
def createCSVFile(f,index):
    fileName = "./Data/Test" + testNum + "/Raw/" + f + "/" + app + "%02d"%index + ".pcapng"  #Wireshark File Name
    print(fileName)
    outputFile ="./Data/Test" + testNum + "/Clean/" + f + "/" +app+"%02d"%index+".csv"  #CSV File Name
    try: 
        #Open the CSV File
        f = open(outputFile,"w")
    except IOError:
        print("Error Couldn't open file")
    with f:
        cmd = ["tcptrace","-l","--csv",fileName]
        #Run Shell Command
        call(cmd,stdout=f)
        #Close File
        f.close()

#Organize csv so it can be read into pandas without problems
def moveComments(infoFile, appName, index):
    # Move the top 8 lines to the info file and delete them from the csv File
    outputFile ="./Data/Clean/" + appName  + "/" +appName+"%02d"%index+".csv"  #CSV File Name
    lines = []
    # Read and store lines in an array
    try:
        #Open the CSV file
        f = open(outputFile,"r")
    except IOError:
        print("Error Couldn't open file")
    with f:
        # Put lines into an array
                lines = f.readlines()

                f.close()
    # Put the information in the respective files
    try:
        #Open the CSV File to Write this time
        f = open(outputFile, "w")
    except IOError:
        print("Error Couldn't open file to read (moveComments)")
    with f:
        for i in range(8):
            print(lines[i].rstrip(),file=infoFile)

        for i in range(8,len(lines)):
            print(lines[i].rstrip(),file=f)

        f.close()



###############################
######### Run Program #########
###############################

app = input("What App? ")
testNum = input( "Which Test? 1 or 2? ")
infoFileOpen = "./Data/Test" + testNum + "/Clean/"+ app + "/" + app +"_Info.txt"
print(infoFileOpen)
try:
    #Open the File
    extraInfoFile = open(infoFileOpen,"w")
except IOError:
    print("Error Couldn't Open Info File")
with extraInfoFile:
    with open("./Data/Test" + testNum + "/Clean/"+ app + "/" + app + "_final.csv","w") as f:
        writer = csv.writer(f)
        for i in range(1,61):
            createCSVFile(app,i)
            moveComments(extraInfoFile,app,i)
            data, name = od.cleanData(app, i)
            if i == 1:
                writer.writerow(name)

            writer.writerow(data)
