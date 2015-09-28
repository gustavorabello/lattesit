#!/bin/bash

for i in *.xml; do
 xmllint --format --recover $i > .tmp.xml
 mv .tmp.xml $i
done;

# $Id: $


