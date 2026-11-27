# Reproduce the checks

Use an existing Python 3.11 or compatible interpreter. Both scripts use its standard library.

    python3 -B -I scripts/verify_repository.py
    python3 -B -I verification/src/replay.py

The replay checks the squared dyadic factors on 1024 block pairs, the own-block bound at 64 endpoints, and the exact disk floor comparison. Its separate numerical checks confirm unit radial mass and compare the compactly supported disk multiplier with a Bessel series across the plotted range.

Use Lean 4.30.0 and its bundled standard library for the partial arithmetic certificate.

    lean -DwarningAsError=true formal/Q1136Certificate.lean

The certificate proves the two squared dyadic power identities, the own-block index comparison, and the scalar inequality used for the disk example. The analytical Bessel and heat arguments are in the manuscript. [Paper build](paper/BUILD.md) · [Visualization guide](visualization/README.md)
