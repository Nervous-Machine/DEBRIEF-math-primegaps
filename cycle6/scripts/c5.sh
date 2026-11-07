set -uxo pipefail
export PATH=$HOME/.elan/bin:$HOME/go/bin:$HOME/work/nanoda_lib/target/release:$PATH
D=$HOME/work/cycle6; cd $HOME/work/PrimeGaps186
echo "start $(date -u +%FT%TZ)" > $D/C5.log
# build the pinned lean4export and comparator executables from the repo's own lake dependencies
(lake build lean4export/lean4export || lake build @lean4export || lake build lean4export) > $D/C5.build.log 2>&1; echo "lean4export_build_exit=$?" >> $D/C5.log
L4E=$(find .lake/packages/lean4export -type f -name lean4export -perm -u+x | head -1); echo "lean4export_bin=$L4E" >> $D/C5.log
(lake build Comparator/comparator || lake build @Comparator || lake build comparator) >> $D/C5.build.log 2>&1; echo "comparator_build_exit=$?" >> $D/C5.log
CMP=$(find .lake/packages/Comparator -type f -name comparator -perm -u+x | head -1); echo "comparator_bin=$CMP" >> $D/C5.log
export COMPARATOR_LEAN4EXPORT=$PWD/$L4E COMPARATOR_LANDRUN=$HOME/go/bin/landrun COMPARATOR_NANODA=$HOME/work/nanoda_lib/target/release/nanoda_bin
{ landrun --version; $COMPARATOR_NANODA --version; $COMPARATOR_LEAN4EXPORT --help 2>&1 | head -2; } >> $D/C5.log 2>&1
export XDG_RUNTIME_DIR=/run/user/$(id -u)
# README-recommended wrapper; --pipe/--wait instead of --pty because there is no terminal
systemd-run --property=RestrictAddressFamilies=~AF_UNIX --user --pipe --wait -E PATH="$PATH" -E COMPARATOR_LEAN4EXPORT -E COMPARATOR_LANDRUN -E COMPARATOR_NANODA --working-directory "$PWD" -- bash -c 'lake exe comparator comparator/main.json' > $D/C5.comparator.log 2>&1
RC=$?; echo "comparator_exit=$RC $(date -u +%FT%TZ)" >> $D/C5.log
if [ $RC -ne 0 ] && grep -q -i "systemd-run\|Failed to connect to bus\|No such file" $D/C5.comparator.log; then
  echo "systemd-run wrapper unavailable; rerunning without it (landrun sandbox still applies)" >> $D/C5.log
  lake exe comparator comparator/main.json > $D/C5.comparator.nosystemd.log 2>&1; echo "comparator_exit_nosystemd=$? $(date -u +%FT%TZ)" >> $D/C5.log
fi
touch $D/C5.done
