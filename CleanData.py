# Custom Python file Load
import organizeData as od
from subprocess import Popen, PIPE,call

# Create the csv file
def createCSVFile(f,index):
    fileName = "./Data/Raw/" + f + "/" + app + "%02d"%index + ".pcapng"  #Wireshark File Name
    print(fileName)
    outputFile ="./Data/Clean/" + f + "/" +app+"%02d"%index+".csv"  #CSV File Name
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
                print(lines[i]rstrip(),file=f)

        f.close()



###############################
######### Run Program #########
###############################

app = input("What App? ")

infoFileOpen = "./Data/Clean/"+ app + "/" + app +"_Info.txt"

try:
    #Open the File
    infoFile = open(infoFileOpen,"w")
except IOError:
    print("Error Couldn't Open Info File")
with infoFile:
    for i in range(1,31):
        createCSVFile(app,i)
        moveComments(infoFile,app,i)
        od.cleanData(app, i) 
