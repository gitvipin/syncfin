# syncfin

Syncfin (Synchronized Finance) is a Stocks tracking tool. With it, you can do some interesting things which you can not do with other screeners, specially the web based ones. It can download historical data (from yahoo finance) for your analysis. It can plot the graphs on Wavefront. It can generate reports by itself.
 
# Examples

## Update Local Data  (from tickers list)
  
### From Tickers List file

> python -msyncfin.main -u -f data/tickers.list


### From Command line list

> python -msyncfin.main -u -t AAPL GBTC  

## Generate Report
--------

### From TCKR file

>> python -msyncfin.main -r -f data/tickers.list

### From Command line

>> python -msyncfin.main -r -t AAPl GBTC


+------+--------------------+-----------------+
| TCKR | Down from Peak (%) | Up from Low (%) |
+------+--------------------+-----------------+
| AAPl |        4.24        |      28.53      |
| GBTC |       25.17        |      217.15     |
+------+--------------------+-----------------+