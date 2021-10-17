class Mempool:
	def __init__(self):
		self.transaction_list = []
		self.pending_count = 0

	def insert(self, transaction_obj):
		self.transaction_list.append({
				'transaction_id' : transaction_obj['transaction_id'],
				'node_id' : transaction_obj['node_id'],
				'state' : "NOT_PROCESSED"
			})
		self.pending_count+=1

	def update_state(self, transaction_id, state):
		for t in self.transaction_list:
			if t['transaction_id'] == transaction_id:
				t['state'] = state
				self.pending_count -= 1
				return True
		return False

	def get_transactions(self):
		transaction_selected = None

		for t in self.transaction_list:
			if t['state'] == "NOT_PROCESSED":
				transaction_selected = t
				return transaction_selected

		return transaction_selected