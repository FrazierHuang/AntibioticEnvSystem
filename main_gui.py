import sys, os, subprocess, threading
from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QTextEdit, QProgressBar, QLineEdit, QTabWidget, QMessageBox, QFrame
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

APP_TITLE = "环境抗生素污染分析系统 v1.0"
LOGO_PATH = "icon.png"  # 你生成的蓝绿显微镜图标（1024x1024 PNG）

class Worker(QObject):
    finished = pyqtSignal(int)
    log = pyqtSignal(str)
    progress = pyqtSignal(int)

    def run_pipeline(self, data_file, out_dir):
        try:
            env = os.environ.copy()
            env["DATA_FILE"] = data_file
            env["OUT_DIR"] = out_dir
            cmd = f'"{sys.executable}" run_all.py'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
            p = 5
            for line in proc.stdout:
                self.log.emit(line.rstrip())
                p = min(p + 2, 95)
                self.progress.emit(p)
            ret = proc.wait()
            self.progress.emit(100)
            self.finished.emit(0 if ret == 0 else 1)
        except Exception as e:
            self.log.emit(f"[ERROR] {e}")
            self.finished.emit(1)

class ImageCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(5, 3), dpi=100)
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.ax.axis("off")

    def show_png(self, path):
        self.ax.clear()
        self.ax.axis("off")
        if Path(path).exists():
            img = Image.open(path)
            self.ax.imshow(img)
        else:
            self.ax.text(0.5, 0.5, f"图片未找到\n{path}", ha="center", va="center", fontsize=10, color="white")
        self.draw()

class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = True  # 默认夜间主题
        self.initUI()
        self.apply_theme()

    def initUI(self):
        self.setWindowTitle(APP_TITLE)
        self.resize(960, 680)

        # === 顶部栏：logo + 标题 + 主题切换 === #
        topbar = QFrame()
        topbar.setObjectName("titleBar")
        hl = QHBoxLayout(topbar)
        hl.setContentsMargins(10, 5, 10, 5)
        if Path(LOGO_PATH).exists():
            logo = QLabel()
            pix = QPixmap(LOGO_PATH).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo.setPixmap(pix)
            hl.addWidget(logo)
        title = QLabel(APP_TITLE)
        title.setObjectName("titleText")
        hl.addWidget(title)
        hl.addStretch()
        self.theme_btn = QPushButton("🌙 夜间")
        self.theme_btn.clicked.connect(self.toggle_theme)
        hl.addWidget(self.theme_btn)

        # === 文件选择区 === #
        top = QHBoxLayout()
        self.in_edit = QLineEdit()
        self.in_edit.setPlaceholderText("选择输入数据文件 (CSV / Excel)")
        btn_in = QPushButton("📂 浏览")
        btn_in.clicked.connect(self.select_input)
        self.out_edit = QLineEdit()
        self.out_edit.setPlaceholderText("选择输出目录 (默认 ./outputs)")
        btn_out = QPushButton("📁 输出")
        btn_out.clicked.connect(self.select_output)
        top.addWidget(self.in_edit, 2); top.addWidget(btn_in, 1)
        top.addWidget(self.out_edit, 2); top.addWidget(btn_out, 1)

        # === 控制按钮 === #
        ctrl = QHBoxLayout()
        self.btn_run = QPushButton("▶️ 开始分析")
        self.btn_run.clicked.connect(self.start_run)
        self.btn_open = QPushButton("📊 打开结果目录")
        self.btn_open.clicked.connect(self.open_output)
        ctrl.addWidget(self.btn_run); ctrl.addWidget(self.btn_open)

        # === 进度条 === #
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # === 日志框 === #
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("运行日志将在此显示...")

        # === 图表 Tab === #
        self.tabs = QTabWidget()
        self.canvas1 = ImageCanvas(); self.tabs.addTab(self.canvas1, "时序趋势")
        self.canvas2 = ImageCanvas(); self.tabs.addTab(self.canvas2, "风险矩阵")
        self.canvas3 = ImageCanvas(); self.tabs.addTab(self.canvas3, "超标比例")
        self.canvas4 = ImageCanvas(); self.tabs.addTab(self.canvas4, "环境参数 / 季节性")

        # === 主布局 === #
        v = QVBoxLayout(self)
        v.addWidget(topbar)
        v.addLayout(top)
        v.addLayout(ctrl)
        v.addWidget(self.progress)
        v.addWidget(QLabel("运行日志："))
        v.addWidget(self.log, 1)
        v.addWidget(QLabel("图表预览："))
        v.addWidget(self.tabs, 3)

    # === 主题切换 === #
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.theme_btn.setText("☀️ 日间")
            self.setStyleSheet(self.dark_theme())
        else:
            self.theme_btn.setText("🌙 夜间")
            self.setStyleSheet(self.light_theme())

    # === 深色主题样式 === #
    def dark_theme(self):
        return """
        QWidget { background-color: #1E1F26; color: #E0E0E0; font-family: 'PingFang SC', Arial; }
        QLineEdit, QTextEdit {
            background-color: #2B2D3A; color: #F5F5F5; border: 1px solid #4C566A; border-radius: 6px; padding: 6px;
        }
        QPushButton {
            background-color: #2196F3; color: white; border-radius: 8px; padding: 8px 14px; font-weight: 500;
        }
        QPushButton:hover { background-color: #42A5F5; }
        QProgressBar {
            border: 1px solid #4C566A; border-radius: 6px; text-align: center; background-color: #2B2D3A;
        }
        QProgressBar::chunk { background-color: #66BB6A; }
        QTabBar::tab {
            background: #2B2D3A; color: #E0E0E0; padding: 6px 12px; border-radius: 4px;
        }
        QTabBar::tab:selected { background: #1976D2; color: white; font-weight: 500; }
        QLabel { color: #E0E0E0; }
        #titleBar { background-color: #0D47A1; }
        #titleText { color: white; font-size: 20px; font-weight: 600; }
        """

    # === 浅色主题样式 === #
    def light_theme(self):
        return """
        QWidget { background-color: #F7F8FA; color: #212121; font-family: 'PingFang SC', Arial; }
        QLineEdit, QTextEdit {
            background: white; border: 1px solid #C5CAE9; border-radius: 6px; padding: 6px;
        }
        QPushButton {
            background-color: #1976D2; color: white; border-radius: 8px; padding: 8px 14px; font-weight: 500;
        }
        QPushButton:hover { background-color: #1565C0; }
        QProgressBar {
            border: 1px solid #C5CAE9; border-radius: 6px; text-align: center; background: white;
        }
        QProgressBar::chunk { background-color: #43A047; }
        QTabBar::tab {
            background: #E8EAF6; padding: 6px 12px; border-radius: 4px; color: #212121;
        }
        QTabBar::tab:selected { background: #1976D2; color: white; font-weight: 500; }
        #titleBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0D47A1, stop:1 #1976D2);
        }
        #titleText { color: white; font-size: 20px; font-weight: 600; }
        """

    def select_input(self):
        f, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", "Data Files (*.csv *.xlsx *.xls)")
        if f:
            self.in_edit.setText(f)
            self.log.append(f"✅ 已选择文件: {f}")

    def select_output(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录", "")
        if d:
            self.out_edit.setText(d)
            self.log.append(f"📁 输出目录: {d}")

    def open_output(self):
        folder = self.out_edit.text().strip() or os.path.join(os.getcwd(), "outputs")
        subprocess.call(["open", folder])

    def start_run(self):
        data_file = self.in_edit.text().strip()
        if not data_file:
            QMessageBox.warning(self, "提示", "请先选择数据文件！")
            return
        out_dir = self.out_edit.text().strip() or os.path.join(os.getcwd(), "outputs")
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        self.progress.setValue(0)
        self.log.append("🚀 正在运行分析，请稍候...\n")

        self.worker = Worker()
        self.worker.log.connect(self.log.append)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(lambda code: self.on_finish(code, out_dir))

        t = threading.Thread(target=self.worker.run_pipeline, args=(data_file, out_dir), daemon=True)
        t.start()

    def on_finish(self, code, out_dir):
        if code == 0:
            self.log.append("\n✅ 分析完成，加载图表中...")
            for name, canvas in zip(
                ["plot_spatiotemporal.png","plot_risk_matrix.png","plot_exceedance.png"],
                [self.canvas1,self.canvas2,self.canvas3]
            ):
                canvas.show_png(os.path.join(out_dir, name))
            self.canvas4.show_png(os.path.join(out_dir, "plot_spatiotemporal.png"))
            self.log.append("🖼 图表预览已更新。")
        else:
            self.log.append("❌ 运行失败，请检查日志。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWin()
    w.show()
    sys.exit(app.exec())