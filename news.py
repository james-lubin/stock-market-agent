from newsapi import NewsApiClient

class News:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='138fc100540742c2b756f3c9220ea091')

    def getHeadlines(self, stock, numHeadlines, beginDate, endDate):
        '''Returns a list of current headlines related to the stock. Uses the Google
        news API. We can also use the newsapi.get_everything() function if we
        need more articles.'''
        jsonHeadlines = self.newsapi.get_everything(
            q = stock,
            from_param = beginDate,
            to = endDate,
            sort_by='relevancy',
            language = 'en')

        status = jsonHeadlines["status"]
        if status == "error":
            return jsonHeadlines["message"]
        else: #request was successful
            totalResults = jsonHeadlines["totalResults"]

        headlines = []
        numResultsToReturn = min(totalResults, numHeadlines)
        articles = jsonHeadlines["articles"]
        for i in range(numResultsToReturn):
            headlines.append(articles[i]["title"])

        return headlines
