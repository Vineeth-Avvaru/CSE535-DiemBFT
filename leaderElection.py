from ledger import Ledger

class LeaderElection:
    def __init__(self, validators, window_size, exclude_size, reputation_leaders):
        self.validators = validators
        self.window_size = window_size
        self.exclude_size = exclude_size
        self.reputation_leaders = reputation_leaders

    def elect_reputation_leader(self, qc):
        active_validators = set()
        last_authors = set()
        current_qc = qc
        i = 0
        while i < self.window_size or len(last_authors) < self.exclude_size:
            current_block = Ledger.commited_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            if i < self.window_size:
                active_validators.add(current_qc.signatures.signers())
            if len(last_authors) < self.exclude_size:
                last_authors.add(block_author)
            current_qc = current_block.qc
            i += 1
        return