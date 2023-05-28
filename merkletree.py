# coding:utf-8
"""
@author: weitaochu@gmail.com
@time: 2023/5/6
"""

import sha3
from web3 import Web3
from lib import MerkleTools


class WhiteList:
    def __init__(self, white_list: [str]):
        self.white_list = white_list
        self.mt = MerkleTools()
        self.mt.hash_function = sha3.keccak_256
        self._add_leaf()

    def _add_leaf(self):
        self.mt.add_leaf(
            [
                Web3.solidity_keccak(["address"], [Web3.to_checksum_address(key)]).hex()[2:]
                for key in self.white_list
            ]
        )
        self.mt.make_tree()

    def get_root(self):
        return self.mt.get_merkle_root()

    def get_proof_by_address(self, address: str):
        hashed_address = Web3.solidity_keccak(["address"], [Web3.to_checksum_address(address)]).hex()[2:]
        _byte = bytearray.fromhex(hashed_address)
        if _byte in self.mt.leaves:
            return self._get_proof(_byte)
        raise ValueError(f"Address: {address} not found")

    def get_proof_by_index(self, index: int):
        if self.mt.get_leaf_count() - 1 < index:
            raise ValueError(f"Out of range")
        return self._format_proof(self.mt.get_proof(index))

    def _get_proof(self, _byte: bytearray):
        return self._format_proof(self.mt.get_proof(self.mt.leaves.index(_byte)))

    def get_leafs(self):
        return [lf.hex() for lf in self.mt.leaves]

    @staticmethod
    def _format_proof(proofs: []):
        _proofs = []
        for p in proofs:
            for _, v in p.items():
                _proofs.append(v)
        return _proofs

    def check_all(self):
        root = self.get_root()
        print(f"Root: {root}")
        for index, _ in enumerate(self.white_list):
            is_valid = self.mt.validate_proof(self.mt.get_proof(index), self.mt.get_leaf(index), root)
            print(f"Index: {index}, "
                  f"leaf: {self.mt.get_leaf(index)}, proof: {self.get_proof_by_index(index)}, valid: {is_valid}")


if __name__ == '__main__':
    wl = WhiteList([
        "0x0000000000000000000000000000000000000000",
        "0x0000000000000000000000000000000000000001",
        "0x0000000000000000000000000000000000000002",
        "0x0000000000000000000000000000000000000003",
        "0x0000000000000000000000000000000000000004",
    ])
    print("ROOT", wl.get_root())
    print(wl.get_proof_by_address("0x0000000000000000000000000000000000000000"))
    wl.check_all()
    print("leafs", wl.get_leafs())

