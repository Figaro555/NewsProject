import unittest

from pyspark.sql import SparkSession

from test.test_data.df_transformer.aggregations import aggregations
from transformers.df_transformer import DFTransformer


class DFTransformerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession \
            .builder \
            .master("local[*]") \
            .getOrCreate()

        cls.spark.sparkContext.setLogLevel("ERROR")
        cls.transformer = DFTransformer()
        cls.path_prefix = "test/test_data/df_transformer"
        cls.df = cls.spark.read.json(cls.path_prefix + "/raw_table.json")

    def test_aggregate_success(self):
        result = self.transformer.aggreagate(self.df, aggregations)
        expected_result = self.spark.read.json(self.path_prefix + "/all_aggregation_result.json")

        self.assertListEqual(sorted(result.columns), sorted(expected_result.columns))
        self.assertListEqual(result.select(sorted(result.columns)).collect(),
                             expected_result.select(sorted(expected_result.columns)).collect())

    def test_aggregate_failure(self):
        with self.assertRaises(Exception) as context:
            self.transformer.aggreagate(self.df, [])
        self.assertTrue("There is no aggregations" in str(context.exception))

    def test_do_aggregation_success(self):
        for i in range(len(aggregations)):
            result = self.transformer.do_aggregation(self.df, aggregations[i])
            expected_result = self.spark.read.json(self.path_prefix + "/part-" + str(i) + ".json")

            self.assertListEqual(sorted(result.columns), sorted(expected_result.columns))
            self.assertListEqual(result.select(sorted(result.columns)).collect(),
                                 expected_result.select(sorted(expected_result.columns)).collect())

    def test_do_aggregation_failure(self):
        with self.assertRaises(Exception) as context:
            self.transformer.do_aggregation(self.df, {})
        self.assertTrue("Wrong aggregation declaration" in str(context.exception))
