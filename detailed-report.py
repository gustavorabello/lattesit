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
 #csvFile = os.getcwd() + '/qualis/' + 'Consulta_Webqualis' + '.csv'
 csvFile = os.getcwd() + '/qualis/' + \
 'classificacoes_publicadas_engenharias_iii_2017' + '.csv'
 tree = ET.parse(xmlFile)

 pinfo = lt.personalInfo(tree)

 # [important,congress,journal,chapter,book]
 binfo = lt.biblioProduction(tree,csvFile,area,fromyear)
 important = binfo[0] 
 congress = binfo[1]
 journal = binfo[2]
 chapter = binfo[3]
 book = binfo[4]

 tinfo = lt.thesisConcluded(tree,fromyear)
 msc = []
 dsc = []
 ic  = []
 if tinfo:
  msc = tinfo[0] 
  dsc = tinfo[1] 
  ic  = tinfo[2]

 cinfo = lt.thesisNotConcluded(tree,fromyear)
 mscNot = []
 dscNot = []
 icNot  = []
 mscNot = cinfo[0] 
 dscNot = cinfo[1] 
 icNot = cinfo[2] 

 techinfo = lt.technicalProduction(tree,fromyear)
 patent = []
 if techinfo:
  patent = techinfo[0] 

 return [pinfo,fromyear,congress,journal,chapter,book,msc,dsc,ic,mscNot,dscNot,icNot,patent]

def countInfo(_info):
 zipped = zip(*_info)

 countCongress = 0
 congress = zipped[2]
 for item in congress:
  countCongress = countCongress + len(item)

 countJournal = 0
 journal = zipped[3]

 #journal = removeDuplicates(journal)

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
  countMsc = countMsc + len(item)

 dsc = zipped[7]
 countDsc = 0
 for item in dsc:
  countDsc = countDsc + len(item)

 ic = zipped[8]
 countIc= 0
 for item in ic:
  countIc = countIc + len(item)

 mscNot = zipped[9]
 countMscNot = 0
 for item in mscNot:
  countMscNot = countMscNot + len(item)

 dscNot = zipped[10]
 countDscNot = 0
 for item in dscNot:
  countDscNot = countDscNot + len(item)

 icNot = zipped[11]
 countIcNot = 0
 for item in icNot:
  countIcNot = countIcNot + len(item)

 patent = zipped[12]
 countPatent = 0
 for item in patent:
  countPatent = countPatent + len(item)

 # name,program,fromyear,congress,journal,A1,A2,B1,B2,B3,B4,B5,C,chapter,book,ic,msc,dsc,icNot,mscNot,dscNot,patent]
 return [zipped[0],sys.argv[1],str(int(zipped[1][0])),countCongress, countJournal, A1, A2, B1, B2, B3, B4, B5, C, countChapter, countBook, countIc, countMsc, countDsc, countIcNot, countMscNot, countDscNot, countPatent]

def printInfo(_info):
 item = countInfo(_info)

 now = datetime.datetime.now()
 print ('')
 print ('RELATORIO DE:')
 for it in item[0]:
  print ('              ' + it)
 print ('')
 print ('PROGRAMA:', item[1])
 print ('PERIODO ANALISADO: ' + item[2] + \
       ' -- ' + str(now.month) + '/' + str(now.year))
 print ('')
 print (' - total de publicacoes em congresso: ',item[3])
 print (' - total de artigos em journal: ',item[4])
 print ('   - A1: ',item[5])
 print ('   - A2: ',item[6])
 print ('   - B1: ',item[7])
 print ('   - B2: ',item[8])
 print ('   - B3: ',item[9])
 print ('   - B4: ',item[10])
 print ('   - B5: ',item[11])
 print ('   - C: ',item[12])
 print (' - total de capitulos publicados: ',item[13])
 print (' - total de livros publicados: ',item[14])
 print (' - total de IC: ',item[15])
 print (' - total de dissertacoes de MSc: ',item[16])
 print (' - total de teses de DSc: ',item[17])
 print (' - total de IC em andamento: ',item[18])
 print (' - total de dissertacoes de MSc em andamento: ',item[19])
 print (' - total de teses de DSc em andamento: ',item[20])
 print (' - total de patentes: ',item[21])
 print ('')

def csvInfo(_info):
 item = countInfo(_info)
 
 now = datetime.datetime.now()
 filename = "output.csv"
 text_file = []
 if os.path.isfile(filename):
  text_file = open(filename, "a")
 else:
  text_file = open(filename, "w")
  header = ' ,'
  header = header + 'Periodicos Indexados Qualis A1, '
  header = header + 'Periodicos Indexados Qualis A2, '
  header = header + 'Periodicos Indexados Qualis B1, '
  header = header + 'Periodicos Indexados Qualis B2, '
  header = header + 'Periodicos Indexados Qualis B3, '
  header = header + 'Periodicos Indexados Qualis B4, '
  header = header + 'Periodicos Indexados Qualis B5, '
  header = header + 'Periodicos Indexados Qualis C, '
  header = header + 'Total em Periodicos, '
  header = header + 'Capitulos, '
  header = header + 'Livros, '
  header = header + 'Patentes Depositadas ou Concedidas, '
  header = header + 'Alunos de IC, '
  header = header + 'Orientacao de Mestres Concluida, '
  header = header + 'Orientacao de Mestres em Andamento, '
  header = header + 'Orientacao de Doutores Concluida, '
  header = header + 'Orientacao de Doutores em Andamento, '
  header = header + 'Artigos em congressos, '
  header = header + 'Equacao 1, '
  header = header + 'Equacao 2 \n'
  text_file.write(header)

 string = (''.join(item[0])).encode('latin-1') + ',  ' # name
 string = string + str(item[5]) + ',  ' # A1
 string = string + str(item[6]) + ',  ' # A2
 string = string + str(item[7]) + ',  ' # B1
 string = string + str(item[8]) + ',  ' # B2
 string = string + str(item[9]) + ',  ' # B3
 string = string + str(item[10]) + ',  ' # B4
 string = string + str(item[11]) + ',  ' # B5
 string = string + str(item[12]) + ',  ' # C
 string = string + str(item[8]+item[7]+item[6]+item[5]+item[9]+item[10]+item[11]+item[12]) + ',  ' # B2
 string = string + str(item[13]) + ',  ' # chapter
 string = string + str(item[14]) + ',  ' # book
 string = string + str(item[21]) + ',  ' # patent
 string = string + str(item[15]+item[18]) + ',  ' # ic
 string = string + str(item[16]) + ',  ' # msc
 string = string + str(item[19]) + ',  ' # msc
 string = string + str(item[17]) + ',  ' # dsc
 string = string + str(item[20]) + ',  ' # dsc
 string = string + str(item[3]) + ',  ' # congress
 eq1 = 1.00*item[5] + 0.75*item[6] + \
       0.75*item[7] + 0.50*item[8] + \
       0.30*item[9]
 string = string + str(eq1) + ',  ' # eq1 
 eq2 = 1.00*item[5] + 0.75*item[6] + \
       0.75*item[7] + 0.50*item[8] + \
       0.30*item[9]
 string = string + str(eq2) + '\n' # eq2
 text_file.write(string)
 text_file.close()

### Remove duplicates from a list 
def removeDuplicates(_tupleList):
 # flat list: turn a list of list into list
 flatlist = [item for sublist in list(_tupleList) for item in sublist]
 # make it tuple again
 tupList = tuple(flatlist)
 b_set = set(map(tuple,tupList)) 
 # back to list
 return [map(list,b_set)]

def allprint ():

 # retrieve lattes files
 lattes = []
 filePath = os.getcwd() + '/' + sys.argv[1] + '/'
 for file in glob.glob(filePath + '/*.xml'):
  base = os.path.basename(file)
  name = os.path.splitext(base)[0]
  lattes.append(name)

 fromyear = sys.argv[2]
 sumInfo = [retrieveInfo(sys.argv[1],lattes[0],fromyear)]
 print ('Analizando Lattes de',lattes[0])
 for name in lattes[1:]:
  info = retrieveInfo(sys.argv[1],name,fromyear)
  sumInfo = sumInfo + [info]
  print ('Analizando Lattes de',name)

 printInfo(sumInfo)

def allSave():

 # retrieve lattes files
 lattes = []
 filePath = os.getcwd() + '/' + sys.argv[1] + '/'
 for file in glob.glob(filePath + '/*.xml'):
  base = os.path.basename(file)
  name = os.path.splitext(base)[0]
  lattes.append(name)

 fromyear = sys.argv[2]
 for name in lattes:
  info = retrieveInfo(sys.argv[1],name,fromyear)
  print ('Analizando Lattes de',name)
  #printInfo([info])
  csvInfo([info])

def singleprint (_program,_name,_fromyear):

 filename = os.getcwd()+'/'+_program+'/'+_name+'.xml'
 if os.path.isfile(filename):
  print ('Analizando Lattes de' + _name)
  # retrieve lattes files
  info = [retrieveInfo(_program,_name,_fromyear)]
 else:
  print ('')
  print ('Check scientist and program name!')
  print ('')
  return None

 printInfo(info)
 csvInfo([info])

def main():
 if len(sys.argv) < 3:
  print ('Requires program name, scientist name and starting date!')
  print ('Ex. python report.py program name_of_scientist 2012')
  print ('Ex. python report.py program 2012')
  print ('')
  sys.exit()

 else:
  #allprint ()
  allSave()

if __name__ == "__main__":
 main()

