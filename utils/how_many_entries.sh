
#!/bin/bash

cut -f 1 $1 | sort - | uniq - | wc -l
