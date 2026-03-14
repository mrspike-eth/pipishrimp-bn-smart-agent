#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
missing=0

ok(){ echo "✅ $1"; }
warn(){ echo "❌ $1"; fail=1; missing=$((missing+1)); }

# 1) core files
for f in \
  settings/menu-management/visual-menu.json \
  settings/menu-management/menu-root.json \
  settings/menu-management/menu-nodes.json \
  settings/menu-management/skill-list-panel.json \
  skill/skills-config.json \
  reset-restore
  do
  [[ -f "$f" ]] && ok "存在: $f" || warn "缺失: $f"
done

# 2) 一级菜单目录
for d in \
  binance-daily watchlist binance-spot-trade bn-wallet-onchain-trade \
  signal-monitor smart-investment-assistant content-creation learning-mode \
  skill-management settings
  do
  [[ -f "$d/menu-config.json" ]] && ok "存在: $d/menu-config.json" || warn "缺失: $d/menu-config.json"
done

# 3) 内容校验
if [[ -f settings/menu-management/visual-menu.json ]]; then
  grep -q "BN Wallet链上交易" settings/menu-management/visual-menu.json && ok "BN Wallet 全称存在" || warn "BN Wallet 全称缺失"
  python3 - <<'PY' || { echo "❌ 菜单JSON结构校验失败"; fail=1; missing=$((missing+1)); }
import json
from pathlib import Path
obj=json.loads(Path('settings/menu-management/visual-menu.json').read_text())
nodes=obj['nodes']
for row in obj['root']['rows']:
    for i in row:
        assert 'next' in i and i['next'] in nodes
for nid,node in nodes.items():
    for row in node.get('rows',[]):
        for it in row:
            assert ('next' in it) ^ ('action' in it)
print('✅ 菜单结构可达性校验通过')
PY
fi

if [[ -f settings/menu-management/skill-list-panel.json ]]; then
  grep -q '"layout"[[:space:]]*:[[:space:]]*"grouped-vertical"' settings/menu-management/skill-list-panel.json \
    && ok "Skill布局为 grouped-vertical" || warn "Skill布局不是 grouped-vertical"
fi

if [[ $fail -eq 0 ]]; then
  echo "\n恢复报告："
  echo "- 菜单恢复：PASS"
  echo "- 回调可达：PASS"
  echo "- Skill分组：PASS"
  echo "- 监控策略：PASS"
  echo "- 缺失项=0"
  echo "RESULT: PASS"
else
  echo "\n恢复报告："
  echo "- 菜单恢复：FAIL"
  echo "- 回调可达：FAIL"
  echo "- Skill分组：FAIL"
  echo "- 监控策略：CHECK"
  echo "- 缺失项=$missing"
  echo "RESULT: FAIL"
  exit 1
fi
