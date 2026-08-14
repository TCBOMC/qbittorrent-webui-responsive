<div align="center">

# 📱 qBittorrent WebUI Responsive

**qBittorrent WebUI 桌面/移动端自动分流工具**

自动识别手机 / 平板 / 浏览器设备模拟，并进入独立的移动版 WebUI

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

</div>

---

## 🎯 这是什么

**qBittorrent WebUI Responsive** 为 qBittorrent Alternative WebUI 增加桌面/移动端自动分流功能。

访问 WebUI 时自动判断当前环境：

```text
手机 / 平板       → 移动版 WebUI
电脑              → 原桌面版 WebUI
浏览器设备模拟    → 移动版 WebUI
```

> 💡 **推荐配合我的另一个项目使用：**
>
> [**qbittorrent-webui-i18n**](https://github.com/TCBOMC/qbittorrent-webui-i18n)
>
> 先使用 `qbittorrent-webui-i18n` 对官方 WebUI 进行多语言预处理，再使用本项目添加桌面/移动端 UI 分流，可以同时获得**多语言支持 + 独立移动端 UI**。

---

## ✨ 核心功能

- **自动设备检测** — 支持手机、平板及桌面设备
- **CSS 逻辑像素检测** — 不依赖固定手机分辨率
- **DevTools 模拟支持** — 支持 Firefox / Chrome 手机设备模拟
- **双入口支持** — `private/` 和 `public/` 同时注入检测器
- **自动复制 UI** — 自动部署到 `private/webui/` 和 `public/webui/`
- **自动备份** — 修改入口文件前自动创建备份
- **可重复执行** — 自动清理旧注入代码，不会重复添加
- **调试信息** — 控制台输出完整的检测依据和最终判断结果

---

## 🚀 快速开始

### 1. 准备目录

将移动版 UI 放入 `webui/`：

```text
root/
├── private/
│   └── index.html
├── public/
│   └── index.html
├── webui/
│   └── your-mobile-ui/
│       └── index.html
└── editui.py
```

### 2. 运行

```bash
python3 editui.py your-mobile-ui
```

脚本会自动：

```text
webui/your-mobile-ui/
        │
        ├──→ private/webui/your-mobile-ui/
        └──→ public/webui/your-mobile-ui/

private/index.html  ← 注入检测器
public/index.html   ← 注入检测器
private/webui/your-mobile-ui/index.html  ← 注入检测器
public/webui/your-mobile-ui/index.html  ← 注入检测器
```

处理完成后即可将项目根目录作为 qBittorrent Alternative WebUI 使用。

---

## 🔍 检测方式

检测器综合使用以下信息：

### User-Agent

支持：

```text
Android
iPhone / iPad / iPod
Windows Phone
webOS / BlackBerry
Mobile / Tablet / Mobi
```

### CSS 逻辑像素

默认使用网页实际 viewport 判断：

```text
短边 ≤ 600px
```

例如：

```text
390 × 844  → Mobile
412 × 915  → Mobile
600 × 960  → Mobile
800 × 1280 → Desktop
```

### 浏览器设备模拟

针对 Firefox / Chrome DevTools 的设备模拟模式，额外检测：

```text
Screen / Viewport 比例
```

因此即使：

```text
Desktop UA
maxTouchPoints = 0
```

也可以识别浏览器正在模拟移动设备的情况。

---

## 🧪 调试

打开浏览器 F12 → Console，可以看到：

```text
qBittorrent Mobile UI Detector

Viewport (CSS px): 390 × 844
Screen (CSS px): 390 × 844
Device Pixel Ratio: 1

mobileUA: false
mobileKeywordUA: false
responsiveMobileViewport: true

RESULT: MOBILE

DECISION REASONS:
  • mobile-sized CSS viewport
```

可以直接查看**当前设备类型以及触发判断的具体原因**。

---

## 📂 处理后的目录

```text
root/
├── private/
│   ├── index.html              # 注入移动检测
│   └── webui/
│       └── your-mobile-ui/
│
├── public/
│   ├── index.html              # 注入移动检测
│   └── webui/
│       └── your-mobile-ui/
│
├── webui/
│   └── your-mobile-ui/    # 原始移动 UI
│
└── editui.py
```

`private/` 和 `public/` 使用相同的移动 UI，不需要单独维护两套移动登录页面。

---

## ⚠️ 注意事项

- 请修改 `webui/` 中的原始 UI，不要直接修改生成后的 `private/webui/` 或 `public/webui/`
- 脚本每次运行都会重新复制指定 UI
- UI 名称必须是 `webui/` 下的一级目录，例如：

```bash
python3 editui.py your-mobile-ui
```

---

## 🔗 推荐项目

### 🌐 [qbittorrent-webui-i18n](https://github.com/TCBOMC/qbittorrent-webui-i18n)

qBittorrent WebUI 国际化预处理工具。

```text
官方 WebUI
    │
    ▼
qbittorrent-webui-i18n
    │
    ▼
多语言 WebUI
    │
    ▼
qBittorrent WebUI Responsive
    │
    ├──→ Desktop UI
    └──→ Mobile UI
```

---

## 📄 许可证

GPLv3

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个 Star！**

</div>
