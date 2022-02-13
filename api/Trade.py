# -*- coding: utf-8 -*
# https://www.ouyicn.help/docs-v5/en/#rest-api-trade
# 交易API调用需要先进行身份验证
# 限速: 60次/2s
import RequestHandler

RequestHandler.post("fff",{})
RequestHandler.__sign("f")

class Trade(object):
    def buy_limit_cross(self,instrument,quantity,price):
        """限价全仓交易

        Args:
            instrument (String): 交易对
            quantity (String)): 数量
            price (String): 价格 
        """
        path = "%s/trade/order" % self.BASE_URL
        params = self._order(instrument, 'cross', 'buy', 'limit', quantity, price)
        return self._post(path, params)

### ----私有函数---- ###
    def _order(self,instId,tdMode,side,ordType,sz,px=None):
        """下单

        Args:
            instId (String): 产品ID
            tdMode (String): 交易模式
            side (String): 订单方向buy/sell
            ordType (String): 订单类型market/limit/post_only/fok/ioc/optimal_limit_ioc
            sz (String): 委托数量
            px (String): 委托价格
        """
        params = {}

        params['instId'] = instId
        params['tdMode'] = tdMode
        params['side'] = side
        params['sz'] = sz

        if px is not None:
            params['ordType'] = ordType
            params['px'] = px
        else:
            params['ordType'] = 'market'

        return params