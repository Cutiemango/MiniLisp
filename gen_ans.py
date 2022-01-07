import os
from pathlib import Path


def filename_without_extension(filename):
    return os.path.splitext(filename)


base_dir = Path("./testcase/test_data")
testcases = os.listdir(base_dir)
for testcase in testcases:
    with open(base_dir / testcase, "r", encoding="utf-8") as file:
        ans_path = base_dir / f"{filename_without_extension(testcase)[0]}.ans"
        os.system(f"./smli/smli < {base_dir / testcase} > {ans_path}")
