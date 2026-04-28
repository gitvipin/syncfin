#!/usr/bin/env python
"""
S&P 500 Ticker Scraper
Scrapes the list of S&P 500 tickers from slickcharts.com/sp500
"""
import argparse
import urllib.request
import re
import sys


def scrape_sp500_tickers():
    """Scrape S&P 500 tickers from slickcharts.com"""
    url = "https://www.slickcharts.com/sp500"
    
    # Add headers to avoid being blocked
    request_obj = urllib.request.Request(url)
    request_obj.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    request_obj.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    
    try:
        with urllib.request.urlopen(request_obj, timeout=30) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse tickers from the HTML
    # The page has tickers in format: <a href="/symbol/SYMBOL">SYMBOL</a>
    # or in data-symbol attributes
    tickers = []
    
    # Pattern 1: <a href="/symbol/AAPL">AAPL</a>
    pattern1 = r'<a[^>]+href="/symbol/([A-Z]+)"[^>]*>.*?</a>'
    matches1 = re.findall(pattern1, html)
    tickers.extend(matches1)
    
    # Pattern 2: data-symbol="AAPL" or symbol in table cells
    pattern2 = r'data-symbol="([A-Z]+)"'
    matches2 = re.findall(pattern2, html)
    tickers.extend(matches2)
    
    # Pattern 3: Look for /symbol/XXX patterns in hrefs
    pattern3 = r'href="/symbol/([A-Z]{1,5})"'
    matches3 = re.findall(pattern3, html)
    tickers.extend(matches3)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tickers = []
    for t in tickers:
        t = t.strip()
        # Filter to only valid ticker symbols
        if t and re.match(r'^[A-Z]{1,5}$', t) and t not in seen:
            seen.add(t)
            unique_tickers.append(t)
    
    return unique_tickers


def main():
    parser = argparse.ArgumentParser(
        description="Scrape S&P 500 tickers from slickcharts.com"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file to save tickers (default: stdout)",
        default=None
    )
    parser.add_argument(
        "-f", "--format",
        choices=["list", "json", "csv"],
        default="list",
        help="Output format (default: list)"
    )
    
    args = parser.parse_args()
    
    print("Scraping S&P 500 tickers from slickcharts.com...")
    tickers = scrape_sp500_tickers()
    
    if not tickers:
        print("No tickers found!", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(tickers)} tickers")
    
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == "list":
                f.write('\n'.join(tickers))
            elif args.format == "json":
                import json
                json.dump(tickers, f, indent=2)
            elif args.format == "csv":
                f.write("ticker\n")
                f.write('\n'.join(tickers))
        print(f"Saved to {args.output}")
    else:
        if args.format == "json":
            import json
            print(json.dumps(tickers, indent=2))
        else:
            print('\n'.join(tickers))


if __name__ == "__main__":
    main()