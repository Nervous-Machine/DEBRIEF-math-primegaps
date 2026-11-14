#!/usr/bin/env bash
# Second independent rerun of openai/PrimeGaps186. Runs inside the isolated VM; writes everything to /out.
set -uo pipefail
OUT=/out; W=$HOME/work; mkdir -p "$W"
COMMIT=61340d0b74163003b32756bb16e91d9209a5e330
FLINT_FIX=7ad753d51c82fdec115cb179b41d0e581f1cb0ec
export PATH=$HOME/.elan/bin:$HOME/.cargo/bin:/usr/local/go/bin:$HOME/go/bin:$HOME/.local/bin:$PATH
log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a $OUT/progress.log; }
step() { local id=$1; shift; log "START $id"; /usr/bin/time -v -o $OUT/$id.time bash -c "$*" > $OUT/$id.log 2>&1; local rc=$?; echo $rc > $OUT/$id.rc; log "END $id rc=$rc wall=$(grep 'Elapsed (wall' $OUT/$id.time | awk '{print $NF}') maxRSS_kB=$(grep 'Maximum resident' $OUT/$id.time | awk '{print $NF}')"; return $rc; }

log "=== rerun start"
sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq time >/dev/null || { log "cannot install time"; exit 1; }
step S0_provision '
  sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq build-essential git curl python3 python3-venv pkg-config libssl-dev time jq unzip autoconf automake libtool libgmp-dev libmpfr-dev
  curl -sSfL https://go.dev/dl/go1.25.4.linux-arm64.tar.gz | sudo tar -C /usr/local -xz
  curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
  curl -sSfL https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none
  curl -LsSf https://astral.sh/uv/install.sh | sh
  git config --global user.email rerun@localhost; git config --global user.name rerun' || { log "ABORT after S0_provision"; exit 1; }
{ uname -a; nproc; free -g; go version; rustc --version; elan --version; uv --version; } > $OUT/environment.txt 2>&1

step S1_source "cd $W && git clone -q https://github.com/openai/PrimeGaps186.git && cd PrimeGaps186 && git checkout -q $COMMIT && git rev-parse HEAD && sha256sum Challenge.lean prime_gap_186_certificate.py" || { log "ABORT after S1_source"; exit 1; }

step C1_tuple "cd $W/PrimeGaps186 && python3 - <<'PY'
import re
src = open('Challenge.lean').read()
nums = None
for m in re.finditer(r'[\[{]([0-9,\s]+)[\]}]', src):
    xs = [int(x) for x in m.group(1).replace('\n',' ').split(',') if x.strip()]
    if len(xs) == 40: nums = xs; break
assert nums, 'no 40-element list found'
primes = [p for p in range(2, 41) if all(p % d for d in range(2, p))]
adm = all(len({h % p for h in nums}) < p for p in primes)
print({'n': len(set(nums)), 'diameter': max(nums) - min(nums), 'admissible': adm, 'tuple': nums})
assert len(set(nums)) == 40 and max(nums) - min(nums) == 186 and adm
PY"

step C4_build "cd $W/PrimeGaps186 && cat lean-toolchain && lake exe cache get && lake build PrimeGaps186" || { log "ABORT after C4_build"; exit 1; }
grep -ci warning $OUT/C4_build.log > $OUT/C4_warnings.txt; grep -ci error $OUT/C4_build.log > $OUT/C4_errors.txt

step C5_tools "cd $W && git clone -q https://github.com/Zouuup/landrun.git && (cd landrun && git rev-parse HEAD && go build -o \$HOME/go/bin/landrun ./cmd/landrun) && git clone -q https://github.com/ammkrn/nanoda_lib.git && (cd nanoda_lib && git rev-parse HEAD && cargo build --release -q) && cd PrimeGaps186 && lake build lean4export/lean4export && lake build Comparator/comparator"

step C5_comparator "cd $W/PrimeGaps186 && export COMPARATOR_LEAN4EXPORT=\$(find .lake/packages/lean4export -type f -name lean4export -perm -u+x | head -1 | xargs realpath) COMPARATOR_LANDRUN=\$HOME/go/bin/landrun COMPARATOR_NANODA=$W/nanoda_lib/target/release/nanoda_bin XDG_RUNTIME_DIR=/run/user/\$(id -u) && systemd-run --property=RestrictAddressFamilies=~AF_UNIX --user --pipe --wait -E PATH -E COMPARATOR_LEAN4EXPORT -E COMPARATOR_LANDRUN -E COMPARATOR_NANODA --working-directory \$PWD -- lake exe comparator comparator/main.json"

step C5_axioms "cd $W/PrimeGaps186 && printf 'import PrimeGaps186\n#print axioms PrimeGap186.dhl_40_2\n#print axioms PrimeGap186.infinite_two_prime_translates_admissibleTuple\n#print axioms PrimeGap186.primeGapLiminf_le_186\n' > /tmp/Axioms.lean && lake env lean /tmp/Axioms.lean"

step C6_stock_flint "uv venv -q --python 3.12 $W/venv-stock && uv pip install -q --python $W/venv-stock/bin/python python-flint==0.9.0 numpy==2.2.6 && $W/venv-stock/bin/python /out/probe_flint.py"

step C8_fixed_flint "cd $W && git clone -q https://github.com/flintlib/flint.git flint-360 && cd flint-360 && git checkout -q v3.6.0 && git cherry-pick -x $FLINT_FIX && ./bootstrap.sh && ./configure --prefix=$W/flint-360fix --disable-static && make -j\$(nproc) && make install && uv venv -q --python 3.12 $W/venv-fixed && PFX=$W/flint-360fix PKG_CONFIG_PATH=$W/flint-360fix/lib/pkgconfig CFLAGS=-I$W/flint-360fix/include LDFLAGS='-L$W/flint-360fix/lib -Wl,-rpath,$W/flint-360fix/lib' uv pip install --python $W/venv-fixed/bin/python --no-binary python-flint python-flint==0.9.0 numpy==2.2.6 && $W/venv-fixed/bin/python -c 'import flint; print(flint.__version__, flint.__FLINT_VERSION__)' && $W/venv-fixed/bin/python /out/probe_flint.py" || { log "ABORT after C8_fixed_flint"; exit 1; }

step C9_certificate "cd $W/PrimeGaps186 && unset PYTHONOPTIMIZE && $W/venv-fixed/bin/python -B prime_gap_186_certificate.py --workers 4 --output /out/prime_gap_186_fresh.json"
log "=== rerun done"
