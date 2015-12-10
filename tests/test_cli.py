import csv
import json
import sys
import tests

from collections import OrderedDict
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from elex.cli.app import ElexApp
from six import with_metaclass

DATA_FILE = 'tests/data/20151103_national.json'
ELECTIONS_DATA_FILE = 'tests/data/00000000_elections.json'

TEST_COMMANDS = [
    'races',
    'candidates',
    'reporting-units',
    'candidate-reporting-units',
    'results',
]


class ElexCLICSVTestMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_fields_test(command):
            """
            Dynamically generate a fields test
            """
            def test(self):
                cli_fields, cli_data = self._test_command(command=command)
                api_data = getattr(self, command.replace('-', '_'))
                api_fields = api_data[0].serialize().keys()
                self.assertEqual(cli_fields, api_fields)
            return test

        def gen_length_test(command):
            """
            Dynamically generate a data length test
            """
            def test(self):
                cli_fields, cli_data = self._test_command(command=command)
                api_data = getattr(self, command.replace('-', '_'))
                self.assertEqual(len(cli_data), len(api_data))
            return test

        def gen_data_test(command):
            """
            Dynamically generate a data test
            """
            def test(self):
                cli_fields, cli_data = self._test_command(command=command)
                api_data = getattr(self, command.replace('-', '_'))
                for i, row in enumerate(cli_data):
                    for k, v in api_data[i].serialize().items():
                        if v is None:
                            v = ''
                        self.assertEqual(row[k], str(v))
            return test

        for command in TEST_COMMANDS:
            fields_test_name = 'test_{0}_fields'.format(command.replace('-', '_'))
            dict[fields_test_name] = gen_fields_test(command)
            length_test_name = 'test_{0}_length'.format(command.replace('-', '_'))
            dict[length_test_name] = gen_length_test(command)
            data_test_name = 'test_{0}_data'.format(command.replace('-', '_'))
            dict[data_test_name] = gen_data_test(command)

        return type.__new__(mcs, name, bases, dict)


class ElexCLICSVTestCase(with_metaclass(ElexCLICSVTestMeta, tests.ElectionResultsTestCase)):
    """
    This testing class is mostly dynamically generated by its metaclass.

    The goal of the CLI tests is to the make sure the CLI output matches the
    Python API. The API tests guarantee the validity of the data, while these
    tests guarantee the CLI provides the same data in CSV format.
    """
    def test_elections_fields(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(fields, ['id', 'electiondate', 'liveresults', 'testresults'])

    def test_elections_length(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(len(data), 11)

    def test_elections_date(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(data[4]['electiondate'], '2015-08-04')

    def test_elections_liveresults(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(data[4]['liveresults'], 'False')

    def test_elections_testresults(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(data[4]['testresults'], 'True')

    def test_next_election_fields(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(fields, ['id', 'electiondate', 'liveresults', 'testresults'])

    def test_next_election_length(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(len(data), 1)

    def test_next_election_date(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(data[0]['electiondate'], '2015-08-25')

    def test_next_election_liveresults(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(data[0]['liveresults'], 'True')

    def test_next_election_testresults(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(data[0]['testresults'], 'False')

    def _test_command(self, command, datafile=DATA_FILE, electiondate=None):
        """
        Execute an `elex` sub-command; returns fieldnames and rows
        """
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        argv = [command]

        if electiondate is not None:
            argv.append(electiondate)

        argv = argv + ['--data-file', datafile]

        app = ElexApp(argv=argv)

        app.setup()
        app.log.set_level('FATAL')
        app.run()

        lines = sys.stdout.getvalue().split('\n')
        reader = csv.DictReader(lines)

        sys.stdout.close()
        sys.stdout = stdout_backup

        return reader.fieldnames, list(reader)


class ElexCLIJSONTestMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_fields_test(command):
            """
            Dynamically generate a fields test
            """
            def test(self):
                cli_fields, cli_data = self._test_command(command=command)
                api_data = getattr(self, command.replace('-', '_'))
                api_fields = api_data[0].serialize().keys()
                self.assertEqual(cli_fields, api_fields)
            return test

        def gen_length_test(command):
            """
            Dynamically generate a data length test
            """
            def test(self):
                cli_fields, cli_data = self._test_command(command=command)
                api_data = getattr(self, command.replace('-', '_'))
                self.assertEqual(len(cli_data), len(api_data))
            return test

        def gen_data_test(command):
            """
            Dynamically generate a data test
            """
            def test(self):
                cli_fields, cli_data = self._test_command(command=command)
                api_data = getattr(self, command.replace('-', '_'))
                for i, row in enumerate(cli_data):
                    for k, v in api_data[i].serialize().items():
                        self.assertEqual(row[k], v)
            return test

        for command in TEST_COMMANDS:
            fields_test_name = 'test_{0}_fields'.format(command.replace('-', '_'))
            dict[fields_test_name] = gen_fields_test(command)
            length_test_name = 'test_{0}_length'.format(command.replace('-', '_'))
            dict[length_test_name] = gen_length_test(command)
            data_test_name = 'test_{0}_data'.format(command.replace('-', '_'))
            dict[data_test_name] = gen_data_test(command)

        return type.__new__(mcs, name, bases, dict)


class ElexCLIJSONTestCase(with_metaclass(ElexCLIJSONTestMeta, tests.ElectionResultsTestCase)):
    """
    This testing class is mostly dynamically generated by its metaclass.

    The goal of the CLI tests is to the make sure the CLI output matches the
    Python API. The API tests guarantee the validity of the data, while these
    tests guarantee the CLI provides the same data in JSON format.
    """
    def test_elections_fields(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(fields, ['id', 'electiondate', 'liveresults', 'testresults'])

    def test_elections_length(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(len(data), 11)

    def test_elections_date(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(data[4]['electiondate'], '2015-08-04')

    def test_elections_liveresults(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(data[4]['liveresults'], False)

    def test_elections_testresults(self):
        fields, data = self._test_command(command='elections', datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(data[4]['testresults'], True)

    def test_next_election_fields(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(fields, ['id', 'electiondate', 'liveresults', 'testresults'])

    def test_next_election_length(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(len(data), 1)

    def test_next_election_date(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(data[0]['electiondate'], '2015-08-25')

    def test_next_election_liveresults(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(data[0]['liveresults'], True)

    def test_next_election_testresults(self):
        fields, data = self._test_command(command='next-election', datafile=ELECTIONS_DATA_FILE, electiondate='2015-08-04')
        self.assertEqual(data[0]['testresults'], False)

    def _test_command(self, command, datafile=DATA_FILE, electiondate=None):
        """
        Execute an `elex` sub-command; returns fieldnames and rows
        """
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        argv = [command]

        if electiondate is not None:
            argv.append(electiondate)

        argv = argv + ['--data-file', datafile, '-o', 'json']

        app = ElexApp(argv=argv)

        app.setup()
        app.log.set_level('FATAL')
        app.run()

        json_data = sys.stdout.getvalue()
        data = json.loads(json_data, object_pairs_hook=OrderedDict)

        sys.stdout.close()
        sys.stdout = stdout_backup

        return list(data[0].keys()), data
