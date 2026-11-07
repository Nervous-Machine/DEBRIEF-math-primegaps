set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y -qq build-essential git curl python3 python3-venv python3-pip pkg-config libssl-dev time jq unzip >/dev/null
# recent Go (landrun) and Rust (nanoda)
GOV=$(curl -sSL 'https://go.dev/VERSION?m=text' | head -1)
curl -sSL "https://go.dev/dl/${GOV}.linux-arm64.tar.gz" -o /tmp/go.tgz && sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf /tmp/go.tgz
curl -sSf https://sh.rustup.rs | sh -s -- -y -q --profile minimal >/dev/null
curl -sSfL https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none >/dev/null
cat >> ~/.bashrc <<'EOF'
export PATH=$HOME/.elan/bin:$HOME/.cargo/bin:/usr/local/go/bin:$HOME/go/bin:$PATH
EOF
export PATH=$HOME/.elan/bin:$HOME/.cargo/bin:/usr/local/go/bin:$HOME/go/bin:$PATH
mkdir -p ~/work ~/work/cycle6 && cd ~/work
git clone -q https://github.com/openai/PrimeGaps186.git && cd PrimeGaps186 && git checkout -q 61340d0b74163003b32756bb16e91d9209a5e330
echo "b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0  Challenge.lean" | sha256sum -c -
git rev-parse HEAD > ~/work/cycle6/source_commit.txt
{ uname -a; nproc; free -g | head -2; go version; rustc --version; elan --version; python3 --version; } | tee ~/work/cycle6/environment.txt
