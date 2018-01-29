## =================================================================== ##
#  this is file ppgem-lattes.py, created at 22-Set-2015                 #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

## =================================================================== ##
# Print the academic publication and its classification according to 
# WebQualis (CAPES) of an input scientist which Curriculum-Vitae 
# appears in the LATTES platform. 
# 
# OBS:
# 1) The WebQualis database may be download from the WebQualis webpage, 
# exporting the complete list of journals in EXCEL format and 
# thereafter saved as Microsoft CSV file format;
#
# 2) The scientist's lattes file may be download as XML file format 
# from the LATTES platform directly;
#
# 3) 'fromyear' is defined below and it stands for the starting year 
# of the publication list.
#
# 
# input: scientist file name 
# output: journal name and qualis classification
#
#
# REMARKS:
# This version outputs the qualis classification only for journal 
# publications.
## =================================================================== ##

import xml.etree.ElementTree as ET
import datetime
import csv
import sys

## ------------ ##
## Personal 
## ------------ ##
def personalInfo(_tree):
 info = _tree.find('DADOS-GERAIS')   # personal info

 name = info.attrib['NOME-COMPLETO']
 cite = info.attrib['NOME-EM-CITACOES-BIBLIOGRAFICAS']
 country = info.attrib['PAIS-DE-NASCIMENTO']

 for title in info[3]:
  # graduation
  if title.tag == 'GRADUACAO':
   gradTitle    = title.attrib['TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO']
   gradDirector = title.attrib['NOME-DO-ORIENTADOR']
   gradName     = title.attrib['NOME-INSTITUICAO']
   gradCourse   = title.attrib['NOME-CURSO']
   gradBegin    = title.attrib['ANO-DE-INICIO']
   gradEnd      = title.attrib['ANO-DE-CONCLUSAO']
 
  # msc
  if title.tag == 'MESTRADO':
   masterTitle    = title.attrib['TITULO-DA-DISSERTACAO-TESE']
   masterDirector = title.attrib['NOME-COMPLETO-DO-ORIENTADOR']
   masterName     = title.attrib['NOME-INSTITUICAO']
   masterCourse   = title.attrib['NOME-CURSO']
   masterBegin    = title.attrib['ANO-DE-INICIO']
   masterEnd      = title.attrib['ANO-DE-CONCLUSAO']
 
  # phd
  if title.tag == 'DOUTORADO':
   phdTitle    = title.attrib['TITULO-DA-DISSERTACAO-TESE']
   phdDirector = title.attrib['NOME-COMPLETO-DO-ORIENTADOR']
   phdName     = title.attrib['NOME-INSTITUICAO']
   phdCourse   = title.attrib['NOME-CURSO']
   phdBegin    = title.attrib['ANO-DE-INICIO']
   phdEnd      = title.attrib['ANO-DE-CONCLUSAO']

  # post-doc
  if title.tag == 'POS-DOUTORADO':
   posdocName  = title.attrib['NOME-INSTITUICAO']
   posdocBegin = title.attrib['ANO-DE-INICIO']
   posdocEnd   = title.attrib['ANO-DE-CONCLUSAO']

 return name

## ------------ ##
## Bibliography
## ------------ ##
def biblioProduction(_tree,_csvFile,_area,_fromyear):
 bib = _tree.find('PRODUCAO-BIBLIOGRAFICA')   # bibliography
 if bib == None:
  #print 'Este lattes nao tem producao bibliografica'
  return None

 important = []
 congress = []
 journal = []
 chapter = []
 book = []

 for kind in bib:
  # Congress papers
  if kind.tag == 'TRABALHOS-EM-EVENTOS':
   for info in kind:
    number = info.attrib['SEQUENCIA-PRODUCAO']
    title = info[0].attrib['TITULO-DO-TRABALHO']
    year = info[0].attrib['ANO-DO-TRABALHO']
    flag = info[0].attrib['FLAG-RELEVANCIA']
    doi = info[0].attrib['DOI']
    event = info[1].attrib['NOME-DO-EVENTO']
    city = info[1].attrib['CIDADE-DO-EVENTO']
    #addinfo = info[-1].attrib['DESCRICAO-INFORMACOES-ADICIONAIS']
    if flag == 'SIM':
     important.append([title,event,year])

    if float(year)/_fromyear>= 1.0:
    #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
     congress.append([kind.tag,title,event,year])

  # Journal papers
  if kind.tag == 'ARTIGOS-PUBLICADOS':
   for info in kind:
    number = info.attrib['SEQUENCIA-PRODUCAO']
    title = info[0].attrib['TITULO-DO-ARTIGO']
    year = info[0].attrib['ANO-DO-ARTIGO']
    flag = info[0].attrib['FLAG-RELEVANCIA']
    doi = info[0].attrib['DOI']
    journaltitle = info[1].attrib['TITULO-DO-PERIODICO-OU-REVISTA']
    issn = info[1].attrib['ISSN']
    issn = str(issn[:4]) + '-' + str(issn[4:])
    #addinfo = info[-1].attrib['DESCRICAO-INFORMACOES-ADICIONAIS']
    if flag == 'SIM':
     important.append([title,journaltitle,year])
    if float(year)/_fromyear >= 1.0:
     with open(_csvFile, 'rt') as f:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
       if row[0] in issn:
        journal.append([kind.tag,title,journaltitle,year,row[2]])

  # Book and book chapters
  if kind.tag == 'LIVROS-E-CAPITULOS':
   if kind[0].tag == 'CAPITULOS-DE-LIVROS-PUBLICADOS':
    for info in kind[0]:
     number = info.attrib['SEQUENCIA-PRODUCAO']
     title = info[0].attrib['TITULO-DO-CAPITULO-DO-LIVRO']
     year = info[0].attrib['ANO']
     flag = info[0].attrib['FLAG-RELEVANCIA']
     country = info[0].attrib['PAIS-DE-PUBLICACAO']
     publisher = info[1].attrib['NOME-DA-EDITORA']
     #addinfo = info[-1].attrib['DESCRICAO-INFORMACOES-ADICIONAIS']
     booktitle = info[1].attrib['TITULO-DO-LIVRO']
     if flag == 'SIM':
      important.append([title,booktitle,year])
 
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
      chapter.append([kind.tag,title,year])

   # Books
   if kind[0].tag == 'LIVROS-PUBLICADOS-OU-ORGANIZADOS':
    for info in kind[0]:
     number = info.attrib['SEQUENCIA-PRODUCAO']
     year = info[0].attrib['ANO']
     flag = info[0].attrib['FLAG-RELEVANCIA']
     country = info[0].attrib['PAIS-DE-PUBLICACAO']
     publisher = info[1].attrib['NOME-DA-EDITORA']
     booktitle = info[0].attrib['TITULO-DO-LIVRO']
     #addinfo = info[-1].attrib['DESCRICAO-INFORMACOES-ADICIONAIS']
     if flag == 'SIM':
      important.append([booktitle,country,year])
  
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
      book.append([kind[0].tag,booktitle,year])
 
 return [important,congress,journal,chapter,book]

## --------------------- ##
## PhD/MSc concluded
## --------------------- ##
def thesisConcluded(_tree,_fromyear):
 thesis = _tree.find('OUTRA-PRODUCAO')   
 if thesis == None:
  #print 'Este lattes nao tem orientacoes de mestrado/doutorado concluidas'
  return None

 msc = []
 dsc = []
 ic  = []

 for kind in thesis:
  if kind.tag == 'ORIENTACOES-CONCLUIDAS':
   for info in kind:

    # M.Sc. concluded
    if info.tag == 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO':
     title = info[0].attrib['TITULO']
     year = info[0].attrib['ANO']
     principal = info[1].attrib['TIPO-DE-ORIENTACAO']
     student = info[1].attrib['NOME-DO-ORIENTADO']
     scholarship = info[1].attrib['FLAG-BOLSA']
     agency = info[1].attrib['NOME-DA-AGENCIA']
   
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
      msc.append([info.tag,year,title,principal,agency])

    # D.Sc. concluded
    if info.tag == 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO':
     title = info[0].attrib['TITULO']
     year = info[0].attrib['ANO']
     principal = info[1].attrib['TIPO-DE-ORIENTACAO']
     student = info[1].attrib['NOME-DO-ORIENTADO']
     scholarship = info[1].attrib['FLAG-BOLSA']
     agency = info[1].attrib['NOME-DA-AGENCIA']
   
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
      dsc.append([info.tag,year,title,principal,agency])

    # IC concluded
    if info.tag == 'OUTRAS-ORIENTACOES-CONCLUIDAS':
     quality = info[0].attrib['NATUREZA']
     title = info[0].attrib['TITULO']
     year = info[0].attrib['ANO']
     student = info[1].attrib['NOME-DO-ORIENTADO']
     scholarship = info[1].attrib['FLAG-BOLSA']
     agency = info[1].attrib['NOME-DA-AGENCIA']
   
     if float(year)/_fromyear>= 1.0 and \
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013 and \
        quality == 'INICIACAO_CIENTIFICA':
        ic.append([info.tag,year,title,student])

 return [msc,dsc,ic]


def thesisNotConcluded(_tree,_fromyear):
 ## --------------------- ##
 ## PhD/MSc not concluded
 ## --------------------- ##
 thesis = _tree.find('DADOS-COMPLEMENTARES')   # bibliography
 if thesis == None:
  #print 'Este lattes nao tem orientacoes de mestrado/doutorado'
  return None

 msc = []
 dsc = []
 ic  = []
 
 for kind in thesis:
  if kind.tag == 'ORIENTACOES-EM-ANDAMENTO':
   for info in kind:
 
    # M.Sc. not concluded
    if info.tag == 'ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO':
     title = info[0].attrib['TITULO-DO-TRABALHO']
     year = info[0].attrib['ANO']
     principal = info[1].attrib['TIPO-DE-ORIENTACAO']
     student = info[1].attrib['NOME-DO-ORIENTANDO']
     scholarship = info[1].attrib['FLAG-BOLSA']
     agency = info[1].attrib['NOME-DA-AGENCIA']
    
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
      msc.append([info.tag,year,title,principal,agency])
 
    # D.Sc. not concluded
    if info.tag == 'ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO':
     title = info[0].attrib['TITULO-DO-TRABALHO']
     year = info[0].attrib['ANO']
     principal = info[1].attrib['TIPO-DE-ORIENTACAO']
     student = info[1].attrib['NOME-DO-ORIENTANDO']
     scholarship = info[1].attrib['FLAG-BOLSA']
     agency = info[1].attrib['NOME-DA-AGENCIA']
   
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
      dsc.append([info.tag,year,title,principal,agency])

    # IC not concluded
    if info.tag == 'ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA':
     title = info[0].attrib['TITULO-DO-TRABALHO']
     year = info[0].attrib['ANO']
     student = info[1].attrib['NOME-DO-ORIENTANDO']
     scholarship = info[1].attrib['FLAG-BOLSA']
     agency = info[1].attrib['NOME-DA-AGENCIA']
   
     if float(year)/_fromyear>= 1.0:
     #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
        ic.append([info.tag,year,title,student])

 return [msc,dsc,ic]

## -------------------- ##
## Technical Production
## -------------------- ##
def technicalProduction(_tree,_fromyear):
 tech = _tree.find('PRODUCAO-TECNICA')   # Technical
 if tech == None:
  #print 'Este lattes nao tem producao tecnica'
  return None

 important = []
 patent = []

 for kind in tech:
  # Patents
  if kind.tag == 'PATENTE':
   title = kind[0].attrib['TITULO']
   year = kind[0].attrib['ANO-DESENVOLVIMENTO']
   flag = kind[0].attrib['FLAG-RELEVANCIA']
   if flag == 'SIM':
    important.append([title,year])
   if float(year)/_fromyear>= 1.0:
   #if float(year)/_fromyear>= 1.0 and float(year)/_fromyear<1.0013:
    patent.append([kind.tag,title,year])

 return [patent]
