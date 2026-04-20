import yfinance as yf

def get_stock_price(ticker: str) -> dict:
    """Fetches the current price and previous close of a given stock ticker."""
    print(f"Agent is calling get_stock_price for: {ticker}")
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        previous_close = info.get('previousClose')
        
        # Fallback just in case the .info dictionary is delayed
        if current_price is None:
            history = stock.history(period="1d")
            if not history.empty:
                current_price = round(history['Close'].iloc[-1], 2)

        return {
            "status": "success",
            "ticker": ticker,
            "current_price": current_price,
            "previous_close": previous_close
        }
        
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to fetch data: {str(e)}"
        }
        


def get_historical_data(ticker: str, period: str = "1mo") -> dict:
    """
    Fetches historical Open, Close, High, Low data for a given stock.
    Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    """
    print(f"Agent is calling get_historical_data for: {ticker} over period: {period}")
    
    try:
        stock = yf.Ticker(ticker)
        # Using period instead of start/end is more reliable for LLM tool calling
        df = stock.history(period=period)
        
        if df.empty:
            return {
                "status": "error", 
                "ticker": ticker,
                "message": "No historical data found. The ticker might be invalid or delisted."
            }
        
        # Format for the LLM: reset index to access the 'Date' column
        df = df.reset_index()
        
        # Convert timestamps to string format so it is JSON serializable
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # Keep it lightweight to save tokens: Date, Open, High, Low, Close [cite: 28]
        # Convert the DataFrame into a list of dictionaries
        records = df[['Date', 'Open', 'High', 'Low', 'Close']].to_dict(orient='records')
        
        return {
            "status": "success",
            "ticker": ticker,
            "period": period,
            "data": records 
        }
        
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to fetch historical data: {str(e)}"
        }


def get_stock_fundamentals(symbol: str) -> dict:
    """Get comprehensive company information."""
    ticker = yf.Ticker(symbol)
    info = ticker.info

    return {
        'market_cap': info.get('marketCap'),
        'pe_ratio': info.get('trailingPE'),
        '52_week_high': info.get('fiftyTwoWeekHigh'),
        '52_week_low': info.get('fiftyTwoWeekLow')
    }
