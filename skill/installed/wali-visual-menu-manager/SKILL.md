---
name: wali-visual-menu-manager
description: 管理 Wali 的可视化菜单（Telegram按钮菜单）。用于查看/调整一级二级菜单结构、维护 callback 路由、预览按钮 payload，并同步到聊天菜单。适用于菜单重构、分组整理、按钮文案调整、回调动作扩展等场景。
---

# Wali Visual Menu Manager

## 目标
统一管理 Wali 的可视化菜单配置与交互入口。

## 核心文件
- `config/visual-menu.json`：菜单主配置（节点、按钮、回调）
- `scripts/menu_payload_preview.py`：预览 Telegram 按钮 payload
- `config/wali-config.md`：文字菜单说明
- `config/menu-structure.md`：层级结构文档

## 相关能力（已实现）
1. 一级/二级菜单数据驱动配置
2. callback 规范：
   - 导航：`nav:<node>`
   - 动作：`act:<domain.action>`
3. 主菜单按钮预览与快速验证
4. Skill 分组管理入口联动（`skill_group_mgmt`）

## 使用步骤

### 1) 修改菜单结构
编辑：`config/visual-menu.json`
- root.rows 调整一级菜单布局
- nodes.<id> 调整二级菜单按钮

### 2) 预览按钮载荷
```bash
python3 scripts/menu_payload_preview.py
```

### 3) 同步文档说明
按需更新：
- `config/wali-config.md`
- `config/menu-structure.md`

### 4) 发送到 Telegram 测试
发送主菜单后，通过 `nav:*` / `act:*` 做联调。

## 设计约束
- 按钮文案尽量短，避免 Telegram 折行难读
- 一行 2 个按钮优先，必要时单按钮独占一行
- 所有二级菜单都保留“返回主菜单”
- 变更优先改 `visual-menu.json`，脚本与文档随之同步

## 扩展建议
- 增加 node 层级权限（危险操作二次确认）
- 增加动态状态按钮（运行中/停止）
- 增加回调路由注册表（自动校验未实现 action）
