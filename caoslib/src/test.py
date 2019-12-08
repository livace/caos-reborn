from utils.constants import CAOS_DIR, COMPILATION_STRING

from clint.textui import puts, colored, indent
import os
import tempfile


def test(args):
    task_path = get_task(args)
    tests_path = os.path.join(task_path, 'tests')

    tests = []
    try:
        tests = os.listdir(tests_path)
    except:
        puts(colored.red(f"Path {tests_path} doesn't exist."))
        exit(0)

    tests = filter(lambda x: os.path.splitext(x)[1] == '.dat', tests)
    tests = list(map(lambda x: os.path.splitext(x)[0], tests))
    if not tests:
        puts(colored.red(f"No tests found at {tests_path}"))
        exit(0)
    with tempfile.TemporaryDirectory() as temp_dir:
        executable_path = os.path.join(temp_dir, 'a.out')
        os.system(COMPILATION_STRING.format(os.path.join(task_path, 'main.c'), executable_path))
        if not os.path.exists(executable_path):
            puts(colored.red(f"Compilation error, aborted"))
            exit(0)

        for test in tests:
            run_test(task_path, test, executable_path)


def get_task_from_folder(folder):
    folder = os.path.abspath(folder)
    caos_dir = os.path.abspath(CAOS_DIR)
    if os.path.commonprefix([caos_dir, folder]) != caos_dir:
        return None
    tokens = os.path.relpath(folder, caos_dir).split(os.path.sep)
    if len(tokens) < 2:
        return None
    return os.path.join(CAOS_DIR, tokens[0], tokens[1])


def get_task_from_args(args):
    grouped = args.grouped
    if '-c' not in grouped or '-t' not in grouped or len(grouped['-c']) == 0 or len(grouped['-t']) == 0:
        return None
    return os.path.join(CAOS_DIR, grouped['-c'][0], grouped['-t'][0])


def get_task(args):
    task_path = get_task_from_args(args) or get_task_from_folder(os.getcwd())
    if not task_path:
        puts(colored.red("Provide both -c and -t flags or switch to task directory for testing."))
        exit(0)
    return task_path


def run_test(task_path, test, executable_path):
    input_path = os.path.join(task_path, 'tests', test + '.dat')
    output_path = os.path.join(task_path, 'tests', test + '.ans')

    if not os.path.exists(output_path):
        puts(colored.yellow(f"No matching output for test {input_path}"))
        puts(colored.yellow(f"{output_path} doesn't exits. Skip it."))
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        result_path = os.path.join(temp_dir, 'res')

        os.system('{} < {} > {}'.format(executable_path, input_path, result_path))

        with open(output_path, 'r') as output_file:
            with open(result_path, 'r') as temp_file:
                expected_lines = output_file.readlines()
                resulting_lines = temp_file.readlines()

                if expected_lines == resulting_lines:
                    puts(colored.green(f"Test {test}: OK!"))
                else:
                    puts(colored.red(f"Test {test}: Failed!"))
                    find_diff(expected_lines, resulting_lines)
                    saved_output_path = os.path.join(task_path, 'tests', test + '.res')
                    os.rename(result_path, saved_output_path)
                    puts(colored.red(f"Resulting output saved to '{saved_output_path}' file."))
                    exit(0)


def find_diff(expected_lines, resulting_lines):
    if (len(expected_lines) != len(resulting_lines)):
        print("Expected and resulting files have different number of lines")
        return

    count = 0
    for (line, (expected, resulting)) in enumerate(zip(expected_lines, resulting_lines)):
        if expected != resulting:
            with indent(quote=f'  Line #{line + 1} > '):
                puts(colored.blue(f"Expected:  {expected}"), newline=False)
                puts(colored.yellow(f"Resulting: {resulting}"))
            count += 1

        if count == 10:
            break
