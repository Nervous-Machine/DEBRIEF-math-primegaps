set -uxo pipefail
export PATH=$HOME/.local/bin:$PATH
D=$HOME/work/cycle6; PFX=$HOME/work/flint-360fix
while [ ! -f $D/C8b.done ]; do sleep 15; done
echo "python-flint build against $PFX $(date -u +%FT%TZ)" >> $D/C8b.log
rm -rf $HOME/work/venv-flint-fixed; uv venv -q --python 3.12 $HOME/work/venv-flint-fixed
export PKG_CONFIG_PATH=$PFX/lib/pkgconfig CFLAGS="-I$PFX/include" LDFLAGS="-L$PFX/lib -Wl,-rpath,$PFX/lib"
PKG_CONFIG_PATH=$PFX/lib/pkgconfig pkg-config --modversion flint >> $D/C8b.log
uv pip install --python $HOME/work/venv-flint-fixed/bin/python --no-binary python-flint "python-flint==0.9.0" "numpy==2.2.6" > $D/C8b.pip.log 2>&1; echo "pyflint_build_exit=$?" >> $D/C8b.log
P=$HOME/work/venv-flint-fixed/bin/python
$P -c "import flint; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__)" >> $D/C8b.log 2>&1
$P -c "import flint, ctypes, glob, os; print([l for l in open('/proc/self/maps').read().split() if 'libflint' in l][:1])" >> $D/C8b.log 2>&1
$P /tmp/probe_flint.py > $D/C8.json 2>> $D/C8b.log; echo "probe_exit=$?" >> $D/C8b.log
touch $D/C8.done2
