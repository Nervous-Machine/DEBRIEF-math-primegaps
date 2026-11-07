set -uxo pipefail
export PATH=$HOME/.elan/bin:$PATH
D=$HOME/work/cycle6; cd $HOME/work/PrimeGaps186
{ echo "start $(date -u +%FT%TZ)"; cat lean-toolchain; } > $D/C4.log 2>&1
/usr/bin/time -v lake exe cache get > $D/C4.cache.log 2>&1; echo "cache_get_exit=$? $(date -u +%FT%TZ)" >> $D/C4.log
lean --version >> $D/C4.log 2>&1; lake --version >> $D/C4.log 2>&1
/usr/bin/time -v lake build PrimeGaps186 > $D/C4.build.log 2>&1; echo "build_exit=$? $(date -u +%FT%TZ)" >> $D/C4.log
echo "warning_lines=$(grep -c -i 'warning' $D/C4.build.log)" >> $D/C4.log
echo "error_lines=$(grep -c -i 'error' $D/C4.build.log)" >> $D/C4.log
grep -E "Elapsed|Maximum resident" $D/C4.build.log >> $D/C4.log
touch $D/C4.done
