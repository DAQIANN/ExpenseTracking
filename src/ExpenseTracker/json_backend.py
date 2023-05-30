import json
from ExpenseTracker.transaction import Transaction

class TransactionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Transaction):
            return {
                '__custom__': True,
                'transaction_type': obj.get_transaction_type(),
                'cost': obj.get_cost()
            }
        return super().default(obj)

def transaction_decoder(obj):
    if '__custom__' in obj:
        transaction_type = obj['transaction_type']
        cost = obj['cost']
        return Transaction(transaction_type, cost)
    return obj

def load_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file, object_hook=transaction_decoder)

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, cls=TransactionEncoder)
