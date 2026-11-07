set -uxo pipefail
export PATH=$HOME/.local/bin:$PATH
D=$HOME/work/cycle6; PFX=$HOME/work/flint-fixed; cd $HOME/work/flint
git checkout -q v3.6.0 && git cherry-pick -x 7ad753d51c82fdec115cb179b41d0e581f1cb0ec > $D/C8.log 2>&1
if [ $? -ne 0 ]; then echo "cherry-pick failed; falling back to main" >> $D/C8.log; git cherry-pick --abort; git checkout -q 140103bf597dc9d7561ccb1e9f516b2b71729bff; fi
git log -1 --format="flint_commit=%H %s" >> $D/C8.log; git describe --tags --always >> $D/C8.log
./bootstrap.sh >> $D/C8.log 2>&1 && ./configure --prefix=$PFX --disable-static >> $D/C8.log 2>&1 && make -j20 >> $D/C8.make.log 2>&1 && make install >> $D/C8.log 2>&1; echo "flint_build_exit=$?" >> $D/C8.log
uv venv -q --python 3.12 $HOME/work/venv-flint-fixed
export PKG_CONFIG_PATH=$PFX/lib/pkgconfig CFLAGS="-I$PFX/include" LDFLAGS="-L$PFX/lib -Wl,-rpath,$PFX/lib"
uv pip install --python $HOME/work/venv-flint-fixed/bin/python --no-binary python-flint "python-flint==0.9.0" "numpy==2.2.6" >> $D/C8.pip.log 2>&1; echo "pyflint_build_exit=$?" >> $D/C8.log
P=$HOME/work/venv-flint-fixed/bin/python
$P -c "import flint; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, flint.__file__)" >> $D/C8.log 2>&1
$P /tmp/probe_flint.py > $D/C8.json 2>> $D/C8.log; echo "probe_exit=$?" >> $D/C8.log
touch $D/C8.done
