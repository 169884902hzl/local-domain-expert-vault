# Maintainer Checklist

本清单主要给原维护者从完整本地工作目录重新发布时使用。普通 GitHub 使用者只需要按 `README.md` 和 `docs/GETTING_STARTED.md` 打开仓库根目录。

## 发布前

- [ ] 重新生成 `exports/github-ready-vault-YYYYMMDD/`。
- [ ] 确认发布包内没有 `.claude/backups/`、`.claude/logs/`、`.claudian/sessions/`、`.smart-env/`、`attachments/`、PDF 缓存和 SQLite 数据库。
- [ ] 运行高置信 secrets 扫描。
- [ ] 运行核心 Python 编译检查。
- [ ] 在发布包内运行 `audit_kb.py`。
- [ ] 在发布包内运行一次 `kb_search.py`。
- [ ] 检查 `README.md` 的快速开始命令仍然正确。

## 发布后

- [ ] 在 GitHub 网页检查文件列表，不应出现本机备份、会话日志、API key、PDF 缓存。
- [ ] 在干净目录 clone 一次，打开 Obsidian 验证 `wiki/`、Graph、Dashboard。
- [ ] 如果发现 key 曾进入 git history，立即删除仓库或重写历史，并轮换 key。

## 可接受的公开内容

- `wiki/` 结构化知识层。
- `.claude/commands/` 和公开脚本。
- `.claude/agents/`、`.claude/skills/`。
- `.claudian/claudian-settings.json` 的脱敏版本。
- `.obsidian/` 的必要配置，但不含 workspace runtime。
- `templates/`、`SCHEMA.md`、`Dashboard.md`、`CLAUDE.md`、`AGENTS.md`。
