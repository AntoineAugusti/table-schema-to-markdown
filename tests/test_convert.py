# -*- coding: utf-8 -*-
import unittest
import os.path as op
import io

from table_schema_to_markdown import convert_source


def filepath(f):
    return op.join(
        op.abspath(op.join(__file__, op.pardir, op.pardir, "tests/files")), f
    )


class TestMain(unittest.TestCase):
    def test_convert_source(self):
        files = ["repertoire"]

        for test in files:
            source_filepath, expected_filepath = map(
                filepath, [test + ".json", "expected_" + test + ".md"]
            )

            buff = io.StringIO()
            convert_source(source_filepath, buff)
            got = buff.getvalue().split("\n")
            buff.close()

            with open(expected_filepath, encoding="utf-8") as f:
                expected = f.read().split("\n")

            self.assertEqual(expected, got)
