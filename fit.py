from sklearn.externals import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
#order of events
#1. Load the data
#2. Adjust formatting for scikitlearn to read
#	a. change training to arrays (data)
#	b. change labels to numbers (target)
#3. Cross Validate
#	a. Split the data into training and test
#	b. call cross_val_score
#4. Pass into fitting
#	
