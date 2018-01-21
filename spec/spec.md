

# Use-Cases & Accompanying Standards

0. Block Lattice General Data Protocol (RAI-BLGDP/"BLGDP")
   1. Permissionless Write -> Data is written to an account you do not control.
   2. Permissioned Write -> Data is written between two accounts you control.
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

# Logic for Permissionless Write

A permissionless write is one where the person initiating the write does not control the private keys to the account which will pocket the data.  The account which receives the data also receives (and therefore can optionally keep) the rai.  

So, starting with...

WC - an account you control with ample raiblocks
RX - an account you do not control with or without a balance


1. Choose one random integer, n, greater than or equal to 1 and less than 15.
2. Choose one random integer, m, greater than or equal to 1 and less than 11.
3. Solve for a data-channel d, equal to round(pi * (10^m) * n, 0)
4. Set frequency band, send d rai from WC to RX.
5. Optionally, Choose payload packet mode, p
   1. if byte (1-256)
   2. if word (2 bytes) (1-65536)
   3. if doubleword (4 bytes) (1-4294967296)
   4. if quadword (8 bytes) (1-18446744073709551616)
   5. if dynamic (reader introspects) (1-total supply of rai)
   6. if number (succinct invoice requests)
   7. to 99. are reserved
6. Optionally, Choose an End-of-Transmission value, e, as any value not included in the transmission or one included rarely (requires escaping).  Recommendation is the value 4 (ASCII "EOT"). Unset the protocol treats it as the default 4.
7. Optionally, Choose an Escape value, s, as any value not included in the transmission or one included rarely.  Recommendation is the value 27 (ASCII "Escape").  Unset defaults to 0 and then effectively disables the transmission of the EOT value; which is the only thing it would need to escape, other than itself.
8. Optionally, Send (s x 1000) + (e x 100) + p from WC to RX. Examples:
   1. 3 : payload packets are doublewords, EOT value is 4 (default), escape is 27 (default).
   2. 27403 : same treatment as 3 except explicit.
   3. 201 : payload packets are bytes, EOT transmission value is 2, escape is 27 (default).
9. Optionally, send value set as EOT (End-Of-Transmission).

Notes:

Omission of the control value will default reading to mode 5 (dynamic).

If the first data value is 1, 2, 3, 4, 5 or 6 then you must send 5 as a
control value to select dynamic treatment.

The 6th mode is a special ultra compact method of requesting a payment on raiblocks. An invoice could be requested, for instance.

### Summary of Permissionless Write

Any complete data transmission on Raiblocks is at a minimum 1 + N transactions, and at a maximum 3 + N transactions, where N is the payload

```
[FREQUENCY BAND SELECTION] (PAYLOAD PACKET MODE) (DATA 1) (DATA 2) ... (DATA N) (EOT)

[] - mandatory
() - optional
```

####  Example for an Invoice

```
[FREQUENCY BAND SELECTION] [6] [RAW NUMBER] x 10 ^ (RAW NUMBER) (INVOICING TERMS SWITCH) (X)/(Y) NET (Z) (EOT)

So an invoice of 55000000000 raw would be:

S314 S6 S55 S9 S4

...where "S" represents sending from WC to RX.
```

# Logic for Permissioned Write

A permissioned write is one where the account initiating the write controls the private keys to two other accounts.  One for the data destination, the other a temporary account which will have a balance of zero after transmission.  These are cheaper, capital wise, to transmit and should be more efficient to read.

So, starting with...

WC - the account treated as the "sender" of the data, with enough rai to cover the frequency channel selection.
A - an account with a starting balance sufficient to cover the transmission and where the data will persist.
B - an account without a starting balance for returning capital to A and must never be used twice, will return all capital to A.

The pseudo code is exactly the same as in the permissionless write, except:

1. The frequency selection happens from WC to A, then everything else is bi-directional between A and B, recycling rai during transmission.
2. Any leftover rai in B is sent to A or WC, leaving a 0 balance in B.  A is the default, but only works with an EOT.

####  Example for sending the string "Jeff" with bytes

```
[FREQUENCY BAND SELECTION] [1] (J) (e) (f) (f) (EOT)

Let WCA, AB & BA be a transaction from WC to A, A to B and B to A.

WCA314 AB1 AB74 AB101 BA102 AB102 BA4 BA172

The BA172 is effectively ignored.

```
