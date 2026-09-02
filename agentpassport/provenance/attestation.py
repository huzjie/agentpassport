# -*- coding: utf-8 -*-
"""证明链：为每次智能体动作生成可验证的全链路留痕。"""
from ..crypto import sha256_any, gen_nonce, gen_id, hash_chain_node
from ..models import Attestation


class AttestationChain:
    """把每个动作串联成 parent_hash 链，保证顺序与完整性可验证。"""

    def __init__(self, ledger=None):
        self.ledger = ledger
        self._last_hash = ""

    def record(self, agent_id, action, inputs=None, outputs=None, tool="",
               duration_ms=0, status="ok", metadata=None):
        """记录一次动作，返回 Attestation。"""
        inputs_hash = sha256_any(inputs if inputs is not None else {})
        outputs_hash = sha256_any(outputs if outputs is not None else {})
        att = Attestation(
            record_id=gen_id("att"),
            agent_id=agent_id,
            action=action,
            inputs_hash=inputs_hash,
            outputs_hash=outputs_hash,
            parent_hash=self._last_hash,
            nonce=gen_nonce(),
            tool=tool,
            duration_ms=duration_ms,
            status=status,
            metadata=metadata or {},
        )
        self._last_hash = hash_chain_node(att.parent_hash,
                                          att.record_id + att.inputs_hash + att.outputs_hash)
        if self.ledger:
            self.ledger.append(att)
        return att

    def verify_chain(self, records):
        """校验一条证明链是否连续、无断裂。返回 (ok, broken_index)。"""
        prev = ""
        for i, r in enumerate(records):
            if r.parent_hash != prev:
                return False, i
            prev = hash_chain_node(r.parent_hash,
                                   r.record_id + r.inputs_hash + r.outputs_hash)
        return True, -1
