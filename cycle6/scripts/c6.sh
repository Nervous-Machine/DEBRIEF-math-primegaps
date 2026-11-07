set -euo pipefail
curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
export PATH=$HOME/.local/bin:$PATH
uv venv -q --python 3.12 $HOME/work/venv-flint
uv pip install -q --python $HOME/work/venv-flint/bin/python "python-flint==0.9.0" "numpy==2.2.6"
$HOME/work/venv-flint/bin/python -c "import flint, numpy, sys; print('python', sys.version.split()[0], 'python-flint', flint.__version__, 'numpy', numpy.__version__)"
$HOME/work/venv-flint/bin/python /tmp/probe_flint.py | tee $HOME/work/cycle6/C6.json
