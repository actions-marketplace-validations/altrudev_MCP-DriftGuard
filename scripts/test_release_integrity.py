#!/usr/bin/env python3
"""Mutation probes proving that missing/false/stale evidence cannot be accepted."""
import sys
sys.dont_write_bytecode = True
import unittest
from release_integrity import assess, REQUIRED

REV="a"*40
def good():
    return {"commit":REV,"passed":True,"suites":{n:{"exit":0,"stdout_sha256":"a"*64,"stderr_sha256":"b"*64} for n in REQUIRED}}

class IntegrityMutations(unittest.TestCase):
    def test_good_local_evidence(self):
        self.assertEqual(assess(good(),REV),[])
    def test_wrong_revision(self):
        self.assertTrue(assess(good(),"b"*40))
    def test_aggregate_false(self):
        e=good();e["passed"]=False
        self.assertTrue(assess(e,REV))
    def test_each_required_suite_removed(self):
        for name in REQUIRED:
            with self.subTest(suite=name):
                e=good();del e["suites"][name]
                self.assertTrue(assess(e,REV))
    def test_each_required_suite_failed(self):
        for name in REQUIRED:
            with self.subTest(suite=name):
                e=good();e["suites"][name]["exit"]=1
                self.assertTrue(assess(e,REV))
    def test_boolean_exit_rejected(self):
        e=good();e["suites"]["go_unit"]["exit"]=False
        self.assertTrue(assess(e,REV))
    def test_absent_output_digest_rejected(self):
        e=good();del e["suites"]["go_unit"]["stdout_sha256"]
        self.assertTrue(assess(e,REV))
    def test_malformed_output_digest_rejected(self):
        e=good();e["suites"]["go_unit"]["stderr_sha256"]="invalid"
        self.assertTrue(assess(e,REV))
    def test_missing_suites(self):
        e=good();del e["suites"]
        self.assertTrue(assess(e,REV))
    def test_empty_suites(self):
        e=good();e["suites"]={}
        self.assertTrue(assess(e,REV))

if __name__=="__main__":
    unittest.main()
