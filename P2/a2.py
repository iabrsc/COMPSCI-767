#Ian Schwartz--COMPSCI767--Assignment2

import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt


#---reads in the csv files from specified directory (use double-backslash because single is an escape)---
#   fA = Amazon, fN = Newegg
fA = pd.read_csv('C:\\Users\\kiing\\scripts\\cleanTableAmazon.csv')

#I see that i am only to focus table A ^^^^
#fN = pd.read_csv('C:\\Users\\kiing\\scripts\\tableNewegg3.csv')

#---Check column names if necessary---
#print(fA.columns)
#print(fN.columns)

missingNameA = fA['Name'].isnull().sum()
missingPriceA = fA['Price'].isnull().sum()
missingRatingA = fA['Rating'].isnull().sum()
missingNumRatingsA = fA['Number of Ratings'].isnull().sum()
missingDisplayA = fA['Display Size (inches)'].isnull().sum()
missingDiskA = fA['Disk Size (GB)'].isnull().sum()
missingRAMA = fA['RAM (GB)'].isnull().sum()
missingOSA = fA['Operating System'].isnull().sum()

#---total number of rows/records---
totalColumns = fA.shape[0]
#print(str(totalColumns))

#Missing items by fraction (fr) and percentages (per) based on the total number of rows/records
frName = (missingNameA / totalColumns)
perName = (frName * 100)
frPrice = (missingPriceA / totalColumns)
perPrice = (frPrice * 100) 
frRating = (missingRatingA / totalColumns)
perRating = (frRating * 100)
frNumRatings = (missingNumRatingsA / totalColumns)
perNumRatings = (frNumRatings * 100)
frDisplay = (missingDisplayA / totalColumns)
perDisplay = (frDisplay * 100)
frDisk = (missingDiskA / totalColumns)
perDisk = (frDisk * 100)
frRAM = (missingRAMA / totalColumns)
perRAM = (frRAM * 100)
frOS = (missingOSA / totalColumns)
perOS = (frOS * 100)


#potential standardization (untested)
#fA['Price'] = fA['Price'].apply(lambda x: '{:.2f}'.format(x))

#Printing the values obtained above ^^^
print('Fractional Name Missing: '+str(frName))
print('Percentage of Names Missing: '+str(perName)+'%')
print('Fractional Price Missing: '+str(frPrice))
print('Percentage Price Missing: '+str(perPrice)+'%')
print('Fractional Rating Missing: '+str(frRating))
print('Percentage of Ratings Missing: '+str(perRating)+'%')
print('Fractional Number of Ratings Missing: '+str(frNumRatings))
print('Percentage of Number of Ratings Missing: '+str(perNumRatings)+'%')

print('Fractional Display Size Missing: '+str(frDisplay))
print('Percentage of Display Size Missing: '+str(perDisplay)+'%')
print('Fractional Disk Space Missing: '+str(frDisk))
print('Percentage of Disk Space Missing: '+str(perDisk)+'%')
print('Fractional RAM Missing: '+str(frRAM))
print('Percentage of RAM Missing: '+str(perRAM)+'%')
print('Fractional OS Missing: '+str(frOS))
print('Percentage of OS Missing: '+str(perOS)+'%')


#-----------------------------------------------------------
#-----------------------------------------------------------


#---TEXTUAL AVERAGE LENGTH---

#creates new columns 'Name Length' and 'OS Length' that store the length of each string
fA['Name Length'] = fA['Name'].str.len()
fA['OS Length'] = fA['Operating System'].str.len()

#get the mean length from those generated columns
avgNameLength = fA['Name Length'].mean()
avgOSLength = fA['OS Length'].mean()

print('Average Name Length: ' + str(avgNameLength))
print('Average Operating System Length: ' + str(avgOSLength))


#-----------------------------------------------------------
#-----------------------------------------------------------




#Boxplot for visual detection of outliers
sns.boxplot(x=fA['Price'])
plt.show()

#Histogram of price in dataframe, for visual distribution of values
fA['Price'].hist(bins=30)
plt.show()

#IQR (interquartile range) method for statistical detection of outliers, found online
Q1 = fA['Price'].quantile(0.25)
Q3 = fA['Price'].quantile(0.75)
IQR = Q3 - Q1
outliers = fA[(fA['Price'] < Q1-1.5*IQR ) | (fA['Price'] > Q3+1.5*IQR)]['Price']

#Histogram of OS in dataframe, for visual distribution of values
fA['OS Length'].hist(bins=30)
plt.show()

Q1OS = fA['OS Length'].quantile(0.25)
Q3OS = fA['OS Length'].quantile(0.75)
IQROS = Q3OS - Q1OS
outliers2 = fA[(fA['OS Length'] < Q1OS-1.5*IQROS ) | (fA['OS Length'] > Q3OS+1.5*IQROS)]['OS Length']






