from hashing import Hashing
from collections import deque

class Mempool:
	def __init__(self):
		# self.transaction_list = []
		# self.pending_count = 0
		self.transaction_list = deque()

	def insert(self, transaction_obj):
		# self.transaction_list.append({
		# 		'transaction_id' : transaction_obj['transaction_id'],
		# 		'node_id' : transaction_obj['node_id'],
		# 		'state' : "NOT_PROCESSED"
		# 	})
		self.transaction_list.append(transaction_obj['transaction_id'])
		# self.pending_count+=1

	def update_state(self, transaction_id, state=None):

		# #print("trying to pop from mempool", transaction_id, state)
		try:
		# for n in self.transaction_list:
			self.transaction_list.remove(transaction_id)
		except ValueError:
			return
		except IndexError:
			return
		# for t in self.transaction_list:
		# 	#print("COMPARING", t['transaction_id'],  transaction_id)
		# 	if t['transaction_id'] == transaction_id:
		# 		# #print("FOUND TRANSACTION ID")
		# 		t['state'] = state
		# 		self.pending_count -= 1

		# 		return True
		# return False

	def get_transactions(self):
		# transaction_selected = None

		# #print("CURRENT TRANSACTION LIST", self.transaction_list)
		# for t in self.transaction_list:
		# 	if t['state'] == "NOT_PROCESSED":
		# 		transaction_selected = t
		# 		return transaction_selected

		# return transaction_selected
		# #print("trying to pop from mempool1")
		return self.transaction_list.popleft()