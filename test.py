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

        assert result == golden.out['output1']


@pytest.mark.golden_test('tests/*.yml')
def test_golden2(golden, caplog):
    with tempfile.TemporaryDirectory() as tmp_dir:
        import compiler
        import procrssor_interface
        import cu

        output_file: str = os.path.join(tmp_dir, 'compiled.bin')
        input_file: str = os.path.join(tmp_dir, 'input')
        result_file: str = os.path.join(tmp_dir, 'result')
        compiler.compile(golden['input_file'], output_file)

        if golden['input_data'] is not None:
            control_unit: cu.ControlUnit = cu.ControlUnit()

            procrssor_interface.load_program(output_file, control_unit)

            nums: list = str(golden['input_data']).split(',')
            for num in nums:
                procrssor_interface.add_input(int(num, 0), control_unit)

            trace, ticks = control_unit.work()

            result = [control_unit.proc.output_queue, ticks, trace]
        else:
            control_unit: cu.ControlUnit = cu.ControlUnit()

            procrssor_interface.load_program(output_file, control_unit)

            trace, ticks = control_unit.work()

            result = [control_unit.proc.output_queue, ticks, trace]

        assert result == golden.out['output2']
