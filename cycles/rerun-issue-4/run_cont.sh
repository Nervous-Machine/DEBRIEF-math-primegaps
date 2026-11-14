#!/usr/bin/env bash
# Continuation after C8 attempt 1 failed (python3-dev missing for the python-flint source build).
set -uo pipefail
OUT=/out; W=$HOME/work
export PATH=$HOME/.elan/bin:$HOME/.cargo/bin:/usr/local/go/bin:$HOME/go/bin:$HOME/.local/bin:$PATH
log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a $OUT/progress.log; }
step() { local id=$1; shift; log "START $id"; /usr/bin/time -v -o $OUT/$id.time bash -c "$*" > $OUT/$id.log 2>&1; local rc=$?; echo $rc > $OUT/$id.rc; log "END $id rc=$rc wall=$(grep 'Elapsed (wall' $OUT/$id.time | awk '{print $NF}') maxRSS_kB=$(grep 'Maximum resident' $OUT/$id.time | awk '{print $NF}')"; return $rc; }
log "=== continuation (deviation D1: installed python3-dev, rebuilt python-flint against existing FLINT 3.6.0+7ad753d)"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-dev >/dev/null
step C8_fixed_flint "ls $W/flint-360fix/lib/libflint* && cd $W/flint-360 && git log --oneline -2 && rm -rf $W/venv-fixed && uv venv -q --python /usr/bin/python3.12 $W/venv-fixed && PKG_CONFIG_PATH=$W/flint-360fix/lib/pkgconfig CFLAGS=-I$W/flint-360fix/include LDFLAGS='-L$W/flint-360fix/lib -Wl,-rpath,$W/flint-360fix/lib' uv pip install --python $W/venv-fixed/bin/python --no-binary python-flint python-flint==0.9.0 numpy==2.2.6 && $W/venv-fixed/bin/python -c 'import flint; print(flint.__version__, flint.__FLINT_VERSION__)' && $W/venv-fixed/bin/python /out/probe_flint.py" || { log "ABORT after C8_fixed_flint"; exit 1; }
step C9_certificate "cd $W/PrimeGaps186 && unset PYTHONOPTIMIZE && $W/venv-fixed/bin/python -B prime_gap_186_certificate.py --workers 4 --output /out/prime_gap_186_fresh.json"
log "=== rerun done"
