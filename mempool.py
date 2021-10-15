class Mempool:
	def __init__(self):
		self.transaction_mapping = {}

	def insert(self, transaction):
		self.transaction_mapping[transaction.id] = transaction

	def get_transactions(self):
		transaction_list = []

		for k, v in self.transaction_mapping:
			transaction_list.append(v)

		return transaction_list