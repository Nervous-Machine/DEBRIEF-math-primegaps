"""C6 probe: the certificate's startup regression, reproduced verbatim from prime_gap_186_certificate.py
(openai/PrimeGaps186 @ 61340d0, check_flint_signed_fft), run against stock python-flint from PyPI."""
import json, platform, sys
import flint
from flint import fmpz_poly


def check_flint_signed_fft():
    """Reject the known signed-FFT regression; never modify the library."""
    a, b = (1 << 509) - 1, (1 << 510) - 1
    p, q = fmpz_poly([a] * 16), fmpz_poly([-b] * 16)
    expected = [-min(j + 1, 31 - j, 16) * a * b for j in range(31)]
    if p * q != fmpz_poly(expected) or p.mul_low(q, 16) != fmpz_poly(expected[:16]):
        raise RuntimeError(
            "FLINT failed its signed-FFT regression; install a build with corrected signed convolution."
        )


out = {"check": "C6", "python": platform.python_version(), "machine": platform.machine(), "system": platform.system(),
       "python_flint": getattr(flint, "__version__", None),
       "flint_version": next((getattr(flint, n) for n in ("__flint_version__", "flint_version", "FLINT_VERSION") if hasattr(flint, n)), None)}
try:
    check_flint_signed_fft()
    out["regression"] = "pass"
except RuntimeError as e:
    out["regression"] = "fail"
    out["error"] = str(e)
    # how wrong is it? record the product's first few coefficients vs expected
    a, b = (1 << 509) - 1, (1 << 510) - 1
    p, q = fmpz_poly([a] * 16), fmpz_poly([-b] * 16)
    got, exp = (p * q).coeffs(), [-min(j + 1, 31 - j, 16) * a * b for j in range(31)]
    out["first_mismatch_index"] = next((j for j, (g, e) in enumerate(zip(got, exp)) if int(g) != e), None)
    out["degree_got"] = len(got) - 1
print(json.dumps(out, indent=1))
