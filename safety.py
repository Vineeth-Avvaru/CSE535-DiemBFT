from blockTree import LedgerCommitInfo, TimeoutInfo, VoteInfo, VoteMsg, BlockTree
from ledger import Ledger
from hashing import Hashing

class Safety:
    def __init__(self, private_key, public_keys, block_tree, ledger):
        #instance variables
        self.private_key = private_key
        self.public_keys = public_keys

        self.highest_vote_round = 0
        self.highest_qc_round = -1

        self.block_tree = block_tree
        self.ledger = ledger
        pass

    def __increase_highest_vote_round(self, round):
        self.highest_vote_round = max( round, self.highest_vote_round)

    def __update_highest_qc_round(self, qc_round):
        self.highest_qc_round = max(self.highest_qc_round, qc_round)

    def __consecutive(self,block_round, round):
        return round + 1 == block_round

    def __safe_to_extend(self, block_round,qc_round,tc):
        return self.__consecutive(block_round, tc.round) and qc_round >= max(tc.tmo_high_qc_rounds)

    def __safe_to_vote(self, block_round,qc_round,tc):
        if block_round <= max(self.highest_vote_round, qc_round):
            return False
        return self.__consecutive(block_round, qc_round) or self.__safe_to_extend(block_round, qc_round, tc)
    
    def __safe_to_timeout(self, round,qc_round,tc):
        if qc_round < self.highest_qc_round or round <= max(self.highest_vote_round-1, qc_round):
            return False
        return self.__consecutive(round, qc_round) or self.__consecutive(round, tc.round)

    def __commit_state_id_candidate(self, block_round, qc):
        if self.__consecutive(block_round,qc.vote_info.round):
            # argument qc.vote_info.parent_id == block id?
            return self.ledger.pending_state(qc.vote_info.id)
        else:
            return None
    

    def make_vote(self, b, last_tc, node_id):
        qc_round = b.qc.vote_info.round

        #TODO
        #if !valid_signatures(b, last_tc):
        #    return None
        
        if self.__safe_to_vote(b.round, qc_round, last_tc):
            self.__update_highest_qc_round(qc_round)
            self.__increase_highest_vote_round(b.round)
            # exec_state_id == state_id ?
            vote_info = VoteInfo(id = b.id, round = b.round, parent_id = b.qc.vote_info.id, parent_round= qc_round, exec_state_id = self.ledger.pending_state(b.id))
            ledger_commit_info = LedgerCommitInfo(commit_state_id = self.__commit_state_id_candidate(b.round, b.qc), vote_info_hash = Hashing.hash(vote_info))
            return VoteMsg(vote_info = vote_info, ledger_commit_info = ledger_commit_info, high_commit_qc = self.block_tree.get_high_commit_qc(), sender= node_id)
        return None

    def make_timeout(self, round, high_qc, last_tc, node_id):
        qc_round = high_qc.vote_info.round
        # if !self.valid_signatures(high_qc, last_tc):
        #     return None
        if self.__safe_to_timeout(round, qc_round, last_tc):
            self.__increase_highest_vote_round(round)
            return TimeoutInfo(round, high_qc, node_id)
        return None
    