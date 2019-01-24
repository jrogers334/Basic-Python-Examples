import os, errno, openpyxl, re

#DELETE the description column (Don't know why I did this!!)

#this is does not include subs or submittals. 

# A0 B1 C2 D3 E4 F5 G6 H7 I8 J9 K10 L11 M12 N13

# GUI ME!   
# the directory for the sub folders
path = 'C:\\Users\\Jim\\Desktop\\Programming\\tccoturnover\\procorefolder'

nonMepFolders = ['001_PM and Superintendant Contacts', '002_Specifications', '003_Submittals', '004_QAQC', '006_Warranties', '005_O&M Manuals']

mepFolders = ['001_PM and Superintendant Contacts', '002_Specifications', '003_Submittals', '004_QAQC', '005_As-Builts', '007_Warranties', '006_O&M Manuals', '008_Commissioning Reports' ]

qaqcFolders = ['001_Pre-Installation Meeting Minutes', '002_Progress Photos', '003_Inspection Reports']

subqaqcfolders = ['001_Turner Reports', '002_Third Party Reports']

#contractDocsFolders = ['Contract Documents', 'Specifications']

submittalFolders = ['002_Shop Drawings', '001_Product Data']

mepDivions = ['14', '21', '22', '23', '25', '26', '27', '28']


# GUI ME!   
# test list of 'sub folders' to be contained within the folders in the specs list

# Submittal Export
wb = openpyxl.load_workbook('allsubmittals.xlsx')
sheet = wb['Sheet1']

# Spec export 
wb2 = openpyxl.load_workbook('speclog2.xlsx')
sheet2 = wb2['Sheet1']


#---------------------#
#--Makes Div and Spec Folders From Lists in this Block--#
#---------------------#


# creates a list of values from the Sheet1 column 'B'. The list is required because the data is in a tuple 
# remove the first value since it will be the column title
vrlist = []
for i in list(sheet2.columns)[1]:
    vrlist.append(i.value)
del vrlist[0]

# creates a new that looks at each value in vrlist and determines if it is less than 6 characters
# if it is less than 6 it takes the delta and adds that number of leading zeros to the existing values and adds them to fldrlist
# fldrlist is now the list of folders to be created by mkdirTurnover
fldrlist = []
for x in vrlist:
    if len(str(x)) < 6:
        fldrlist.append(((6-len(str(x)))*'0')+str(x))
    else:
        fldrlist.append(str(x))

# creates a list of values from the Sheet1 column 'C'. The list is required because the data is in a tuple 
# remove the first value since it will be the column title
deslist = []
for n in list(sheet2.columns)[2]:
    deslist.append((n.value).strip())
del deslist[0]


# USE TOTALFLDR to create folders in the below function
# combines vrlist and vrlistdes to create a new list that is the spec section + ' - ' + the spec description
# this new list will be used to create the folders with the below functions
totalfldr = []
for i in range(len(fldrlist)):
    totalfldr.append(str(fldrlist[i]) + ' - ' + str(deslist[i]))

# DIVPATH == THE LIST OF DIV FOLDERS AND PATHS BASED ON path ABOVE
# divslong is a list of the first two characters in each of the specs
# divpathlist is a list of unique values from dvislong
# divpath is a list of the path concatenated with each of the values in divpathlist
divslong = []
for j in fldrlist:
    divslong.append(j[:2])

divpathlist = list(set(divslong))

divpath = []
for x in divpathlist:
    divpath.append(path + '\\Division ' + x)

#print(divpath)


#---------------------#
#--Makes a List of Spec, Sub, and Submittal information--#
#---------------------#


specRawList = []  # list of every line item in the Spec Section, column A
for a in list(sheet.columns)[0]:
    specRawList.append(a.value)
del specRawList[0]
specListNone = list(set(specRawList))  # list of unique Spec Sections
specList = [x for x in specListNone if x is not None]


divListLng = []
for b in specList:
    divListLng.append('Division ' + b[:2])
divList = list(set(divListLng))  # list of unique Divisions


specNums = []
for c in specList:
    hc, sc, tc = c.partition('-')
    specNums.append(hc.strip())

subNum = []  # list submittal number with 3 digit number following -
subNumRawNone = []
for d in list(sheet.columns)[1]:
    subNumRawNone.append(d.value)
del subNumRawNone[0]
subNumRaw = [x for x in subNumRawNone if x is not None]
for e in subNumRaw:
    head, sep, tail = e.partition('-')
    if len(str(tail)) < 3:
        subNum.append(head + '-' + ((3-len(str(tail)))*'0')+str(tail))
    else:
        subNum.append(head + '-' + tail)
revNum = []  # list of all rev numbers    
for f in list(sheet.columns)[5]:
    revNum.append(f.value)
del revNum[0]

totalSubNum = []  # list of submittals 000000-000-0
for g,h in zip(subNum, revNum):
    totalSubNum.append(str(g) + '-' + str(h))

subDesNone = []
for i in list(sheet.columns)[3]:
    subDesNone.append(i.value)
del subDesNone[0]
subDes = [x for x in subDesNone if x is not None]
subDesClean = []
for p in subDes:
    q = re.sub('[/\:*?"<>|]', '', p)
    subDesClean.append(q)


contractors = []  # list of all contractors
for j in list(sheet.columns)[7]:
    contractors.append(j.value)
del contractors[0]

#Approver's Possible Response Options: Approved, Approved As Noted, Pending, Rejected, Reviewed, Revise and Resubmit, Void

status = []
cleanStatus = []
for k in list(sheet.columns)[28]:
    status.append(str(k.value))
del status[0]
for p in status:  # note that you can't just "replace" an item in a list, you need to replace what you want in the item and then append it new value to a different list
    cleanStatus.append(p.replace('\n', ', '))

#Test run, it worked
#tube = 'Approved\nApproved'
#tube = tube.replace('\n', ', ')
#print(tube)



mapped = zip(specRawList, contractors, totalSubNum, subDesClean, cleanStatus)
mapped = list(mapped)
mapped_list = [list(x) for x in mapped]  # makes a 2D array

#print(len(mapped_list))

mappedlm = mapped_list[:]  # this exists to change the range of the list to run a sample set of data

#print(mappedlm[:10])

word = 'Approved'
mappedApproved = []
for x in mappedlm:
    if word in x[4]:
        mappedApproved.append(x)

#print(len(mappedlm))
#print(len(mappedApproved))
#print(mappedApproved)

mappedcombined = []
for o in mappedApproved:
    fixed = (o[0].strip(), o[1].strip(), (o[2].strip() + ' ' + o[3].strip() + ' ' + o[4].strip()))
    mappedcombined.append(fixed)

#for h in mappedcombined[:5]:
#    print(str(h[2].split()))
    

print(mappedcombined[:5])

for h in mappedcombined[:50]:
    if h[0][:2] in mepDivions:
        print(h[2])
#for h in mappedcombined:
#    print(h[0][:2])


#divlist - use divpath
#speclist - use totalfldr

def mkdirDivSpec(divlist, speclist, subfldr):
    for j in divlist:
        try:
            os.makedirs(j)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for k in speclist:
            if k[:2] == j[-2:]:
                for h in subfldr:
                    try:
                        os.makedirs(j + '\\' + k + '\\' + h)
                    except OSError as e:
                        if e.errno != errno.EEXIST:
                            raise


def mkdirDivNonMep(divlist, speclist, submittallist, subfolders, qaqc, subsubfolders, subqaqcs):
    for j in divlist:
        try:
            os.makedirs(j)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for k in speclist:
            if k[:2] == j[-2:]:
                for h in submittallist:
                    if h[0][:7] == k[:7]:
                        for p in subfolders:
                            if p == '004_QAQC':
                                for t in qaqc:
                                    if t == '003_Inspection Reports':
                                        for u in subqaqcs:
                                            try:
                                                os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t + '\\' + u)
                                            except OSError as e:
                                                if e.errno != errno.EEXIST:
                                                    raise
                                    else:
                                        try:
                                            os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t)
                                        except OSError as e:
                                            if e.errno != errno.EEXIST:
                                                raise

                            elif p == '003_Submittals':
                                for u in subsubfolders:
                                    try:
                                        os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + u)
                                    except OSError as e:
                                        if e.errno != errno.EEXIST:
                                            raise
                                txtPath = j + '\\' + k + '\\'+ str(h[1]) + '\\' + p + '\\'
                                nof = str(h[2]).split()
                                nofsplit = str(nof[0])
                                completeName = os.path.join(txtPath, nofsplit + '.txt')
                                file1 = open (completeName, 'w')
                                tofile = 'This is a place holder txt file, please delete this when the coresponding submittal has been added to the appropriate folder.'
                                file1.write(tofile)
                                file1.close()

                            else:
                                try:
                                    os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p)
                                except OSError as e:
                                    if e.errno != errno.EEXIST:
                                        raise



def mkdirDivMep(divlist, speclist, submittallist, subfolders, qaqc, subsubfolders, subqaqcs):
    for j in divlist:
        try:
            os.makedirs(j)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for k in speclist:
            if k[:2] == j[-2:]:
                for h in submittallist:
                    if h[0][:7] == k[:7]:
                        for p in subfolders:
                            if p == '004_QAQC':
                                for t in qaqc:
                                    if t == '003_Inspection Reports':
                                        for u in subqaqcs:
                                            try:
                                                os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t + '\\' + u)
                                            except OSError as e:
                                                if e.errno != errno.EEXIST:
                                                    raise
                                    else:
                                        try:
                                            os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t)
                                        except OSError as e:
                                            if e.errno != errno.EEXIST:
                                                raise
                            elif p == '003_Submittals':
                                for u in subsubfolders:
                                    try:
                                        os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + u)
                                    except OSError as e:
                                        if e.errno != errno.EEXIST:
                                            raise
                                txtPath = j + '\\' + k + '\\'+ str(h[1]) + '\\' + p + '\\'
                                nof = str(h[2]).split()
                                nofsplit = str(nof[0])
                                completeName = os.path.join(txtPath, nofsplit + '.txt')
                                file1 = open (completeName, 'w')
                                tofile = 'This is a place holder txt file, please delete this when all the coresponding submittals has been added to the appropriate folders.'
                                file1.write(tofile)
                                file1.close()            
                            #elif p == 'Contract Documents':
                                #for v in contractdocsubfolders:
                                    #try:
                                        #os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + v)
                                    #except OSError as e:
                                        #if e.errno != errno.EEXIST:
                                            #raise                
                            else:
                                try:
                                    os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p)
                                except OSError as e:
                                    if e.errno != errno.EEXIST:
                                        raise
def mkdirDivCombined(divlist, speclist, submittallist, mepsubfolders, subfolders, qaqc, subsubfolders, subqaqcs, mepdivs):
    for j in divlist:
        try:
            os.makedirs(j)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for k in speclist:
            if k[:2] == j[-2:]:
                for h in submittallist:
                    if h[0][:7] == k[:7]:
                        if h[0][:2] in mepdivs:
                            for p in mepsubfolders:
                                if p == '004_QAQC':
                                    for t in qaqc:
                                        if t == '003_Inspection Reports':
                                            for u in subqaqcs:
                                                try:
                                                    os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t + '\\' + u)
                                                except OSError as e:
                                                      if e.errno != errno.EEXIST:
                                                        raise
                                        else:
                                            try:
                                                os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t)
                                            except OSError as e:
                                                if e.errno != errno.EEXIST:
                                                    raise

                                elif p == '003_Submittals':
                                    for u in subsubfolders:
                                        try:
                                            os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + u)
                                        except OSError as e:
                                            if e.errno != errno.EEXIST:
                                                raise
                                    txtPath = j + '\\' + k + '\\'+ str(h[1]) + '\\' + p + '\\'
                                    nof = str(h[2]).split()
                                    nofsplit = str(nof[0])
                                    completeName = os.path.join(txtPath, nofsplit + '.txt')
                                    file1 = open (completeName, 'w')
                                    tofile = 'This is a place holder txt file, please delete this when the coresponding submittal has been added to the appropriate folder.'
                                    file1.write(tofile)
                                    file1.close()
                                else:
                                    try:
                                        os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p)
                                    except OSError as e:
                                        if e.errno != errno.EEXIST:
                                            raise
                        else:
                            for p in subfolders:
                                if p == '004_QAQC':
                                    for t in qaqc:
                                        if t == '003_Inspection Reports':
                                            for u in subqaqcs:
                                                try:
                                                    os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t + '\\' + u)
                                                except OSError as e:
                                                    if e.errno != errno.EEXIST:
                                                        raise
                                        else:
                                            try:
                                                os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + t)
                                            except OSError as e:
                                                if e.errno != errno.EEXIST:
                                                    raise

                                elif p == '003_Submittals':
                                    for u in subsubfolders:
                                        try:
                                            os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + u)
                                        except OSError as e:
                                             if e.errno != errno.EEXIST:
                                                raise
                                    txtPath = j + '\\' + k + '\\'+ str(h[1]) + '\\' + p + '\\'
                                    nof = str(h[2]).split()
                                    nofsplit = str(nof[0])
                                    completeName = os.path.join(txtPath, nofsplit + '.txt')
                                    file1 = open (completeName, 'w')
                                    tofile = 'This is a place holder txt file, please delete this when the coresponding submittal has been added to the appropriate folder.'
                                    file1.write(tofile)
                                    file1.close()

                                else:
                                    try:
                                        os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p)
                                    except OSError as e:
                                        if e.errno != errno.EEXIST:
                                            raise

#mkdirDivNonMep(divpath, totalfldr, mappedcombined, nonMepFolders, qaqcFolders, submittalFolders, subqaqcfolders)

#mkdirDivMep(divpath, totalfldr, mappedcombined, mepFolders, qaqcFolders, submittalFolders, subqaqcfolders)

mkdirDivCombined(divpath, totalfldr, mappedcombined, mepFolders, nonMepFolders, qaqcFolders, submittalFolders, subqaqcfolders, mepDivions)


#This block needs work in before creating text files. 
#                            elif p == 'Submittals':
#                                for u in submittalFolders:
#                                    try:
#                                        os.makedirs(j + '\\' + k + '\\' + str(h[1]) + '\\' + p + '\\' + str(u[2][:12]) + '.txt')
#                                    except OSError as e:
#                                        if e.errno != errno.EEXIST:
#                                            raise





### This chunk of code is a work in progress to highlight only those items that are the most current revision, the approach is to call out only those items that are approved regardless of revision number

#subNumList = []
#for t in mappedlm:
#    subNumList.append(t[3])

#subNumUnique = list(set(subNumList))

#print(len(subNumList))
#print(len(subNumUnique))

#test2 = []
#i = 0  # len(subNumUnique)
#while i < (len(mappedlm)-1):
#    if mappedlm[i][3].strip() == mappedlm[i+1][3].strip():
#        #mappedlm.pop((i+1))
#        test2.append(mappedlm[i+1])
#    else:
#        pass
#    i += 1

#print(len(mappedlm))
#print(len(test2))

#test = []
#for o in mappedlm:
#    test.append(o[3])
#print('len test ' + str(len(test)))
#print(test)
#print(test2)

#final = []
#for x in mappedlm:
#    for y in test2:
#        if x[3] != y[3]:
#            final.append(x)

#finalcount = []
#for q in final:
#    finalcount.append(q[3])
#print(len(set(finalcount)))

#finaltuple = []
#for s in final:
#    finaltuple.append(tuple(s))
#pft = set(tuple(finaltuple))










#print(len(pft))

#for i in pft:
#    print(i)




#i = 0
#while i < len(mappedmod[:10]):
#    if mappedmod[i][3] == mappedmod[i+1][3]:
#        print(mappedmod[i][3])
#    else:
#        pass
#        #print(mappedmod[i][3])
#    i += 1


#print(mappedmod[:10])


#for l in range(0, len(mappedmod[:10])):
    #if mappedmod[l][3] == mappedmod[l+1][3]:
        #print(mappedmod[l])









        

