

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


0. Choose one irrational number, r, from the set of pi, e or root 2.
1. Choose one random integer, n, from the set of integers from 1 to 19 excluding 10.
2. Choose one random integer, m, from the set of integers from 2 to 10.
3. Solve for a data-channel d, equal to round(r * (10^m) * n, 0)
4. Set frequency band, send d rai from WC to RX.
5. Choose payload packet mode, p
   1. 1 if byte (1-256)
   2. 2 if word (2 bytes) (1-65536)
   3. 3 if doubleword (4 bytes) (1-4294967296)
   4. 4 if quadword (8 bytes) (1-18446744073709551616)
   5. 5 if dynamic (reader's choice, eg. introspection) (1-total supply of rai)
   6. 6 if invoice (eg. succinct invoice requests)
   7. 7 if payment (eg. succinct invoice payments)
   8. 8 if time (eg. succinct due date communication)
   9. 9 to 99 are reserved.
6. Optionally, choose an End-of-Transmission value, e.  Any value not included in the transmission or one included rarely (requires escaping) is ideal.  Recommendation and default is the value 4 (ASCII "EOT").
7. Optionally, choose an Escape value, s, as any value not included in the transmission or one included rarely and between 1 and 99.  Recommendation is the value 27 (ASCII "Escape").  Unset defaults to 0 but disables the transmission of the EOT value; which is the only thing it would need to escape, other than itself.
8. Send (e x 10000) + (s x 100) + p from WC to RX. Examples:
   1. 3 : payload packets are doublewords, EOT value is 4 (default), escape is 0. (default).
   2. 40003 : same treatment as simply sending "3", except it's explicit.
   3. 22701 : payload packets are bytes, EOT is 2, escape is 27 (recommended).
   4. 2601 : payload packets are bytes, EOT is 4 (default), escape is 26.
9. Send data.
10. Optionally, calculate a checksum of everything sent except the frequency band selection, send it.
11. Send EOT value (End-Of-Transmission).

# Logic for Permissioned Write

A permissioned write is one where the account initiating the write controls the private keys to two other accounts.  One for the data destination, the other a temporary account which will have a balance of zero after transmission.  These are cheaper, capital wise, to transmit and should be more efficient to read.

So, starting with...

WC - the account treated as the "sender" of the data, with enough rai to cover the frequency channel selection.
A - an account with a starting balance sufficient to cover the transmission and where the data will persist.
B - an account without a starting balance for returning capital to A and must never be used twice, will return all capital to A.

The pseudo code is exactly the same as in the permissionless write, except:

1. The frequency selection happens from WC to A, then everything else is bi-directional between A and B, recycling rai during transmission.
2. Any leftover rai in B is sent to A or WC, leaving a 0 balance in B.  A is the default, but only works with an EOT.

# Mode Syntax

The following convention is used below.

```
[] - mandatory
() - optional
```

### Summary of Generalized Protocol

Any complete data transmission on Raiblocks has an overhead of at least 2 transactions, and at a maximum 4 + N, where N is the number of packets that need to be escaped.

```
[FREQUENCY BAND SELECTION] [PAYLOAD PACKET MODE]
(DATA 1) (DATA 2) ... (escape) (DATA=eot) ... (DATA N)
(checksum) (EOT)
```

#### Permissionless
```
Let S be a transaction from WC to RX.

S314 S1 S74 S101 S102 S102 S4
```

#### Permissioned
```
Let WCA, AB & BA be a transaction from WC to A, A to B and B to A.

WCA314 AB1 AB74 AB101 BA102 AB102 BA4 BA172

Notice the switch half way through, funds are sent back to A as data.  The BA172 is effectively ignored.
```


### Mode 1 : Bytes

Mode 1 tells the reader that everything coming after is bytes.

```
[FREQUENCY BAND SELECTION] [1] (DATA 1) (DATA 2) ... (escape) (DATA=eot) ... (DATA N) (checksum) (EOT)
```

####  Example for sending the string "Jeff" with bytes

Below is a *permissionless* write.

```
[3141] [1] (1) (e) (f) (f) (EOT)

becomes...

S3141 S1 S74 S101 S102 S102 S4
```

We're communicating on the 1-3-pi frequency, with mode 1 and the default EOT value, with no escape value set.

####  Example for sending the a byte stream of the values 1, 2, 3, 4

Below is a *permissionless* write.

```
[31415] [1] (1) (2) (3) (4) (EOT)

becomes...

S31415 60001 1 2 3 4 6
```

We're communicating on the 1-4-pi frequency, with mode 1 and a non-default EOT value of 6, with no escape value set.


### Mode 6 : Invoices

The 6th mode is a special ultra compact method of requesting a payment on raiblocks. An invoice could be requested, for instance.

####  Example for an Invoice

```
[FREQUENCY BAND SELECTION] [6] [RAW NUMBER] x 10 ^ (RAW NUMBER) (INVOICING TERMS SWITCH) (X)/(Y) NET (Z) (EOT)

So an invoice of 55000000000 raw would be:

S314 S6 S55 S9 S4

...where "S" represents sending from WC to RX.
```

# FAQ

1. What's with the Frequency Band Selection? pi? e? root-2?

The vision here is that indexing raiblock clients will look for receives that are part of an future-proof, infinitely scalable set only constrained by the rai supply.  This set is defined as something easy to derive and implement in any programming language as well as fairly quick to search against.  The exact set is still a WIP, but the idea is that these will work like AM/FM radio stations, except a client could scan more (or all to a logical ceiling) at a time.  With the parameters as defined, there are exactly 432 unique stations, which can individually be communicated to other humans such as "4-10-pi" or "2-7-root-2".  These numbers were selected because they shouldn't overlap with values that are likely more common such as numbers under 100, an ASCII character, or multiples of round numbers, are relatively low and don't overlap on themselves.  Prime numbers were also considered, but ruled out on the fact that the set it harder to derive.

2. Why is the checksum optional?

If you're sending only a few bytes, or have a use case that should be lightweight, or low-risk, the protocol allows for skipping the checksum.  For higher reliability, add it.  This means applications will have a choice to make surrounding assuming if the last packet is the checksum or if it's actually data.  Forcing all use cases to include one is taxing on everybody.  This means that use cases which need it, are forced to make an assumption about the last send.  Is the data corrupt or was the checksum omitted?  Your app can decide this.
