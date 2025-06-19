#!/bin/bash

### convert gene accessions from argv1 using argv2 reference annotations in tabular format ###

cat $1 | while read l; do echo "$l" > 1; cut -f 2 1 | grep -w -f 1 $1 > 2; paste 1 2 > 3; cat 3 >> 4; done
