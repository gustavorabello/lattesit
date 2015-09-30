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

 congress = 0
 for person in zipped[2]:
  congress = congress + len(person)/4

 journal = 0
 ## flat list: turn a list of list into list
 jour = [item for sublist in list(zipped[3]) for item in sublist]

 ## Remove duplicates from a list 
 # make it tuple again
 tjour = tuple(jour)
 b_set = set(map(tuple,tjour)) 
 jour = map(list,b_set)

 A1=0; A2=0; B1=0; B2=0; B3=0; B4=0; B5=0; C=0;
 for person in jour:
  journal = journal + len(person)/5
  for j in person:
   A1 = A1 + j.count("A1")
   A2 = A2 + j.count("A2")
   B1 = B1 + j.count("B1")
   B2 = B2 + j.count("B2")
   B3 = B3 + j.count("B3")
   B4 = B4 + j.count("B4")
   B5 = B5 + j.count("B5")
   C  = C  + j.count("C ")

 chapter = 0
 for person in zipped[4]:
  chapter = chapter + len(person)

 book = 0
 for person in zipped[5]:
  book = book + len(person)

 msc = 0
 for person in zipped[6]:
  msc = msc + len(person)

 dsc = 0
 for person in zipped[7]:
  dsc = dsc + len(person)

 mscNot = 0
 for person in zipped[8]:
  mscNot = mscNot + len(person)

 dscNot = 0
 for person in zipped[9]:
  dscNot = dscNot + len(person)

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
 print ' - total de publicacoes em congresso: ',congress
 print ' - total de artigos em journal: ',journal
 print '   - A1: ',A1
 print '   - A2: ',A2
 print '   - B1: ',B1
 print '   - B2: ',B2
 print '   - B3: ',B3
 print '   - B4: ',B4
 print '   - B5: ',B5
 print '   - C: ',C
 print ' - total de capitulos publicados: ',chapter
 print ' - total de livros publicados: ',book
 print ' - total de dissertacoes de MSc: ',msc
 print ' - total de teses de DSc: ',dsc
 print ' - total de dissertacoes de MSc em andamento: ',mscNot
 print ' - total de teses de DSc em andamento: ',dscNot
 print ''

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

