import pandas
from SymbolInfo import SymbolInfo
import json


class AnalyzeSymbol:

    @classmethod
    def analyze(cls):
        """
        get correlation coefficient between BTC and XRP.
        make XRP chart delay.
        :return:
        """
        print("interval\tcorrelation")
        for i in range(0, 60):
            xrp: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
            btc: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_BTC_JPY)

            d_xrp: list[SymbolInfo.SymbolOHLC] = xrp.find_ohlc_many(skip=i, limit=1000)
            d_btc: list[SymbolInfo.SymbolOHLC] = btc.find_ohlc_many(limit=1000)

            s_xrp = pandas.Series([xrp_ohlcs.close for xrp_ohlcs in d_xrp])
            s_btc = pandas.Series([btc_ohlcs.close for btc_ohlcs in d_btc])

            print("{}\t{}".format(i, s_btc.corr(s_xrp)))

    @classmethod
    def analyze_self(cls):
        """
        get correlation coefficient between BTC and XRP.
        make XRP chart delay.
        :return:
        """
        print("interval\tcorrelation")
        for i in range(0, 60):
            xrp: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
            btc: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)

            d_xrp: list[SymbolInfo.SymbolOHLC] = xrp.find_ohlc_many(skip=i, limit=1000)
            d_btc: list[SymbolInfo.SymbolOHLC] = btc.find_ohlc_many(limit=1000)

            s_xrp = pandas.Series([xrp_ohlcs.close for xrp_ohlcs in d_xrp])
            s_btc = pandas.Series([btc_ohlcs.close for btc_ohlcs in d_btc])

            print("{}\t{}".format(i, s_btc.corr(s_xrp)))

    @classmethod
    def analyze_diff(cls):
        """
        get correlation coefficient between BTC chart move and XRP chart move.
        make XRP chart delay.
        chart move means difference between price on previous minute and current price.
        :return:
        """
        print("interval\tcorrelation")
        for i in range(0, 50):
            xrp: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
            btc: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_BTC_JPY)

            d_xrp: list[SymbolInfo.SymbolOHLC] = xrp.find_ohlc_many(skip=i, limit=1000)
            d_btc: list[SymbolInfo.SymbolOHLC] = btc.find_ohlc_many(limit=1000)

            l_xrp: list[float] = []
            l_btc: list[float] = []

            prev_price = 0
            for xrp_price in [c_xrp.close for c_xrp in d_xrp]:
                if prev_price != 0:
                    l_xrp.append(xrp_price - prev_price)
                prev_price = xrp_price

            prev_price = 0
            for btc_price in [c_btc.close for c_btc in d_btc]:
                if prev_price != 0:
                    l_btc.append(btc_price - prev_price)
                prev_price = btc_price

            s_xrp = pandas.Series(l_xrp)
            s_btc = pandas.Series(l_btc)

            print("{}\t{}".format(i, s_xrp.corr(s_btc)))

    @classmethod
    def analyze_diff_self(cls):
        """
        get correlation coefficient between XRP chart move and XRP chart move(delay).
        make XRP chart delay.
        chart move means difference between price on previous minute and current price.
        :return:
        """
        print("interval\tcorrelation")
        for i in range(0, 50):
            xrp: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
            btc: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)

            d_xrp: list[SymbolInfo.SymbolOHLC] = xrp.find_ohlc_many(skip=i, limit=1000)
            d_btc: list[SymbolInfo.SymbolOHLC] = btc.find_ohlc_many(limit=1000)

            l_xrp: list[float] = []
            l_btc: list[float] = []

            prev_price = 0
            for xrp_price in [c_xrp.close for c_xrp in d_xrp]:
                if prev_price != 0:
                    l_xrp.append(xrp_price - prev_price)
                prev_price = xrp_price

            prev_price = 0
            for btc_price in [c_btc.close for c_btc in d_btc]:
                if prev_price != 0:
                    l_btc.append(btc_price - prev_price)
                prev_price = btc_price

            s_xrp = pandas.Series(l_xrp)
            s_btc = pandas.Series(l_btc)

            print("{}\t{}".format(i, s_xrp.corr(s_btc)))


if __name__ == '__main__':
    AnalyzeSymbol.analyze()

    # _xrp: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
    # _btc: SymbolInfo = SymbolInfo(SymbolInfo.SYMBOLS.FX_XRP_JPY)
    #
    # _d_xrp = _xrp.find_ohlc_many()
    #
    # for ohlc in _d_xrp:
    #     print(ohlc)
