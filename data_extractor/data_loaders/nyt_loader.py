import boto3

from data_loaders.news_loader import NewsLoader


class NYTLoader(NewsLoader):
    country = "USA"

    def load_data(self):
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket="mbucket111111", Key='NewsProject/Data Extractor/Config/NYTimesConfig.txt')
        nyt_key = response['Body'].read().decode('UTF-8')
        url = "https://api.nytimes.com/svc/topstories/v2/home.json?api-key=" + nyt_key
        response = self.do_get_request(url)
        content = response.json()

        return [self.get_article_data(article) for article in content["results"]]

    def get_article_data(self, article):
        return {"country": self.country,
                "title": article["title"],
                "author": article["byline"][3:],
                "date": article["created_date"],
                "text": article["abstract"]}
