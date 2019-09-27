import os
import unittest
import StringIO
import sys

from simpleDB import DB

class testExamples(unittest.TestCase):
    """
    File-based unit tests
    """

    def setUp(self):
        self.actual_output = []
        self.db = DB()

        #test configuration
        self.test_data_dir = '{}./data/'.format(os.path.dirname(__file__))

    def test_basic_setgetdelincr(self):
        self.worker('basic_setgetdelincr')

    def test_basic_delval(self):
        self.worker('basic_delval')

    def test_basic_getincr(self):
        self.worker('basic_getincr')

    def test_transaction_multidiscardexec(self):
        self.worker('transaction_multidiscardexec')

    def test_transaction_exec(self):
        self.worker('transaction_exec')

    def test_transaction_discard(self):
        self.worker('transaction_discard')

    def test_transaction_multiempty(self):
        self.worker('transaction_multiempty')

    def test_transaction_delval(self):
        self.worker('transaction_delval')

    def test_transaction_discardonly(self):
        self.worker('transaction_discardonly')

    def test_transaction_execonly(self):
        self.worker('transaction_execonly')


    def worker(self,name):
        """
        Main routine for testing output from <name>_in.txt with <name>_out.txt
        Location of the test files = self.test_data_dir
        """
        out_file = '{}{}_out.txt'.format(self.test_data_dir,name)
        expected_output = self.read_lines(out_file)

        commands = self.read_lines('{}{}_in.txt'.format(self.test_data_dir,name))
        self.run_commands(commands)
        self.assertEqual(len(self.actual_output),len(expected_output),
                'Result from command differens in length compared to {}'.format(out_file))

        for i, act in enumerate(self.actual_output):
            self.assertEqual(str(act), expected_output[i],
                    'Command line {} does not match {}'.format(i+1, out_file))


    def run_commands(self,commands):
        """
        Runs each command and stores the result in actual_output
        capture stdout
        """
        for cmd in commands:
            try:
                capturedOutput = StringIO.StringIO()          
                sys.stdout = capturedOutput                   
                self.db.onecmd(cmd)
                sys.stdout = sys.__stdout__                   
                if capturedOutput.getvalue() != '':
                    self.actual_output.append(capturedOutput.getvalue())
            except SystemExit:
                break

    def read_lines(self,fname):
        """
        Reads and accumulates file content in a list
        """
        with open(fname,'r') as f:
            return [line for line in f]

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(testExamples)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
