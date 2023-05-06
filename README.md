# merletreepy

Generating the proof and root which can be used for merkle validation in Solidity for airdrop.

## usage
```
# add your white list
wl = WhiteList([
        "0x0000000000000000000000000000000000000000",
        "0x0000000000000000000000000000000000000001",
        "0x0000000000000000000000000000000000000002",
        "0x0000000000000000000000000000000000000003",
        "0x0000000000000000000000000000000000000004",
    ])

# get root
print(wl.get_root())
# get proof of given address
print(wl.get_proof_by_address("0x0000000000000000000000000000000000000000"))
```

## checking with merkletreejs
checking with merkletreejs: [website](https://lab.miguelmota.com/merkletreejs/example/)
