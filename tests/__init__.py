import unittest

from elex.api import api, utils


class ElectionResultsTestCase(unittest.TestCase):
    data_url = 'tests/data/20151103_national.json'

    def setUp(self, **kwargs):
        e = api.Election(electiondate='2015-11-03', datafile=self.data_url, testresults=False, liveresults=True, is_test=False)
        self.raw_races = e.get_raw_races()
        self.race_objs = e.get_race_objects(self.raw_races)
        self.ballot_measures = e.ballot_measures
        self.candidate_reporting_units = e.candidate_reporting_units
        self.candidates = e.candidates
        self.races = e.races
        self.reporting_units = e.reporting_units
        self.results = e.results


class ElectionNetworkTestCase(unittest.TestCase):
    def setUp(self, **kwargs):
        """
        Cache all responses to allow for single assertion per test without
        exceeding the API request limit.
        """
        self.nonexistent_response = utils.api_request('/1965-01-01')
        self.nonexistent_param_response = utils.api_request('/', foo='bar')
        self.bad_date_response = utils.api_request('/9999-99-99')
