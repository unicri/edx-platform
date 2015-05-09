
import os
import unittest
from pavelib.utils.test.suites.bokchoy_suite import BokChoyTestSuite

REPO_DIR = os.getcwd()


class TestPaverBokChoyCmd(unittest.TestCase):

    def setUp(self):
        self.request = BokChoyTestSuite('')

    def _expected_command(self, expected_text_append, expected_default_store=None):
        if expected_text_append:
            expected_text_append = "/" + expected_text_append
        shard = os.environ.get('SHARD')
        expected_statement = (
            "DEFAULT_STORE={default_store} "
            "SCREENSHOT_DIR='{repo_dir}/test_root/log{shard_str}' "
            "BOK_CHOY_HAR_DIR='{repo_dir}/test_root/log{shard_str}/hars' "
            "SELENIUM_DRIVER_LOG_DIR='{repo_dir}/test_root/log{shard_str}' "
            "nosetests {repo_dir}/common/test/acceptance/tests{exp_text} "
            "--with-xunit "
            "--xunit-file={repo_dir}/reports/bok_choy{shard_str}/xunit.xml "
            "--verbosity=2 "
        ).format(
            default_store=expected_default_store,
            repo_dir=REPO_DIR,
            exp_text=expected_text_append,
            shard_str='/shard_' + shard if shard else '',
        )
        return expected_statement.strip()

    def test_default_bokchoy(self):
        self.assertEqual(self.request.cmd.strip(), self._expected_command(''))

    def test_suite_request_bokchoy(self):
        self.request.test_spec = "test_foo.py"
        self.assertEqual(self.request.cmd.strip(), self._expected_command(self.request.test_spec))

    def test_class_request_bokchoy(self):
        self.request.test_spec = "test_foo.py:FooTest"
        self.assertEqual(self.request.cmd.strip(), self._expected_command(self.request.test_spec))

    def test_case_request_bokchoy(self):
        self.request.test_spec = "test_foo.py:FooTest.test_bar"
        self.assertEqual(self.request.cmd.strip(), self._expected_command(self.request.test_spec))

    def test_default_bokchoy_with_draft_default_store(self):
        self.request.test_spec = "test_foo.py"
        self.request.default_store = "draft"
        self.assertEqual(self.request.cmd.strip(), self._expected_command(self.request.test_spec, "draft"))

    def test_default_bokchoy_with_invalid_default_store(self):
        # the cmd will dumbly compose whatever we pass in for the default_store
        self.request.test_spec = "test_foo.py"
        self.request.default_store = "invalid"
        self.assertEqual(self.request.cmd.strip(), self._expected_command(self.request.test_spec, "invalid"))

    def test_serversonly(self):
        self.request.serversonly = True
        self.assertEqual(self.request.cmd.strip(), "")
