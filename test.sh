#!/bin/bash

for f in ./testcase/test_data/*.lsp
do
    filename=$(basename -s .lsp $f) # lsp filename without extension
    ans="${f%.*}.ans"               # /path/to/lsp.ans

    # generate answers if not present
    if [[ ! -f $ans ]]; then
        ./smli/smli < $f &> $ans
    fi

    DIFF=$(python -u ./mlisp.py < $f |& diff -y --width=80 --suppress-common-lines $ans -)

    if [[ -z "$DIFF" ]]; then
        echo "Test $filename passed"
    else
        echo "Test $filename failed"
        echo "$DIFF"
    fi
done
