## =================================================================== ##
#  this is file report.py, created at 25-Set-2015                       #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

import xml.etree.ElementTree as ET
import lattes as lt
import os
import datetime
import csv
import sys
import glob

def retrieveInfo(_program,_name,_fromyear):
 fromyear = float(_fromyear)
 area = 'ENGENHARIAS III'

 filePath = os.getcwd() + '/' + _program + '/'
 xmlFile = filePath + _name + '.xml'
 csvFile = os.getcwd() + '/qualis/' + 'Consulta_Webqualis' + '.csv'
 tree = ET.parse(xmlFile)

 pinfo = lt.personalInfo(tree)

 # [important,congress,journal,chapter,book]
 binfo = lt.technicalProduction(tree,csvFile,area,fromyear)
 important = binfo[0] 
 congress = binfo[1]
 journal = binfo[2]
 chapter = binfo[3]
 book = binfo[4]

 tinfo = lt.thesisConcluded(tree,fromyear)
 msc = []
 dsc = []
 if tinfo:
  msc = tinfo[0] 
  dsc = tinfo[1] 

 cinfo = lt.thesisNotConcluded(tree,fromyear)
 mscNot = []
 dscNot = []
 mscNot = cinfo[0] 
 dscNot = cinfo[1] 

 return [pinfo,fromyear,congress,journal,chapter,book,msc,dsc,mscNot,dscNot]

def printInfo(_info):
 zipped = zip(*_info)

 countCongress = 0
 congress = zipped[2]
 for item in congress:
  countCongress = countCongress + len(item)

 countJournal = 0
 journal = zipped[3]

 journal = removeDuplicates(journal)

 A1=0; A2=0; B1=0; B2=0; B3=0; B4=0; B5=0; C=0;
 for item in journal:
  countJournal = countJournal + len(item)
  for j in item:
   A1 = A1 + j[4].count("A1")
   A2 = A2 + j[4].count("A2")
   B1 = B1 + j[4].count("B1")
   B2 = B2 + j[4].count("B2")
   B3 = B3 + j[4].count("B3")
   B4 = B4 + j[4].count("B4")
   B5 = B5 + j[4].count("B5")
   C  = C  + j[4].count("C ")

 chapter = zipped[4]
 countChapter = 0
 for item in chapter:
  countChapter = countChapter + len(item)

 book = zipped[5]
 countBook = 0
 for item in book:
  countBook = countBook + len(item)

 msc = zipped[6]
 countMsc = 0
 for item in msc:
  countmsc = countMsc + len(item)

 dsc = zipped[7]
 countDsc = 0
 for item in dsc:
  countDsc = countDsc + len(item)

 mscNot = zipped[8]
 countMscNot = 0
 for item in mscNot:
  countMscNot = countMscNot + len(item)

 dscNot = zipped[9]
 countDscNot = 0
 for item in dscNot:
  countDscNot = countDscNot + len(item)

 now = datetime.datetime.now()
 print ''
 print 'RELATORIO DE:'
 for item in zipped[0]:
  print '              ' + item
 print ''
 print 'PROGRAMA:', sys.argv[1]
 print 'PERIODO ANALISADO: ' + str(int(zipped[1][0])) + \
       ' -- ' + str(now.month) + '/' + str(now.year)
 print ''
 print ' - total de publicacoes em congresso: ',countCongress
 print ' - total de artigos em journal: ',countJournal
 print '   - A1: ',A1
 print '   - A2: ',A2
 print '   - B1: ',B1
 print '   - B2: ',B2
 print '   - B3: ',B3
 print '   - B4: ',B4
 print '   - B5: ',B5
 print '   - C: ',C
 print ' - total de capitulos publicados: ',countChapter
 print ' - total de livros publicados: ',countBook
 print ' - total de dissertacoes de MSc: ',countMsc
 print ' - total de teses de DSc: ',countDsc
 print ' - total de dissertacoes de MSc em andamento: ',countMscNot
 print ' - total de teses de DSc em andamento: ',countDscNot
 print ''

### Remove duplicates from a list 
def removeDuplicates(_tupleList):
 # flat list: turn a list of list into list
 flatlist = [item for sublist in list(_tupleList) for item in sublist]
 # make it tuple again
 tupList = tuple(flatlist)
 b_set = set(map(tuple,tupList)) 
 # back to list
 return [map(list,b_set)]

def all():

 # retrieve lattes files
 lattes = []
 filePath = os.getcwd() + '/' + sys.argv[1] + '/'
 for file in glob.glob(filePath + '/*.xml'):
  base = os.path.basename(file)
  name = os.path.splitext(base)[0]
  lattes.append(name)

 fromyear = sys.argv[2]
 sumInfo = [retrieveInfo(sys.argv[1],lattes[0],fromyear)]
 print 'Analizando Lattes de',lattes[0]
 for name in lattes[1:]:
  info = retrieveInfo(sys.argv[1],name,fromyear)
  sumInfo = sumInfo + [info]
  print 'Analizando Lattes de',name

 printInfo(sumInfo)

def single(_program,_name,_fromyear):

 filename = os.getcwd()+'/'+_program+'/'+_name+'.xml'
 if os.path.isfile(filename):
  print 'Analizando Lattes de',_name
  # retrieve lattes files
  info = [retrieveInfo(_program,_name,_fromyear)]
 else:
  print ''
  print 'Check scientist and program name!'
  print ''
  return None

 printInfo(info)

def main():
 if len(sys.argv) < 3:
  print 'Requires program name, scientist name and starting date!'
  print 'Ex. python report.py program name_of_scientist 2012'
  print 'Ex. python report.py program 2012'
  print ''
  sys.exit()

 try:
  single(sys.argv[1],sys.argv[2],sys.argv[3])
 except:
  all()

if __name__ == "__main__":
 main()

