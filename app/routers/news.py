from fastapi import APIRouter
import pandas as pd
from newsapi import NewsApiClient

import os
from dotenv import load_dotenv

router = APIRouter()

@router.get("/api/news/quandl", tags = ["news"])
async def get_quandl():
    return os.getenv("QUANDL_TOKEN")

@router.get("/api/news/", tags = ["news"])
async def get_news(keywords: str, from_date: str, to_date: str, page: int):

    # load_dotenv('../.env')

    page_size = 20
    source_ids = [
        'axios',
        'bbc-news',
        'bloomberg',
        'cnn',
        'independent',
        'msnbc',
        'nbc-news',
        'reuters',
        'the-wall-street-journal',
        'the-washington-post'
        ]

    id_string = ",".join(source_ids)

    buzzwords = [
                "announce", 
                "report", 
                "stock", 
                "share", 
                "value", 
                "valuation", 
                "market",
                "buy",
                "firm",
                "sell",
                "sale",
                "earn",
                "lose",
                "loss",
                "profit"
                ]
    buzzwords_joined = "({})".format(" OR ".join(buzzwords))

    keywords_split = keywords.split(",")
    keywords_wrapped = ["({})".format(x) for x in keywords_split]
    keywords_joined = "({})".format(" OR ".join(keywords_wrapped))

    query_string = keywords_joined + " AND " + buzzwords_joined

    NEWSAPI_TOKEN = os.getenv("NEWSAPI_TOKEN")
    newsapi = NewsApiClient(api_key=NEWSAPI_TOKEN)
    all_articles = newsapi.get_everything(q=query_string,
                                        sources=id_string,
                                        from_param=from_date,
                                        to=to_date,
                                        language='en',
                                        sort_by='relevancy',
                                        page_size=page_size,
                                        page=page)

    return all_articles