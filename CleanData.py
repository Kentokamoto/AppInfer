import pandas as pd
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
        Print("Error Couldn't open file")
    with f:
        cmd = ["tcptrace","-l","--csv",fileName]
        #Run Shell Command
        call(cmd,stdout=f)
        #Close File
        f.close()



# Condense the csv file so it is in proper order for scikitlearn
def cleanData(f,index):
    fb = pd.read_csv("Facebook.csv")


###############################
######### Run Program #########
###############################

app = input("What App? ")

for i in range(1,31):
   createCSVFile(app,i) 

