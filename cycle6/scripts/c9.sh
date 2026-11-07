set -uxo pipefail
D=$HOME/work/cycle6; cd $HOME/work/PrimeGaps186
P=$HOME/work/venv-flint-fixed/bin/python
unset PYTHONOPTIMIZE
echo "start $(date -u +%FT%TZ)" > $D/C9.log
$P -c "import flint, numpy, sys; print('python', sys.version.split()[0], 'python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__)" >> $D/C9.log 2>&1
sha256sum prime_gap_186_certificate.py >> $D/C9.log
/usr/bin/time -v $P -B prime_gap_186_certificate.py --workers 20 --output $D/prime_gap_186_fresh.json > $D/C9.run.log 2>&1; echo "certificate_exit=$? $(date -u +%FT%TZ)" >> $D/C9.log
grep -E "Elapsed|Maximum resident" $D/C9.run.log >> $D/C9.log
python3 -c "import json,sys; r=json.load(open('$D/prime_gap_186_fresh.json')); print('passed=', r.get('passed'), 'elapsed_seconds=', r.get('elapsed_seconds'), 'keys=', list(r)[:15])" >> $D/C9.log 2>&1
touch $D/C9.done
