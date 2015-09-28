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
 A1=0; A2=0; B1=0; B2=0; B3=0; B4=0; B5=0; C=0;
 for j in journal:
  A1 = A1 + j.count("A1")
  A2 = A2 + j.count("A2")
  B1 = B1 + j.count("B1")
  B2 = B2 + j.count("B2")
  B3 = B3 + j.count("B3")
  B4 = B4 + j.count("B4")
  B5 = B5 + j.count("B5")
  C = C + j.count("C ")

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

 return [pinfo,fromyear,len(congress), len(journal),A1,A2,B1,B2,B3,B4,B5,C,len(chapter), len(book), len(msc), len(dsc), len(mscNot), len(dscNot)]

def printInfo(_info):
 now = datetime.datetime.now()
 print ''
 print 'RELATORIO DO ', _info[0]
 print 'PERIODO ANALISADO: ' + str(int(_info[1])) + \
       ' -- ' + str(now.month) + '/' + str(now.year)
 print ''
 print ' - total de publicacoes em congresso: ',_info[2]
 print ' - total de artigos em journal: ',_info[3]
 print '   - A1: ',_info[4]
 print '   - A2: ',_info[5]
 print '   - B1: ',_info[6]
 print '   - B2: ',_info[7]
 print '   - B3: ',_info[8]
 print '   - B4: ',_info[9]
 print '   - B5: ',_info[10]
 print '   - C: ',_info[11]
 print ' - total de capitulos publicados: ',_info[12]
 print ' - total de livros publicados: ',_info[13]
 print ' - total de dissertacoes de MSc: ',_info[14]
 print ' - total de teses de DSc: ',_info[15]
 print ' - total de dissertacoes de MSc em andamento: ',_info[16]
 print ' - total de teses de DSc em andamento: ',_info[17]
 print ''

def all():

 # retrieve lattes files
 lattes = []
 filePath = os.getcwd() + '/' + sys.argv[1] + '/'
 for file in glob.glob(filePath + '/*.xml'):
  base = os.path.basename(file)
  name = os.path.splitext(base)[0]
  lattes.append(name)

 lists = [0]*16
 sumInfo = []
 for name in lattes:
  fromyear = sys.argv[2]
  info = retrieveInfo(sys.argv[1],name,fromyear)
  print 'Analizing Lattes of',name
  lists = [sum(x) for x in zip(lists,info[2:])]

 printInfo([sys.argv[1]]+[fromyear]+lists)

def single(_program,_name,_fromyear):

 filename = os.getcwd()+'/'+_program+'/'+_name+'.xml'
 if os.path.isfile(filename):
  print 'Analizing Lattes of',_name
  # retrieve lattes files
  info = retrieveInfo(_program,_name,_fromyear)
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

