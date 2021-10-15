#from block_tree import LedgerCommitInfo, TimeoutInfo, VoteInfo, VoteMsg, BlockTree
#from ledger import Ledger

class Safety:
    def __init__(self, private_key, public_keys, highest_vote_round, highest_qc_round, blockTree, ledger):
        pass

    def __increase_highest_vote_round(self, round):
        pass

    def __update_highest_qc_round(self, qc_round):
        pass

    def __consecutive(self,block_round, round):
        pass

    def __safe_to_extend(self, block_round,qc_round,tc):
        pass

    def __safe_to_vote(self, block_round,qc_round,tc):
        pass

    def __safe_to_timeout(self, round,qc_round,tc):
        pass

    def __commit_state_id_candidate(self, block_round, qc):
        pass

    def make_vote(self, b, last_tc):
        pass

    def make_timeout(self, round, high_qc, last_tc):
        pass
    