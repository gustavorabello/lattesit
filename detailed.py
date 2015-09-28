## =================================================================== ##
#  this is file detailes.py, created at 25-Set-2015                     #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

import xml.etree.ElementTree as ET
import datetime
import csv
import sys
import ppgem_lattes as pg

def main():
 if len(sys.argv) < 3:
  print 'Requires name of scientist and starting date!'
  print 'Ex. python ppgem-lattes.py name_of_scientist 2012'
  print ''
  sys.exit()

 fromyear = float(sys.argv[2])
 area = 'ENGENHARIAS III'

 print ''
 print ''

 filePath = '/Users/gustavo/Desktop/ppgem/'
 xmlFile = filePath + 'lattes/' + str(sys.argv[1]) + '.xml'
 csvFile = filePath + 'qualis/' + 'Consulta_Webqualis' + '.csv'
 tree = ET.parse(xmlFile)

 pinfo = pg.personalInfo(tree)
 print 75*'*'
 print pinfo
 print 75*'*'
 print ''

 # [important,congress,journal,chapter,book]
 binfo = pg.technicalProduction(tree,csvFile,area,fromyear)
 important = binfo[0] 
 congress = binfo[1]
 journal = binfo[2]
 chapter = binfo[3]
 book = binfo[4]

 # [kind.tag,title,event,year]
 if len(congress) > 0:
  print congress[0][0]
  print 75*'-'
  for info in congress:
   print info[1], info[3]
  print ''

 # [kind.tag,journaltitle,year,row[2]
 if len(journal) > 0:
  print journal[0][0]
  print 75*'-'
  for info in journal:
   print info[3],info[2],info[1]
  print ''

 # [kind.tag,title,year]
 if len(chapter) > 0:
  print chapter[0][0]
  print 75*'-'
  for info in chapter:
   print info[1],info[2]
  print ''

 # [kind.tag,title,year]
 if len(book) > 0:
  print book[0][0]
  print 75*'-'
  for info in book:
   print info[1],info[2]
  print ''

 tinfo = pg.thesisConcluded(tree,fromyear)
 if tinfo:
  msc = tinfo[0] 
  dsc = tinfo[1] 

  # [info.tag,year,title,principal,agency]
  if len(msc) > 0:
   print msc[0][0]
   print 75*'-'
   for info in msc:
    print 'MSc',info[1],info[2]
   print ''

  # [info.tag,year,title,principal,agency]
  if len(dsc) > 0:
   print dsc[0][0]
   print 75*'-'
   for info in dsc:
    print 'DSc',info[1],info[2]
   print ''

 cinfo = pg.thesisNotConcluded(tree,fromyear)
 mscNot = cinfo[0] 
 dscNot = cinfo[1] 

 # [info.tag,year,title,principal,agency]
 if len(mscNot) > 0:
  print mscNot[0][0]
  print 75*'-'
  for info in mscNot:
   print 'MSc',info[1],info[2]
  print ''

 # [info.tag,year,title,principal,agency]
 if len(dscNot) > 0:
  print dscNot[0][0]
  print 75*'-'
  for info in dscNot:
   print 'DSc',info[1],info[2]
  print ''

 now = datetime.datetime.now()
 print ''
 print 'RELATORIO DO PESQUISADOR ',pinfo
 print 'PERIODO ANALISADO: ' + str(int(fromyear)) + \
       ' -- ' + str(now.month) + '/' + str(now.year)
 print ''
 if binfo:
  print ' - total de publicacoes em congresso: ',len(congress)
  print ' - total de artigos em journal: ',len(journal)
  print ' - total de capitulos publicados: ',len(chapter)
  print ' - total de livros publicados: ',len(book)
 if tinfo:
  print ' - total de dissertacoes de MSc: ',len(msc)
  print ' - total de teses de DSc: ',len(dsc)
 if cinfo:
  print ' - total de dissertacoes de MSc em andamento: ',len(mscNot)
  print ' - total de teses de DSc em andamento: ',len(dscNot)
 print ''

if __name__ == "__main__":
 main()

