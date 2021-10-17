from blockTree import BlockTree, TC

class Pacemaker:
    def __init__(self, block_tree, config):

        # instance variables
        self.current_round = 0
        self.last_round_tc = None
        self.pending_timeouts = {}
        # block_tree object
        self.block_tree = block_tree

        self.config = config


    # def get_round_timer(self, round):
    #     #TODO : formula unknown
    #     pass

    # def start_timer(self, new_round):
    #     self.current_round = new_round
    
    # def local_timeout_round(self):
    #     # handled in main module
    #     pass

    def process_remote_timeout(self, timeout):
        timeout_info = timeout.tmo_info

        if timeout_info.round < self.current_round:
            return None

        print("pm 1")
        if timeout_info.round not in self.pending_timeouts.keys():
            self.pending_timeouts[timeout_info.round] = [timeout_info]
            
        else:
            print("pm 11")
            tmo_senders = [t.sender for t in self.pending_timeouts[timeout_info.round] if t is not None]

            if timeout_info.sender not in tmo_senders:
                self.pending_timeouts[timeout_info.round].append(timeout_info)
        print("pm 2")

        tmo_senders = [t.sender for t in self.pending_timeouts[timeout_info.round] if t is not None]

        print("pm 3")

        if len(tmo_senders) == self.config['f'] + 1:
            # stop_timer(self.current_round)
            self.local_timeout_round()

        if len(tmo_senders) == 2*self.config['f'] + 1:
            return TC(
                timeout_info.round,
                [t.high_qc.round for t in self.pending_timeouts[timeout_info.round]],
                [t.signature for t in self.pending_timeouts[timeout_info.round]]
            )
        
        return None

    # def advance_round_tc(self, tc):
    #     if tc is None or tc.round < self.current_round:
    #         return False
    #     self.last_round_tc = tc
    #     self.start_timer(tc.round + 1)
    #     return True

    # def advance_round_qc(self, qc):
    #     if qc.vote_info.round < self.current_round:
    #         return False
    #     self.last_round_tc = None
    #     self.start_timer(qc.vote_info.round + 1)
    #     return True