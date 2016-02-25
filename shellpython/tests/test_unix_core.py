import unittest
import os

from shellpython import core


class StreamMock:

    def __init__(self):
        self.lines = []

    def mocked_print(self, text):
        self.lines.append(text)


class TestExecute(unittest.TestCase):

    def setUp(self):
        self.stdout_mock = StreamMock()
        self.stderr_mock = StreamMock()
        core._print_stdout = self.stdout_mock.mocked_print
        core._print_stderr = self.stderr_mock.mocked_print

    def test_simple_echo_success(self):
        result = core._create_result('echo 1', '')
        self.assertEqual(result.returncode, 0)

        self.assertEqual(result.stdout, '1')
        self.assertEqual(len(result.stdout_lines), 1)
        self.assertEqual(result.stdout_lines[0], '1')

        self.assertEqual(result.stderr, '')
        self.assertEqual(len(result.stderr_lines), 0)

        self.assertEqual(len(self.stdout_mock.lines), 0)
        self.assertEqual(len(self.stderr_mock.lines), 0)

    def test_simple_echo_failure(self):
        result = core._create_result('cat non_existent_file', '')
        self.assertNotEqual(result.returncode, 0)

        self.assertEqual(result.stdout, '')
        self.assertEqual(len(result.stdout_lines), 0)

        self.assertGreater(len(result.stderr), 0)
        self.assertGreater(len(result.stderr_lines), 0)

        self.assertEqual(len(self.stdout_mock.lines), 0)
        self.assertEqual(len(self.stderr_mock.lines), 0)

    def test_param_p(self):
        core._create_result('echo 1', 'p')

        self.assertEqual(len(self.stdout_mock.lines), 1)
        self.assertEqual(self.stdout_mock.lines[0], '1')

        self.assertEqual(len(self.stderr_mock.lines), 0)

    def test_param_e(self):
        result = core._create_result('cat non_existent_file', 'e')

        self.assertEqual(len(self.stdout_mock.lines), 0)

        self.assertGreater(len(self.stderr_mock.lines), 0)
        self.assertEqual(len(self.stderr_mock.lines), len(result.stderr_lines))

    def test_param_e_no_stderr(self):
        core._create_result('echo 1', 'e')

        self.assertEqual(len(self.stderr_mock.lines), 0)

    def test_param_p_no_stdout(self):
        core._create_result('cat non_existent_file', 'p')

        self.assertEqual(len(self.stdout_mock.lines), 0)