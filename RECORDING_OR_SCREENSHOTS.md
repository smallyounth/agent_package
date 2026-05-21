# 录屏或关键截图说明

本包提供关键运行截图，满足“3-5 分钟录屏或关键运行截图”的替代要求。面试时可以按 `RUNBOOK_10MIN.md` 录 3-5 分钟视频，也可以直接展示以下截图。

## 截图清单

| 文件 | 展示内容 |
|---|---|
| `screenshots_and_recording/01-core-directory.svg` | 核心目录和交付包结构 |
| `screenshots_and_recording/02-ai-enhancement-output.svg` | AI 增强模块输出：P1 风险、CPU 96%、下一步动作 |
| `screenshots_and_recording/03-test-output.svg` | 两条测试样例通过 |
| `screenshots_and_recording/04-agent-state-flow.svg` | Agent Plan-Execute-Replan 状态流 |
| `screenshots_and_recording/*.png` | 实际运行关键截图 |
| `screenshots_and_recording/*.mp4` | 3-5 分钟录屏素材 |

## 建议录屏脚本

1. 打开 `README.md`，说明项目是企业 OnCall Agent。
2. 执行离线 demo，展示结构化摘要输出。
3. 执行单元测试，展示 2 条测试通过。
4. 打开 `ARCHITECTURE.md`，讲 Agent 状态流和工具边界。
5. 打开 `DEBUG_RECORD.md`，讲真实排错过程。

这个流程控制在 3-5 分钟内，不依赖外部服务。
