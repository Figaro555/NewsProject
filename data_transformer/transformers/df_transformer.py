from pyspark.sql import DataFrame
from pyspark.sql.functions import avg, lit, count


class DFTransformer:

    def aggreagate(self, df: DataFrame, aggregations: list):
        if len(aggregations) > 0:
            res = self.do_aggregation(df, aggregations[0])
            for i in range(1, len(aggregations)):
                res = res.union(self.do_aggregation(df, aggregations[i]))
            return res
        raise Exception("There is no aggregations")

    def do_aggregation(self, df: DataFrame, agg_description: dict):
        agg_type = None

        try:
            if agg_description['agg_type'] == 'avg':
                agg_type = avg(agg_description['column'])
            elif agg_description['agg_type'] == 'count':
                agg_type = count(agg_description['column'])

            agg1_res = df.where(df[agg_description['column']] > 0) if agg_description['greater_then_zero'] else df

            return agg1_res.groupBy('country') \
                .agg(agg_type.alias('metrix')) \
                .withColumn('category', lit(agg_description['name']))

        except Exception as _ex:
            raise Exception("Wrong aggregation declaration")
