from fastapi import APIRouter
import yfinance as yf
import pandas as pd

router = APIRouter()

@router.get("/api/symbols/{symbol}/info", tags = ["symbols", "tickers"])
async def get_ticker_info(symbol: str):
    ticker = yf.Ticker(symbol)
    return ticker.info

@router.get("/api/symbols/{symbol}/chart/", tags = ["symbols", "tickers", "chart"])
async def get_ticker_chart(symbol: str, period: str = "1d", interval: str = "5m"):
    
    resolution_dict = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1d",
        "6mo": "1d",
        "ytd": "1d",
        "1y": "1d",
        "5y": "1wk",
        "max": "1wk"
    }
    interval = resolution_dict[period]

    ticker = yf.Ticker(symbol)
    hist = ticker.history(period = period, interval = interval)
    hist["utc_timestamp"] = (hist.index.astype(int) * 1E-6).astype(int)

    SPLIT_FIELDS = ["Stock Splits", "utc_timestamp"]
    splits = hist.loc[hist["Stock Splits"] != 0][SPLIT_FIELDS]
    splits.columns = ["split_ratio", "utc_timestamp"]
    stock_splits = splits.to_dict(orient="list")

    TICKER_FIELDS = ["High", "Low", "Close", "Volume", "utc_timestamp"]
    hist = hist[TICKER_FIELDS].dropna()
    hist["price"] = hist[["High", "Low", "Close"]].mean(axis=1)

    response = hist[["utc_timestamp", "price"]].to_dict(orient="list")
    offset_object = hist.index[0].utcoffset()
    utc_offset = int(offset_object.total_seconds()) * 1000 if offset_object else 0
    response["utc_offset"] = utc_offset
    response["stock_splits"] = stock_splits

    return response