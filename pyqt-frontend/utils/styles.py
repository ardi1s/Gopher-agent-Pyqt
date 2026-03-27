#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用样式定义
保持与 Vue 前端一致的视觉风格
"""

import platform
from PyQt6.QtGui import QColor, QLinearGradient, QBrush
from PyQt6.QtCore import Qt


def get_font_family():
    """根据平台获取合适的字体"""
    system = platform.system()
    if system == 'Darwin':  # macOS
        return '"PingFang SC", "Helvetica Neue", Arial, sans-serif'
    elif system == 'Windows':
        return '"Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif'
    else:  # Linux
        return '"Noto Sans CJK SC", "PingFang SC", "Helvetica Neue", Arial, sans-serif'


class AppStyles:
    """应用样式类"""
    
    # 颜色定义
    PRIMARY_COLOR = "#667eea"
    SECONDARY_COLOR = "#764ba2"
    SUCCESS_COLOR = "#67c23a"
    WARNING_COLOR = "#e6a23c"
    DANGER_COLOR = "#f56c6c"
    INFO_COLOR = "#409eff"
    
    # 背景色
    BG_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2)"
    CARD_BG = "rgba(255, 255, 255, 0.95)"
    INPUT_BG = "rgba(255, 255, 255, 0.96)"
    
    # 文字颜色
    TEXT_PRIMARY = "#2c3e50"
    TEXT_SECONDARY = "#7f8c8d"
    TEXT_WHITE = "#ffffff"
    
    @staticmethod
    def get_global_style():
        """获取全局样式"""
        font_family = get_font_family()
        return """
        QWidget {
            font-family: """ + font_family + """;
            outline: none;
        }
        
        QScrollBar:vertical {
            background: transparent;
            width: 8px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: rgba(102, 126, 234, 0.3);
            border-radius: 4px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: rgba(102, 126, 234, 0.5);
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
    
    @staticmethod
    def get_login_card_style():
        return """
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        """
    
    @staticmethod
    def get_primary_button_style():
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5a6fd6, stop:1 #6a4190);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4e63c2, stop:1 #5e3780);
            }
            QPushButton:disabled {
                background: #cccccc;
            }
        """
    
    @staticmethod
    def get_secondary_button_style():
        return """
            QPushButton {
                background: transparent;
                color: #409eff;
                border: none;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                color: #66b1ff;
                text-decoration: underline;
            }
        """
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QTextEdit {
                background: rgba(255, 255, 255, 0.96);
                border: 2px solid rgba(0, 0, 0, 0.06);
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 15px;
                color: #2c3e50;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #409eff;
            }
            QLineEdit:disabled, QTextEdit:disabled {
                background: #f5f7fa;
                color: #c0c4cc;
            }
        """
    
    @staticmethod
    def get_session_list_style():
        return """
            QListWidget {
                background: rgba(255, 255, 255, 0.95);
                border: none;
                outline: none;
                padding: 0;
            }
            QListWidget::item {
                background: transparent;
                color: #2c3e50;
                padding: 15px 20px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.03);
            }
            QListWidget::item:hover {
                background: rgba(102, 126, 234, 0.06);
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2);
                color: white;
                font-weight: 600;
            }
        """
