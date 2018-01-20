# raida
A hobby project focused on encoding data in the Raiblock Block lattice

# Requirements to Write Data to the Raiblocks Block Lattice

I'm working on a spec and corresponding python library for this, but do not want to release any part of it until the Raiblock client matures a bit.  I don't want tons of users wrecklessly adding uncompressed data to the network.  It's bad enough we'll probably have many blocks of spam even without a library to make it easy. Check back to this repo later.

# Requirements to Read Data from the Raiblocks Block Lattice

Below is a POC.  I'd like to work with others on a globally logical compression scheme and conventions/metadata to speed up reading and indexing.

* python 3
* a fully synchronized Raiblocks Node running on port 7076
```
pip install raiblocks
git clone https://github.com/jnmclarty/raida.git
python example_read.py
```
