#!/usr/bin/env python
'''
This module has implementation of financial models for calculating intrinsic
value of a stock.
'''

class IntrinsicValue(object):
    def __init__(self, ):
        pass

class PTE_IntrinsicValue(IntrinsicValue):
    def __init__(self, pe, eps, gr, dr=10, mos=25, years=5):

	# P/E should be taken as median or average of last 5 years
        self.pe = float(pe)   # price to earning

	# Earnings per Share : for last 12 months.
        self.eps = float(eps)	# earnings per share

	# Expected Growth rate for next 5 years.
	self.gr = float(gr)	# growth rate

	# Margin of safety - should be between 15 to 25
	self.mos = float(mos)

	# Adjusted Growth rate
	self.agr = self.gr * (1 - self.mos/100)

	# Number of years
	self.years = float(years)

        # Discount rate
        self.dr = float(dr)

        self._npv, self._ivalue = None, None

    def get_value(self):
        if self._ivalue:
            return self._ivalue
	_gr = 1 + self.agr / 100    # growth rate

        # Value after 5 years
	self._ivalue = self.pe * self.eps * (_gr ** self.years)

        # Net present value
        self._npv = self._ivalue / ((1 + self.dr/100)**self.years)
        return self._npv, self._ivalue

class DCF_IntrinsicValue(IntrinsicValue):
    def __init__(self):
        pass

class ROE_IntrinsicValue(IntrinsicValue):
    def __init__(self):
        pass



if __name__ == '__main__':
    x = PTE_IntrinsicValue(19, 2, 10)
    print  x.get_value()
