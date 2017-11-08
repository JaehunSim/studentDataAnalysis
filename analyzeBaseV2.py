# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame, Series
import re
import numpy as np
pd.set_option('display.unicode.east_asian_width',True) #한국어 있으면 column 맞춰서 정렬
pd.set_option("display.float_format", '{0:,.0f}'.format)
pd.set_option('display.width', 1000) #열들이 넓게 프린트 될수 있게함 

data = pd.read_csv("studentData.csv", encoding="euc-kr")             

majorCount = data.iloc[:,3].value_counts()

bigMajorCount = data.iloc[:,2].value_counts()

studentNum = data.iloc[:,0]
studentNumFirst4 = studentNum.apply((lambda x: str(x)[:4]))
studentNumFirst4Count = studentNumFirst4.value_counts()

studentName = data.iloc[:,1]
studentNameLast = studentName.apply((lambda x: str(x)[0]))
studentNameLastCount = studentNameLast.value_counts()

studentEmail = data.iloc[:,4]
emailList = []
emailIDList = []
emailRegexCompiler = re.compile("([\w.]+)[@]([\w.]+)") 
# ([\w.]+): email's ID part; group(1)
# [@]: "@" itself
# ([\w.]+): email's address part; group(2)
for i in range(len(studentEmail)):
    temp = emailRegexCompiler.search(studentEmail[i])
    emailList.append(temp.group(2))
    emailIDList.append(temp.group(1))
studentEmailDomain = Series(emailList)
studentEmailDomainCount = studentEmailDomain.value_counts()

studentEmailID = Series(emailIDList)
iDwithinBirthday = []
iDwithinPhoneNumber = []

iDwithinLastName = []
iDwithinFirstNameDirect = []
iDwithinFirstNameTranslate = []
iDwithinInitialName = []

birthdayRange = pd.date_range('2016-01-01', '2016-12-31').strftime('%m%d') # 0101 to 1231
yearRange = pd.date_range('1980-01-01','1999-01-01').strftime('%y')
yearRange4 = pd.date_range('1980-01-01','1999-01-01').strftime('%Y')
justNumbersRegexCompiler =  re.compile("[\d]+")
numberPartInID = []
numberPartIndexInID = []
for i in range(len(studentEmailID)):
    temp = justNumbersRegexCompiler.findall(studentEmailID[i])
    if len(temp) == 1:
        numberPartInID.append(temp[0])
        numberPartIndexInID.append(i)        
#exception Index: 49, 188
    
for i in range(len(numberPartInID)):
    if len(numberPartInID[i]) == 4:
        for year in yearRange4:
            if year in numberPartInID[i]:
                if studentEmailID[numberPartIndexInID[i]] not in iDwithinBirthday:
                    iDwithinBirthday.append(studentEmailID[numberPartIndexInID[i]])
    if len(numberPartInID[i]) in [4,6]:
        for date in birthdayRange:
            if date in numberPartInID[i]:
                if studentEmailID[numberPartIndexInID[i]] not in iDwithinBirthday:
                    iDwithinBirthday.append(studentEmailID[numberPartIndexInID[i]])
    if len(numberPartInID[i]) == 2:
          for smallYear in yearRange:
           if smallYear in numberPartInID[i]:
                if studentEmailID[numberPartIndexInID[i]] not in iDwithinBirthday:
                    iDwithinBirthday.append(studentEmailID[numberPartIndexInID[i]])
    
#exception Appending
iDwithinBirthday.append(studentEmailID[49])
iDwithinBirthday.append(studentEmailID[188])

studentPhoneNumber = data.iloc[:,5]
phoneNumberRegexCompiler = re.compile("([\d.]+)[-]([\d.]+)[-]([\d.]+)")
phoneNumberRegexCompiler2 = re.compile("[01]([\d.]{4})([\d.]{4})")
#([\d.]+):digit 0-9 group(1~3)
phoneFormer = []
phoneLatter = []
for i in range(len(studentPhoneNumber)):
    temp = phoneNumberRegexCompiler.search(studentPhoneNumber[i])
    temp2 = phoneNumberRegexCompiler2.search(studentPhoneNumber[i])
    if temp != None:
        phoneFormer.append([i,temp.group(2)])
        phoneLatter.append([i,temp.group(3)])
    elif temp2 != None:
        phoneFormer.append([i,temp2.group(1)])
        phoneLatter.append([i,temp2.group(2)])
    else:
        phoneFormer.append([i,"0000"]) #index 299
        phoneLatter.append([i,"0000"]) #index 299
#exception: index:299 02-889-2951 No relation with ID

formerNumbers = []
for i in phoneFormer:
    formerNumbers.append(i[1])        

concatFormer = ""
for i in formerNumbers:
    concatFormer += i
concatFormer = Series(list(concatFormer))
concatFormerCounts = concatFormer.value_counts()
concatFormerCounts = concatFormerCounts.sort_index()
    
latterNumbers = []
for i in phoneLatter:
    latterNumbers.append(i[1])        

concatLatter = ""
for i in latterNumbers:
    concatLatter += i
concatLatter = Series(list(concatLatter))
concatLatterCounts = concatLatter.value_counts()
concatLatterCounts = concatLatterCounts.sort_index()

for i in range(len(numberPartInID)):
    if (phoneFormer[numberPartIndexInID[i]][1] in numberPartInID[i]) or (phoneLatter[numberPartIndexInID[i]][1] in numberPartInID[i]):
        iDwithinPhoneNumber.append(studentEmailID[numberPartIndexInID[i]])
        
notNumberRegexCompiler = re.compile("[\D]+")
textPartInID = []
textPartIndexInID = []
for i in range(len(studentEmailID)):
    temp = notNumberRegexCompiler.findall(studentEmailID[i])
    if len(temp) == 1:
        textPartInID.append(temp[0])
        textPartIndexInID.append(i)