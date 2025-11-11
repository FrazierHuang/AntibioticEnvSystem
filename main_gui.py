import json, sys
from pathlib import Path
from PyQt6 import QtWidgets, QtGui, QtCore
import pandas as pd
from antibiotic_env import read_data, compute_metrics, plot_spatiotemporal, plot_risk_matrix, plot_exceedance

APP_DIR = Path('.')
CONF_PATH = APP_DIR / 'lang' / 'config.json'

def load_lang(code='zh_CN'):
    lang_file = APP_DIR / 'lang' / (code + '.json')
    if not lang_file.exists():
        lang_file = APP_DIR / 'lang' / 'en_US.json'
    return code, json.loads(lang_file.read_text(encoding='utf-8'))

def save_conf(code, first_launch=False):
    CONF_PATH.write_text(json.dumps({'lang': code, 'first_launch': first_launch}), encoding='utf-8')

def read_conf():
    if CONF_PATH.exists():
        try:
            return json.loads(CONF_PATH.read_text(encoding='utf-8'))
        except Exception:
            return {'lang':'zh_CN','first_launch':True}
    return {'lang':'zh_CN','first_launch':True}

class WelcomeDialog(QtWidgets.QDialog):
    def __init__(self, lang_dict, parent=None):
        super().__init__(parent)
        self.L = lang_dict
        self.setWindowTitle(self.L['welcome_title'])
        self.setModal(True)
        self.resize(700, 460)
        v = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel(f"<h2 style='margin:6px 0'>{self.L['welcome_title']}</h2>")
        subtitle = QtWidgets.QLabel(f"<div style='color:#3aa6a1'>{self.L['welcome_subtitle']}</div>")
        v.addWidget(title); v.addWidget(subtitle)
        steps = QtWidgets.QLabel('<br>'.join([f"• {s}" for s in self.L['welcome_steps']]))
        steps.setWordWrap(True); v.addWidget(steps)
        req = QtWidgets.QLabel(f"<i>{self.L['welcome_data_req']}</i>")
        req.setWordWrap(True); v.addWidget(req)
        author = QtWidgets.QLabel(self.L['welcome_author']); v.addWidget(author)
        btn = QtWidgets.QPushButton(self.L['welcome_btn']); btn.clicked.connect(self.accept)
        v.addStretch(1); v.addWidget(btn)

class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        conf = read_conf()
        self.lang_code, self.L = load_lang(conf.get('lang','zh_CN'))
        self._init_ui()
        if read_conf().get('first_launch', True):
            dlg = WelcomeDialog(self.L, self)
            if dlg.exec():
                save_conf(self.lang_code, first_launch=False)

    def _init_ui(self):
        self.setWindowTitle(self.L['app_title'])
        self.resize(900, 600)
        central = QtWidgets.QWidget(self); self.setCentralWidget(central)
        v = QtWidgets.QVBoxLayout(central)

        top = QtWidgets.QHBoxLayout()
        self.btn_select = QtWidgets.QPushButton(self.L['btn_select'])
        self.btn_run = QtWidgets.QPushButton(self.L['btn_run'])
        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setPlaceholderText('*.csv, *.xlsx')
        top.addWidget(self.btn_select); top.addWidget(self.path_edit,1); top.addWidget(self.btn_run)
        v.addLayout(top)

        self.log = QtWidgets.QTextEdit(); self.log.setReadOnly(True)
        v.addWidget(self.log,1)

        self.status = QtWidgets.QLabel(self.L['status_ready']); v.addWidget(self.status)

        menubar = self.menuBar()
        m_lang = menubar.addMenu(self.L['menu_lang'])
        act_cn = QtGui.QAction(self.L['lang_cn'], self)
        act_en = QtGui.QAction(self.L['lang_en'], self)
        m_lang.addAction(act_cn); m_lang.addAction(act_en)
        act_cn.triggered.connect(lambda: self.switch_lang('zh_CN'))
        act_en.triggered.connect(lambda: self.switch_lang('en_US'))

        self.btn_select.clicked.connect(self.select_file)
        self.btn_run.clicked.connect(self.run_analysis)

    def switch_lang(self, code):
        self.lang_code, self.L = load_lang(code)
        save_conf(self.lang_code, first_launch=False)
        self.setWindowTitle(self.L['app_title'])
        self.btn_select.setText(self.L['btn_select'])
        self.btn_run.setText(self.L['btn_run'])
        self.menuBar().clear()
        m_lang = self.menuBar().addMenu(self.L['menu_lang'])
        act_cn = QtGui.QAction(self.L['lang_cn'], self)
        act_en = QtGui.QAction(self.L['lang_en'], self)
        m_lang.addAction(act_cn); m_lang.addAction(act_en)
        act_cn.triggered.connect(lambda: self.switch_lang('zh_CN'))
        act_en.triggered.connect(lambda: self.switch_lang('en_US'))
        self.status.setText(self.L['status_ready'])

    def select_file(self):
        path,_ = QtWidgets.QFileDialog.getOpenFileName(self, self.L['btn_select'], str(Path('.').resolve()), self.L['file_filter'])
        if path:
            self.path_edit.setText(path)

    def run_analysis(self):
        p = self.path_edit.text().strip()
        if not p:
            QtWidgets.QMessageBox.warning(self, 'AntibioticEnv', self.L['msg_no_file']); return
        outdir = Path('outputs'); outdir.mkdir(exist_ok=True)
        self.status.setText(self.L['status_running']); QtWidgets.QApplication.processEvents()
        try:
            df = read_data(p)
            df_all, per_site, exceed = compute_metrics(df)
            plot_spatiotemporal(df_all, outdir)
            plot_risk_matrix(df_all, outdir)
            plot_exceedance(exceed, outdir)
            with pd.ExcelWriter(outdir / 'outputs.xlsx') as xw:
                df_all.to_excel(xw, index=False, sheet_name='records')
                per_site.to_excel(xw, index=False, sheet_name='site_metrics')
                exceed.to_excel(xw, index=False, sheet_name='exceedance')
            self.log.append(self.L['status_done']); self.status.setText(self.L['status_done'])
            QtWidgets.QMessageBox.information(self, 'AntibioticEnv', self.L['msg_done'])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e)); self.status.setText('Error')

def main():
    app = QtWidgets.QApplication(sys.argv); win = MainWin(); win.show(); sys.exit(app.exec())

if __name__ == '__main__':
    main()
