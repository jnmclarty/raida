

# Use-Cases & Accompanying Standards

0. Block Lattice General Data Protocol (RAI-BLGDP/"BLGDP")
  A. Permissionless Write -> Data is written to an account you don't control.
  B. Permissioned Write -> Data is written between two accounts you do control.
1. Value Transmission Meta Data Convention (RAI-VTMD/"VTMD")
2. Nested Arbitrary Command Convention (RAI-NACC/"NACC")
3. Encoding-explicit, version-mandatory, compression-optional, encryption-optional file-format (RAI-FF/"RFF")
4. Namespaced Name Service Registry (RAI-NNSR/"NNSR")
5. Messaging Protocol (RAI-MP)
6. Voting Protocol (RAI-VP)
7. Bounty Protocol (RAI-BP)

# Principles

0. Block Lattice space should be considered a scarce resource.
1. Terminating balances should be strongly-coupled with the priority of the data.  Zero-balance ==> Delete/Ignore the byte stream.
2. Accidental pockets (ie. receiving spam) should not destroy data or reduce performance of read operations.
3. Indexing of data on the block lattice should be efficient.
4. Reading data on the block lattice should be as fast as possible.
5. Writing data on the block lattice should be as cheap as possible.
6. Everything should be trustless, but optionally centralized for enhanced versions of representatives for fast indexing.
7. You should be able to send somebody else the data, so they control the private keys.

# Pseudo code for Permissionless Write

Starting with:
* an account you control with working capital, WC and
* an account you do not control with or without a balance, A

1. Choose one random integer, n, greater than or equal to 1 and less than 15.
2. Choose one random integer, m, greater than or equal to 1 and less than 11.
2. Solve for a data-channel d, equal to round(pi * (10^m) * n, 0)
3. Set frequency band, send d rai from WC to A.
4. Choose size control Value:  
   4.1 if byte (1-256), send 1 from WC to A.
   4.2 if word (2 bytes) (1-65536), send 2 from WC to A.
   4.3 if doubleword (4 bytes) (1-4294967296), send 3 from WC to A.
   4.4 if quadword (8 bytes) (1-18446744073709551616), send 4 from WC to A.
   4.5 if dynamic (reader introspects) (1-total supply of rai), send 5 from WC to A.

   You can omit this control value if the first value in the transmission is
   not of the set above and you are okay with dynamic.  

   If you first character is 1, 2, 3, 4, 5 or 6 then you must send 5 as a
   control value.

   4.6 if number, send 6 from WC to A.

   This is a special ultra compact method of requesting an payment on raiblocks.

   An invoice could be requested as easy as:

   [FREQUENCY BAND SELECTION] [6] [RAW NUMBER] x 10 ^ (RAW NUMBER) (INVOICING TERMS SWITCH) (X)/(Y) NET (Z) (EOT)

5. Send 4. (End-Of-Transmission)

The overhead of any complete data transmission on Raiblocks is 4 transactions:
[FREQUENCY BAND SELECTION] (SIZE SELECTION) n x (DATA) (EOT)

# Pseudo code for Permissioned Write

Starting with:
* an account you control with working capital, WC and
* an account you do not control with or without a balance, B


2.  random number from the set of {3, 31, 314, 31419}
  1. Determine Send the value of pi scaled by multiples of 10, rounded to the nearest equivalent of pi from A to B
  2. Send a stream of doubles A to B
  3. Send the same integer equivalent of pi from A to B


# Block Lattice General Data Protocol



# Nested Arbitrary Command Convention "NACC"

#
# Namespaced Name Service Registry
