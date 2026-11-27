# Explore the dyadic kernel scaling

[Download the offline explorer ZIP](https://raw.githubusercontent.com/DannyExperiments/endpoint-bessel-fourier-coefficients/v1.0.0/visualization/endpoint-bessel-fourier-coefficients-explorer.zip), extract it, and open index.html. Change the radius from 1/2 to 1/4 or 1/8, and drag Rotate to view the spatial footprint. The left surface is divided by its own peak so the widths remain visible at every scale.

The teaching example uses a uniform probability density on a disk of radius 1/2. Its autocorrelation is a constant times the disk overlap area. Relative to its peak, the autocorrelation at separation u within the unit disk is (2/π)(arccos u − u√(1 − u²)). The Fourier multiplier is the square of the real Fourier transform of the uniform disk. The transform can be integrated as (4/π)∫ cos((s/2) sin θ) cos²θ dθ on [0, π/2]. Quadrature provides the plotted values.

The guaranteed half-height band is exact. For argument s no greater than 1/2, the projection of any point in the disk has absolute value no greater than 1/2. The cosine lower bound gives transform at least 1 − s²/8 ≥ 31/32, so its square is above 1/2. Dilation by r makes the guarantee extend to frequency 1/(2r). The smooth kernel in the general proof supplies the same type of guarantee plus decay for the high-frequency estimates.

To render the GIF, use an existing Python environment with Pillow and Arial or DejaVu Sans available.

    python3 visualization/render.py
