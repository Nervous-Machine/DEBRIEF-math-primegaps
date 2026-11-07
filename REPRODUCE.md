# Reproducing the rerun

What follows is the sequence we ran on 7 November 2026, with the incidental parts (our VM, our log directory) left out.
The scripts as actually run are in `cycle6/scripts/`; they are the record, this is the recipe. Expect about two hours of
machine time on 20 cores, 30 GB of RAM for the Lean build, and roughly 25 GB of disk.

Write down what you expect before you run each step. Ours are in `prereg_cycle6.yaml`.

## 0. Machine

Fresh Ubuntu LTS. We used an aarch64 VM; an x86-64 machine would be the more useful second data point. Run nothing
from the repository on a machine you care about; it is downloaded code.

```sh
sudo apt-get install -y build-essential git curl python3 python3-venv pkg-config libssl-dev time jq unzip
# Go (for landrun), Rust (for nanoda), elan (for Lean), uv (for Python)
curl -sSfL https://go.dev/dl/$(curl -sSL 'https://go.dev/VERSION?m=text' | head -1).linux-$(dpkg --print-architecture).tar.gz | sudo tar -C /usr/local -xz
curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
curl -sSfL https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=$HOME/.elan/bin:$HOME/.cargo/bin:/usr/local/go/bin:$HOME/go/bin:$HOME/.local/bin:$PATH
```

## 1. Source, pinned

```sh
mkdir -p ~/work && cd ~/work
git clone https://github.com/openai/PrimeGaps186.git && cd PrimeGaps186
git checkout 61340d0b74163003b32756bb16e91d9209a5e330
echo "b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0  Challenge.lean" | sha256sum -c -
sha256sum prime_gap_186_certificate.py   # we saw 7f71bdefcfe3bb5ca76a143929b3cb3f4156c21dc483253cda3077420f1e5de4
uname -a; nproc; free -g; go version; rustc --version; elan --version
```

## 2. C4, the Lean build

```sh
cd ~/work/PrimeGaps186
cat lean-toolchain                      # leanprover/lean4:v4.34.0-rc2; elan fetches it on first use
/usr/bin/time -v lake exe cache get      # Mathlib oleans
/usr/bin/time -v lake build PrimeGaps186 2>&1 | tee build.log
grep -ci warning build.log; grep -ci error build.log    # both 0 for us
```

Pass means exit 0 with no error and no warning lines. Record wall time and maximum resident set size from `time -v`.

## 3. C5, Comparator with Nanoda and the Lean kernel

The repository's `comparator/README.md` is the reference. The two external tools:

```sh
cd ~/work
git clone https://github.com/Zouuup/landrun.git && (cd landrun && git rev-parse HEAD && go build -o $HOME/go/bin/landrun ./cmd/landrun)
git clone https://github.com/ammkrn/nanoda_lib.git && (cd nanoda_lib && git rev-parse HEAD && cargo build --release)
```

We used landrun `ec104f6e` and nanoda `8de7e0c4`. Then, in the repository:

```sh
cd ~/work/PrimeGaps186
lake build lean4export/lean4export; lake build Comparator/comparator
export COMPARATOR_LEAN4EXPORT=$(find .lake/packages/lean4export -type f -name lean4export -perm -u+x | head -1 | xargs realpath)
export COMPARATOR_LANDRUN=$HOME/go/bin/landrun
export COMPARATOR_NANODA=$HOME/work/nanoda_lib/target/release/nanoda_bin
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemd-run --property=RestrictAddressFamilies=~AF_UNIX --user --pipe --wait \
  -E PATH -E COMPARATOR_LEAN4EXPORT -E COMPARATOR_LANDRUN -E COMPARATOR_NANODA --working-directory "$PWD" \
  -- bash -c '/usr/bin/time -v lake exe comparator comparator/main.json' 2>&1 | tee comparator.log
```

Pass means Comparator reports all three declarations matched to `Challenge.lean`, Nanoda accepts, the Lean kernel
accepts, and exit 0. Then the axioms:

```sh
cat > /tmp/Axioms.lean <<'LEAN'
import PrimeGaps186
#print axioms PrimeGap186.dhl_40_2
#print axioms PrimeGap186.infinite_two_prime_translates_admissibleTuple
#print axioms PrimeGap186.primeGapLiminf_le_186
LEAN
lake env lean /tmp/Axioms.lean
```

Pass means each theorem uses exactly `PrimeGap186.kloosterman3_bound`, `PrimeGap186.kloosterman2_correlation_bound`,
`PrimeGap186.physical_integral_bounds`, `propext`, `Quot.sound`, `Classical.choice`, and nothing else. Our output is
`cycle6/C5.axioms.txt`.

## 4. C6, the stock library fails the certificate's own regression

```sh
uv venv --python 3.12 ~/work/venv-flint
uv pip install --python ~/work/venv-flint/bin/python "python-flint==0.9.0" "numpy==2.2.6"
~/work/venv-flint/bin/python /path/to/cycle6/scripts/probe_flint.py
```

`probe_flint.py` is the certificate's `check_flint_signed_fft` reproduced verbatim. On the PyPI wheel (which bundles
unfixed FLINT 3.6.0) we saw `"regression": "fail"`, first wrong coefficient at index 15. If a future wheel bundles a
release containing PR 2790, this will pass and step 5 is unnecessary; say which version you had.

## 5. C8, FLINT 3.6.0 plus the one upstream fix

```sh
git config --global user.email you@example.com; git config --global user.name "you"   # cherry-pick needs an identity
cd ~/work && git clone https://github.com/flintlib/flint.git flint-360 && cd flint-360
git checkout v3.6.0 && git cherry-pick -x 7ad753d51c82fdec115cb179b41d0e581f1cb0ec   # applied cleanly for us
./bootstrap.sh && ./configure --prefix=$HOME/work/flint-360fix --disable-static && make -j$(nproc) && make install

uv venv --python 3.12 ~/work/venv-flint-fixed
PFX=$HOME/work/flint-360fix
PKG_CONFIG_PATH=$PFX/lib/pkgconfig CFLAGS="-I$PFX/include" LDFLAGS="-L$PFX/lib -Wl,-rpath,$PFX/lib" \
  uv pip install --python ~/work/venv-flint-fixed/bin/python --no-binary python-flint "python-flint==0.9.0" "numpy==2.2.6"
~/work/venv-flint-fixed/bin/python -c "import flint; print(flint.__version__, flint.__FLINT_VERSION__)"   # 0.9.0 3.6.0
~/work/venv-flint-fixed/bin/python /path/to/cycle6/scripts/probe_flint.py    # expect "regression": "pass"
```

Do not use FLINT main: python-flint 0.9.0's build requires FLINT ≥ 3.0 and < 3.7, and main reports 3.7.0-dev.

## 6. C9, the certificate

```sh
cd ~/work/PrimeGaps186
unset PYTHONOPTIMIZE
/usr/bin/time -v ~/work/venv-flint-fixed/bin/python -B prime_gap_186_certificate.py --workers 4 --output fresh.json 2>&1 | tee certificate.log
python3 -c "import json; r=json.load(open('fresh.json')); print(r['passed'], r['elapsed_seconds'])"
```

The script accepts `--workers 1` or `--workers 4` only. Pass means `"passed": true`. Ours took 1:03:48 with 4 workers
and peaked at 9.7 GB. The receipt also carries the final margin; we computed the lower end exactly from the receipt's
rational fields and compared it to the required 2e-5 (see `cycle6/collect.py`).

## 7. Report

Open an issue titled `Rerun: <machine>` with your environment lines, the exit codes, the wall times, the axiom
printout, the probe outputs and the receipt. Or send a pull request adding a row to `RESULTS.md` and your logs under
`reruns/<date>-<party>/`.
