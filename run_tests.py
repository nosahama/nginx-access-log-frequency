"""Tests for nginx-access-log-frequency."""

import unittest
try:
    from StringIO import StringIO
except ImportError:
    # Python 3.x
    from io import StringIO
import sys

from nginx_access_log_ip_frequency import (
    count_nginx_log_ip_address_frequency,
    create_parser,
    print_report
)

EXPECTED_IP_TEST_STRING_OUTPUT = """=========================================
Top 5 Most Frequently Logged IP Addresses
  According to file: example-access.log  
=========================================
 1. 111.222.333.444 : 10
 2. 33.444.55.666   : 9
 3. 222.333.444.555 : 8
 4. 444.555.666.77  : 3
 5. 55.666.777.888  : 2"""


class NGINXAccessLogFrequencyTest(unittest.TestCase):
    """Test Case for for nginx_access_log_frequency.py."""

    def setUp(self):
        """Setup the test client."""
        self.parser = create_parser()

    def assert_output(self, parser_args, expected_output):
        """
        Verify that `expected_output` will be generated by `parse_args`.

        Raises:
        AssertionError if `expected_output` was not generated by `parse_args`.
        """
        c = count_nginx_log_ip_address_frequency(parser_args.file)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_report(
                c,
                parser_args.limit,
                parser_args.file
            )
            output = out.getvalue().strip()
            assert output == expected_output
        finally:
            sys.stdout = saved_stdout

    def test_nginx_access_log_frequency(self):
        """Test nginx_access_log_frequency.py."""
        args = self.parser.parse_args([
            '-l',
            '5',
            '-f',
            'example-access.log'
        ])
        self.assert_output(args, EXPECTED_IP_TEST_STRING_OUTPUT)

if __name__ == '__main__':
    unittest.main()
