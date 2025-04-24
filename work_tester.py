def run_source(source_path, timeout_sec=5, input_file="input.txt", output_file="actual.txt"):
    import subprocess, pathlib, os

    path = pathlib.Path(source_path)
    ext = path.suffix
    base_name = path.stem
    exec_file = f"{base_name}.out"

    try:
        if ext == ".c":
            compile_cmd = ["gcc", source_path, "-o", exec_file]
            run_cmd = [f"./{exec_file}"]
        elif ext == ".cpp":
            compile_cmd = ["g++", source_path, "-o", exec_file]
            run_cmd = [f"./{exec_file}"]
        elif ext == ".java":
            compile_cmd = ["javac", source_path]
            run_cmd = ["java", base_name]
        elif ext == ".py":
            compile_cmd = None
            run_cmd = ["python3", source_path]
        else:
            return {"成功": False, "エラー": "不明なファイル形式です"}

        if compile_cmd:
            result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                return {"成功": False, "エラー": f"コンパイルエラー:\n{result.stderr}"}

        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            result = subprocess.run(run_cmd, stdin=infile, stdout=outfile, stderr=subprocess.PIPE, text=True, timeout=timeout_sec)

        if result.returncode != 0:
            return {"成功": False, "エラー": f"実行時エラー:\n{result.stderr}"}

        return {"成功": True, "出力ファイル": output_file, "実行ファイル": exec_file}

    except subprocess.TimeoutExpired:
        return {"成功": False, "エラー": f"タイムアウト（{timeout_sec}秒を超えました）"}

    # 実行ファイルは check() で削除するのでここでは削除しない

def check_output(actual_output_file="actual.txt", expected_output_file="output.txt", exec_file_to_cleanup=None):
    import os

    try:
        with open(actual_output_file, "r") as actual_f:
            actual_output = actual_f.read().strip()
        with open(expected_output_file, "r") as expected_f:
            expected_output = expected_f.read().strip()
    except FileNotFoundError:
        return {
            "判定": False,
            "実行結果": None,
            "期待出力": None,
            "エラー": "出力ファイルまたは期待ファイルが見つかりません"
        }

    result = actual_output == expected_output

    # ファイル削除（clean up）
    if os.path.exists(actual_output_file):
        os.remove(actual_output_file)
    if exec_file_to_cleanup and os.path.exists(exec_file_to_cleanup):
        os.remove(exec_file_to_cleanup)
    if os.path.exists("*.class"):  # Javaのクリーンアップ（雑に全部消す想定）
        for f in os.listdir():
            if f.endswith(".class"):
                os.remove(f)

    return {
        "判定": result,
        "実行結果": actual_output,
        "期待出力": expected_output,
        "エラー": None
    }

def run_all_tests(source_file, testcase_dir="testcase"):
    import glob
    import re

    input_files = sorted(glob.glob(f"{testcase_dir}/input*.txt"))
    print(input_files)
    results = []

    for input_path in input_files:
        # ファイル名から数字だけを抽出（例：input3.txt → 3）
        test_id_match = re.search(r"input(\d+)\.txt", input_path)
        if not test_id_match:
            continue
        test_id = test_id_match.group(1)

        expected_path = f"{testcase_dir}/output{test_id}.txt"
        actual_path   = f"{testcase_dir}/actual{test_id}.txt"

        run_result = run_source(source_file, input_file=input_path, output_file=actual_path)

        if not run_result["成功"]:
            results.append({
                "ケース": test_id,
                "成功": False,
                "エラー": run_result["エラー"]
            })
            continue

        check_result = check_output(actual_path, expected_output_file=expected_path, exec_file_to_cleanup=run_result.get("実行ファイル"))

        results.append({
            "ケース": test_id,
            "成功": True,
            "判定": check_result["判定"],
            "実行結果": check_result["実行結果"],
            "期待出力": check_result["期待出力"]
        })

    return results



results = run_all_tests("main.c")

for r in results:
    print(f"[ケース {r['ケース']}]")
    if not r["成功"]:
        print(f"  エラー: {r['エラー']}")
    else:
        print(f"  判定: {'True' if r['判定'] else 'False'}")
        if not r["判定"]:
            print(f"  実行結果:\n{r['実行結果']}")
            print(f"  期待出力:\n{r['期待出力']}")
    print()

