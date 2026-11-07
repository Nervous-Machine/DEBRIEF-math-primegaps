set -uxo pipefail
export PATH=$HOME/.cargo/bin:/usr/local/go/bin:$HOME/go/bin:$PATH
D=$HOME/work/cycle6; cd $HOME/work
git clone -q https://github.com/Zouuup/landrun.git && cd landrun && git rev-parse HEAD > $D/landrun_commit.txt && (go build -o $HOME/go/bin/landrun ./cmd/landrun || go build -o $HOME/go/bin/landrun .) > $D/tools.log 2>&1; echo "landrun_build_exit=$?" >> $D/tools.log
cd $HOME/work && git clone -q https://github.com/ammkrn/nanoda_lib.git && cd nanoda_lib && git rev-parse HEAD > $D/nanoda_commit.txt && cargo build --release -q >> $D/tools.log 2>&1; echo "nanoda_build_exit=$?" >> $D/tools.log
ls -la $HOME/go/bin/landrun $HOME/work/nanoda_lib/target/release/nanoda_bin >> $D/tools.log 2>&1
touch $D/tools.done
