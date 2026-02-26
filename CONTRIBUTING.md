# 贡献指南

## 文档与 GitHub Pages

本站文档由 [mike](https://github.com/jimporter/mike) 做多版本管理，发布在 GitHub Pages 分支 `gh-pages`。

- **根路径** [https://caiyunapp.github.io/aqi-hub/](https://caiyunapp.github.io/aqi-hub/) 会跳转到默认版本 `latest`。
- **版本路径**：`/latest/`（main）、`/develop/`（develop 分支）、`/0.2.1/`、`/0.3.0/` 等，可在页面顶栏版本选择器中切换。

### 本地预览

- **单版本**：`make docs-serve`（需先 `uv sync --group dev`）。
- **多版本**（与线上一致的版本选择器）：`make docs-serve-versioned`。详见 Makefile 中 `docs-serve-versioned` 目标上方的注释。

### 维护 Pages（首次或检查时）

在仓库 **Settings → Pages** 中：

- **Source**：Deploy from a branch  
- **Branch**：gh-pages  
- **目录**：/ (root)  

推送至 `main` / `develop` 或打 tag `v*` 后，由 workflow 自动构建并推送到 `gh-pages`，无需手动发布。
