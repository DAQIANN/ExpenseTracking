class Transaction:
    def __init__(self, transaction_type, cost):
        self.transaction_type = transaction_type
        self.cost = cost
    
    def get_transaction_type(self):
        return self.transaction_type
    
    def set_transaction_type(self, transaction_type):
        self.transaction_type = transaction_type
    
    def get_cost(self):
        return self.cost
    
    def set_cost(self, cost):
        self.cost = cost