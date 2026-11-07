set -uxo pipefail
D=$HOME/work/cycle6; PFX=$HOME/work/flint-360fix
git config --global user.email "debrief@nervousmachine.local"; git config --global user.name "NM DEBRIEF rerun"
cd $HOME/work && rm -rf flint-360 && git clone -q https://github.com/flintlib/flint.git flint-360 && cd flint-360
git checkout -q v3.6.0 && git cherry-pick -x 7ad753d51c82fdec115cb179b41d0e581f1cb0ec > $D/C8b.log 2>&1; echo "cherry_pick_exit=$?" >> $D/C8b.log
git log -2 --format="flint_commit=%H %s" >> $D/C8b.log; git status --short | head >> $D/C8b.log
./bootstrap.sh > /dev/null 2>&1 && ./configure --prefix=$PFX --disable-static > $D/C8b.configure.log 2>&1 && make -j16 > $D/C8b.make.log 2>&1 && make install > /dev/null 2>&1; echo "flint_build_exit=$?" >> $D/C8b.log
ls $PFX/lib >> $D/C8b.log
touch $D/C8b.done
