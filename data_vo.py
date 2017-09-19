class DataVo (object):
    def __init__(self):
        self._order_id=None
        self._product_name = None
        self._order_status = None
        self._product_url = None
        self._cost_price = None

        @property
        def order_id(self):
            self._order_id

        @order_id.setter
        def order_id(self, value):
            self._order_id = value


        @property
        def product_name(self):
            self._product_name

        @product_name.setter
        def product_name(self, value):
            self._product_name = value

        @property
        def order_status(self):
            self._order_status

        @order_status.setter
        def order_status(self, value):
            self._order_status = value

        @property
        def product_url(self):
            self._product_url

        @product_url.setter
        def product_url(self, value):
            self._product_url = value

        @property
        def cost_price(self):
            self._cost_price

        @cost_price.setter
        def cost_price(self, value):
            self._cost_price = value


    def serialize(self):
        d = dict()
        d['order_id'] = self._id
        d['product_name'] = self._product_name
        d['order_status'] = self._order_status
        d['order_status'] = self._order_status
        d['cost_price'] = self._cost_price
        return d
