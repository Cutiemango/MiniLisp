import os
import sys
import mlisp
from pathlib import Path


def filename_without_extension(file):
    return os.path.splitext(file)


base_dir = Path("./testcase/test_data")
testcases = [file for file in os.listdir(base_dir) if file.endswith('.lsp')]

for testcase in testcases:
    filename = filename_without_extension(testcase)[0]
    with open(base_dir / testcase, "r", encoding="utf-8") as file:
        input_str = "".join([line.strip() for line in file.readlines()])
        out_path = base_dir / f"{filename}.out"
        sys.stdout = open(out_path, "w")
        try:
            mlisp.run_interpreter(input_str)
        except Exception as err:
            print(err)

sys.stdout = sys.__stdout__

for testcase in testcases:
    filename = filename_without_extension(testcase)[0]
    ans_path = base_dir / f"{filename}.ans"
    out_path = base_dir / f"{filename}.out"
    print(f"Testcase {filename}:")
    os.system(f"diff {ans_path} {out_path}")

