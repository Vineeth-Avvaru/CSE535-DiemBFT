from ledger import Ledger
import random

class LeaderElection:
    def __init__(self, validators, window_size, exclude_size, seed, ledger, pacemaker):
        self.validators = validators
        self.window_size = window_size
        self.exclude_size = exclude_size
        self.reputation_leaders = {} # round to leaders elected
        self.seed = seed
        self.ledger = ledger
        self.pacemaker = pacemaker

    def elect_reputation_leader(self, qc):
        active_validators = set()
        last_authors = set()
        current_qc = qc
        i = 0
        while i < self.window_size or len(last_authors) < self.exclude_size:
            current_block = self.ledger.commited_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            if i < self.window_size:
                active_validators.add(current_qc.signatures.signers())
            if len(last_authors) < self.exclude_size:
                last_authors.add(block_author)
            current_qc = current_block.qc
            i += 1
        random.seed(self.seed)
        return random.choice(active_validators)

    def update_leaders(self, qc):
        extended_round = qc.vote_info.round
        qc_round = qc.vote_info.round
        current_round = self.pacemaker.current_round
        if extended_round + 1 == qc_round and qc_round + 1  == current_round:
            self.reputation_leaders[current_round+1] = self.elect_reputation_leader(qc)
        
    def get_leader(self, round):
        if round in self.reputation_leaders.keys():
            return self.reputation_leaders[round]
        
        return self.validators[(round//2)%len(self.validators)]