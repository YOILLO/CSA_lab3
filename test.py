import os.path
import tempfile
import pytest
import subprocess


@pytest.mark.golden_test('tests/*.yml')
def test_golden(golden, caplog):
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file: str = os.path.join(tmp_dir, 'compiled.bin')
        input_file: str = os.path.join(tmp_dir, 'input')
        result_file: str = os.path.join(tmp_dir, 'result')
        subprocess.call(["python", "./compiler.py", golden['input_file'], output_file])
        if golden['input_data'] is not None:
            nums: list = str(golden['input_data']).split(',')
            with open(input_file, 'w') as f:
                for num in nums:
                    f.write(num + "\n")

            subprocess.call(["python", "./procrssor_interface.py", output_file, result_file, '-i', input_file])
        else:
            subprocess.call(["python", "./procrssor_interface.py", output_file, result_file])

        with open(result_file, 'r') as f:
            result = f.readlines()

        assert result == golden.out['output']
