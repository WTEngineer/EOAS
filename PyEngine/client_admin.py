from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys
import configparser
import os
from datetime import date, datetime
from PyQt5.QtCore import pyqtSignal, QTimer
import uuid
import sqlite3
import requests
from shutil import copy2
from gov_request import connect_gov
from cryptography.fernet import Fernet
from threading import Thread
from pynput.keyboard import Key, Listener
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


########################################################### key certfile
# KEY = b'9h6Qhu2Wx-mfahDjfMnd9Atv3e2BrPOUGU8utyYK6vw='
KEY = b'NthBRA5htGkZprUpudAG-Guh5UTcbxwT50Jwvg7ePV0='
########################################################### added by me

X_rate = 1
Y_rate = 1

KEY_H = 700
KEY_W = 20

MAIN_BACK_STYLE = "background-color: rgb(5,20,50)"

LOGO_BACK_STYLE = "background-color: rgba(255,255,255,0)"

RECT_STYLE = "background-color: rgba(255, 255, 255, 0);" \
             "border-color: rgb(255, 255, 0);" \
             "border-style: solid;" \
             "border-width: 2px;" \
             "border-radius: 20px;"

RECT_STYLE1 = "background-color: rgba(255, 255, 255, 0);" \
              "color: rgb(255, 255, 255);" \
              "font: 24pt \"Arial\";" \
              "border-color: rgb(255, 255, 255);" \
              "border-style: solid;" \
              "border-width: 5px;" \
              "border-radius: 10px;"

RECT_STYLE2 = "background-color: rgba(0, 0, 255, 50);" \
              "border-color: rgb(255, 255, 0);" \
              "border-style: solid;" \
              "border-width: 2px;" \
              "border-radius: 20px;"

TEXT_STYLE_BIG = "background-color: rgba(255, 255, 255, 0);" \
                 "color: rgb(255, 255, 255);" \
                 "font: 20pt \"Arial\";"

TEXT_STYLE_SMALL = "background-color: rgba(255, 255, 255, 0);" \
                   "color: rgb(255, 255, 255);" \
                   "font: 14pt \"Arial\";"

KEYBOARD_BACK_STYLE = "background-color: rgba(0, 0, 0, 150);"

KEY_BUTTON_RELEASE_STYLE = "background-color: rgb(30, 40, 50);" \
                           "color: rgb(220, 220, 220);" \
                           "font: 16pt \"Arial\";" \
                           "font: Bold;" \
                           "border-color: rgb(160, 160, 160);" \
                           "border-style: solid;" \
                           "border-width: 1px;" \
                           "border-radius: 4px;"

KEY_BUTTON_PRESS_STYLE = "background-color: rgb(80, 90, 100);" \
                         "color: rgb(255, 255, 255);" \
                         "font: 16pt \"Arial\";" \
                         "font: Bold;" \
                         "border-color: rgb(255, 255, 255);" \
                         "border-style: solid;" \
                         "border-width: 1px;" \
                         "border-radius: 4px;"

BUTTON_PRESS_STYLE = "background-color: rgba(200, 200, 255, 200);" \
                     "color: rgb(255, 255, 255);" \
                     "font: 20pt \"Arial\";" \
                     "font: Bold;" \
                     "border-color: rgb(200, 200, 255);" \
                     "border-style: solid;" \
                     "border-width: 2px;" \
                     "border-radius: 10px;"

BUTTON_RELEASE_STYLE = "background-color: rgb(40, 130, 230);" \
                       "color: rgb(255, 255, 255);" \
                       "font: 20pt \"Arial\";" \
                       "font: Bold;" \
                       "border-color: rgb(40, 130, 230);" \
                       "border-style: solid;" \
                       "border-width: 2px;" \
                       "border-radius: 10px;"


LAW_TEXTEDIT_STYLE = "background-color: rgb(240, 240, 240);" \
                     "color: rgb(30, 30, 50);" \
                     "font: 10pt \"Arial\";" \
                     "border-color: rgb(240, 240, 240);" \
                     "border-style: solid;" \
                     "border-width: 2px;" \
                     "border-radius: 20px;"

MAIN_LINEEDIT_STYLE = "background-color: rgb(220, 220, 220);" \
                      "color: rgb(80, 80, 80);" \
                      "font: 14pt \"Arial\";" \
                      "border-color: rgb(220, 220, 220);" \
                      "border-style: solid;" \
                      "border-width: 2px;" \
                      "border-radius: 10px;"

MAIN_LINEEDIT_DISABLE_STYLE = "background-color: rgb(30, 40, 50);" \
                              "color: rgb(200, 200, 200);" \
                              "font: 14pt \"Arial\";" \
                              "border-color: rgb(220, 220, 220);" \
                              "border-style: solid;" \
                              "border-width: 2px;" \
                              "border-radius: 10px;"

KEYBOARD_LINEEDIT_STYLE = "background-color: rgb(230, 230, 230);" \
                          "color: rgb(50, 50, 50);" \
                          "font: 14pt \"Arial\";" \
                          "border-color: rgb(230, 230, 230);" \
                          "border-style: solid;" \
                          "border-width: 1px;" \
                          "border-radius: 4px;"

spcial_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss', ord('Ä'): 'Ae', ord('Ü'): 'Ue',
                   ord('Ö'): 'Oe'}


# class CardWindow(QtWidgets.QMainWindow):
class AdminWindow(QtWidgets.QWidget):
    key_enter_pressed_signal = pyqtSignal()

    def __init__(self, X_rate, Y_rate):
        super(AdminWindow, self).__init__()

        #################################
        paramFile = ROOT_DIR + "/config.ini"
        config_params = configparser.ConfigParser()
        config_params.read(paramFile)

        self.encryptor = Fernet(KEY)

        ##################################
        
        self.db_file_path = None
        self.db_data = []
        
        self.edit_admin_id_flag = False
        self.edit_admin_password_flag = False

        self.edit_cert_url_flag = False
        self.edit_cert_user_flag = False
        self.edit_cert_userpass_flag = False
        self.edit_cert_pass_flag = False

        self.edit_adminsetting_user_flag = False
        self.edit_adminsetting_password_flag = False

        self.edit_machine_1_ip_flag = False
        self.edit_machine_2_ip_flag = False
        self.edit_machine_3_ip_flag = False
        self.edit_machine_4_ip_flag = False
        self.edit_machine_5_ip_flag = False
        self.edit_machine_6_ip_flag = False
        self.edit_machine_7_ip_flag = False
        self.edit_machine_8_ip_flag = False
        self.edit_machine_9_ip_flag = False
        self.edit_machine_10_ip_flag = False
        self.edit_machine_11_ip_flag = False
        self.edit_machine_12_ip_flag = False
        self.edit_machine_pass_flag = False
        
        self.edit_db_lastname_flag = False
        self.edit_db_birth_flag = False

        self.edit_wlansetting_ip_flag = False
        self.edit_wlansetting_port_flag = False

        self.edit_wifisetting_wlan_flag = False
        self.edit_wifisetting_essid_flag = False
        self.edit_wifisetting_password_flag = False

        self.edit_name_flag = False
        self.edit_birth_flag = False
        self.edit_age_flag = False
        self.edit_statue_flag = False
        self.key_shift_pressed_flag = False

        self.card_firstname = ''
        self.card_lastname = ''
        self.card_birth = ''
        self.card_age = 0
        self.card_statue = ''

        self.key_typed_string = ''

        self.admin_id_value_string = ''
        self.admin_password_value_string = ''

        self.cert_url_value_string = 'https://oasis.hessen.de/oasisws/spielerstatus'
        self.cert_user_value_string = ''
        self.cert_filepath_value_string = ''
        self.cert_userpass_value_string = ''
        self.cert_pass_value_string = ''

        self.adminsetting_user_value_string = ''
        self.adminsetting_password_value_string = ''

        self.machine_1_ip_value_string = ''
        self.machine_2_ip_value_string = ''
        self.machine_3_ip_value_string = ''
        self.machine_4_ip_value_string = ''
        self.machine_5_ip_value_string = ''
        self.machine_6_ip_value_string = ''
        self.machine_7_ip_value_string = ''
        self.machine_8_ip_value_string = ''
        self.machine_9_ip_value_string = ''
        self.machine_10_ip_value_string = ''
        self.machine_11_ip_value_string = ''
        self.machine_12_ip_value_string = ''
        self.machine_pass_value_string = ''

        self.wlansetting_ip_value_string = ''
        self.wlansetting_port_value_string = ''

        self.wifisetting_wlan_value_string = ''
        self.wifisetting_essid_value_string = ''
        self.wifisetting_password_value_string = ''

        self.request_allow_counts = 0
        self.request_notallow_counts = 0

        if os.path.exists('statistical_counts.txt'):
            f = open('statistical_counts.txt', 'r')
            line = f.read()
            f.close()

            self.request_allow_counts = int(line.split(':')[0])
            self.request_notallow_counts = int(line.split(':')[1])


        ##############################

        self.active_gov_request = False
        self.active_machine_screen = False

        self.auto_hide_allow_screen_flag = False
        self.auto_hide_notallow_screen_flag = False
        self.auto_hide_machine_screen_flag = False

        self.timer = QTimer()

        ##################################
        self.setStyleSheet(MAIN_BACK_STYLE)

        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setGeometry(int(0 * X_rate), int(0 * Y_rate), int(768 * X_rate), int(1024 * Y_rate))
        self.bg_label.setStyleSheet(MAIN_BACK_STYLE)

        # ------- Log in Screen -------------
        self.login_logo = QtWidgets.QLabel(self)
        self.login_logo.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/logo.png")
        self.login_logo.setPixmap(pix)
        self.login_logo.setGeometry(int(235 * X_rate), int(150 * Y_rate), int(300 * X_rate), int(100 * Y_rate))
        self.login_logo.setStyleSheet(LOGO_BACK_STYLE)

        self.login_text1 = QtWidgets.QLabel(self)
        self.login_text1.setAlignment(QtCore.Qt.AlignLeft)
        text1 = "ID"
        self.login_text1.setText(text1)
        self.login_text1.setGeometry(int(200 * X_rate), int(350 * Y_rate), int(250 * X_rate), int(50 * Y_rate))
        self.login_text1.setStyleSheet(TEXT_STYLE_BIG)

        self.login_id_value = QtWidgets.QLabel(self)
        # self.login_id_value.setAlignment(QtCore.Qt.AlignLeft)
        self.login_id_value.setGeometry(int(200 * X_rate), int(400 * Y_rate), int(350 * X_rate), int(60 * Y_rate))
        self.login_id_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.login_id_value.mousePressEvent = self.get_login_id_value_press_event

        self.login_text2 = QtWidgets.QLabel(self)
        self.login_text2.setAlignment(QtCore.Qt.AlignLeft)
        text1 = "Password"
        self.login_text2.setText(text1)
        self.login_text2.setGeometry(int(200 * X_rate), int(550 * Y_rate), int(250 * X_rate), int(50 * Y_rate))
        self.login_text2.setStyleSheet(TEXT_STYLE_BIG)

        self.login_password_value = QtWidgets.QLabel(self)
        # self.login_password_value.setAlignment(QtCore.Qt.AlignLeft)
        self.login_password_value.setGeometry(int(200 * X_rate), int(600 * Y_rate), int(350 * X_rate), int(60 * Y_rate))
        self.login_password_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.login_password_value.mouseReleaseEvent = self.get_login_password_value_press_event

        self.login_btn = QtWidgets.QLabel(self)
        self.login_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Login"
        self.login_btn.setText(text2)
        self.login_btn.setGeometry(int(150 * X_rate), int(940 * Y_rate), int(200 * X_rate), int(70 * Y_rate))
        self.login_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.login_btn.mousePressEvent = self.get_login_btn_press_event
        self.login_btn.mouseReleaseEvent = self.get_login_btn_release_event

        self.close_btn = QtWidgets.QLabel(self)
        self.close_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Close"
        self.close_btn.setText(text2)
        self.close_btn.setGeometry(int(420 * X_rate), int(940 * Y_rate), int(200 * X_rate), int(70 * Y_rate))
        self.close_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.close_btn.mousePressEvent = self.get_close_btn_press_event
        self.close_btn.mouseReleaseEvent = self.get_close_btn_release_event

        # ------------------- Login Success Screen ---------------------------
        self.login_success_text = QtWidgets.QLabel(self)
        self.login_success_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Login Success"
        self.login_success_text.setText(text1)
        self.login_success_text.setGeometry(int(0 * X_rate), int(350 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.login_success_text.setStyleSheet(TEXT_STYLE_BIG)

        self.login_success_icon = QtWidgets.QLabel(self)
        self.login_success_icon.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/allow.png")
        self.login_success_icon.setPixmap(pix)
        self.login_success_icon.setGeometry(int(300 * X_rate), int(400 * Y_rate), int(150 * X_rate), int(150 * Y_rate))
        self.login_success_icon.setStyleSheet(LOGO_BACK_STYLE)

        self.login_success_ok_btn = QtWidgets.QLabel(self)
        self.login_success_ok_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.login_success_ok_btn.setText(text2)
        self.login_success_ok_btn.setGeometry(int(320 * X_rate), int(940 * Y_rate), int(120 * X_rate), int(70 * Y_rate))
        self.login_success_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.login_success_ok_btn.mousePressEvent = self.get_login_success_ok_btn_press_event
        self.login_success_ok_btn.mouseReleaseEvent = self.get_login_success_ok_btn_release_event

        # ------------------- Login Failed Screen ---------------------------
        self.login_failed_text = QtWidgets.QLabel(self)
        self.login_failed_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Login Failed"
        self.login_failed_text.setText(text1)
        self.login_failed_text.setGeometry(int(0 * X_rate), int(350 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.login_failed_text.setStyleSheet(TEXT_STYLE_BIG)

        self.login_failed_icon = QtWidgets.QLabel(self)
        self.login_failed_icon.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/notallow.png")
        self.login_failed_icon.setPixmap(pix)
        self.login_failed_icon.setGeometry(int(300 * X_rate), int(400 * Y_rate), int(150 * X_rate), int(150 * Y_rate))
        self.login_failed_icon.setStyleSheet(LOGO_BACK_STYLE)

        self.login_failed_ok_btn = QtWidgets.QLabel(self)
        self.login_failed_ok_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.login_failed_ok_btn.setText(text2)
        self.login_failed_ok_btn.setGeometry(int(320 * X_rate), int(940 * Y_rate), int(120 * X_rate), int(70 * Y_rate))
        self.login_failed_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.login_failed_ok_btn.mousePressEvent = self.get_login_failed_ok_btn_press_event
        self.login_failed_ok_btn.mouseReleaseEvent = self.get_login_failed_ok_btn_release_event

        # ------------------ Admin menu screen --------------------------------
        self.menu_certsetting_button = QtWidgets.QLabel(self)
        self.menu_certsetting_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Oasis Setting"
        self.menu_certsetting_button.setText(text2)
        self.menu_certsetting_button.setGeometry(int(100 * X_rate), int(200 * Y_rate), int(250 * X_rate),
                                                 int(70 * Y_rate))
        self.menu_certsetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_certsetting_button.mousePressEvent = self.get_menu_certsetting_button_press_event
        self.menu_certsetting_button.mouseReleaseEvent = self.get_menu_certsetting_button_release_event

        self.menu_machinesetting_button = QtWidgets.QLabel(self)
        self.menu_machinesetting_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Freischaltung"
        self.menu_machinesetting_button.setText(text2)
        self.menu_machinesetting_button.setGeometry(int(100 * X_rate), int(320 * Y_rate), int(250 * X_rate),
                                                    int(70 * Y_rate))
        self.menu_machinesetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_machinesetting_button.mousePressEvent = self.get_menu_machinesetting_button_press_event
        self.menu_machinesetting_button.mouseReleaseEvent = self.get_menu_machinesetting_button_release_event


        self.menu_adminsetting_button = QtWidgets.QLabel(self)
        self.menu_adminsetting_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Admin Setting"
        self.menu_adminsetting_button.setText(text2)
        self.menu_adminsetting_button.setGeometry(int(100 * X_rate), int(440 * Y_rate), int(250 * X_rate),
                                                  int(70 * Y_rate))
        self.menu_adminsetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_adminsetting_button.mousePressEvent = self.get_menu_adminsetting_button_press_event
        self.menu_adminsetting_button.mouseReleaseEvent = self.get_menu_adminsetting_button_release_event

        self.menu_about_button = QtWidgets.QLabel(self)
        self.menu_about_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "About"
        self.menu_about_button.setText(text2)
        self.menu_about_button.setGeometry(int(100 * X_rate), int(560 * Y_rate), int(250 * X_rate),
                                           int(70 * Y_rate))
        self.menu_about_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_about_button.mousePressEvent = self.get_menu_about_button_press_event
        self.menu_about_button.mouseReleaseEvent = self.get_menu_about_button_release_event

        self.menu_manual_button = QtWidgets.QLabel(self)
        self.menu_manual_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Abfrage"
        self.menu_manual_button.setText(text2)
        self.menu_manual_button.setGeometry(int(420 * X_rate), int(200 * Y_rate), int(250 * X_rate),
                                                 int(70 * Y_rate))
        self.menu_manual_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_manual_button.mousePressEvent = self.get_menu_manual_button_press_event
        self.menu_manual_button.mouseReleaseEvent = self.get_menu_manual_button_release_event

        self.menu_wifisetting_button = QtWidgets.QLabel(self)
        self.menu_wifisetting_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "WiFi Setting"
        self.menu_wifisetting_button.setText(text2)
        self.menu_wifisetting_button.setGeometry(int(420 * X_rate), int(320 * Y_rate), int(250 * X_rate),
                                                 int(70 * Y_rate))
        self.menu_wifisetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_wifisetting_button.mousePressEvent = self.get_menu_wifisetting_button_press_event
        self.menu_wifisetting_button.mouseReleaseEvent = self.get_menu_wifisetting_button_release_event

        self.menu_update_button = QtWidgets.QLabel(self)
        self.menu_update_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Update"
        self.menu_update_button.setText(text2)
        self.menu_update_button.setGeometry(int(420 * X_rate), int(440 * Y_rate), int(250 * X_rate),
                                                 int(70 * Y_rate))
        self.menu_update_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_update_button.mousePressEvent = self.get_menu_update_button_press_event
        self.menu_update_button.mouseReleaseEvent = self.get_menu_update_button_release_event


        self.menu_machine_button = QtWidgets.QLabel(self)
        self.menu_machine_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Machine"
        self.menu_machine_button.setText(text2)
        self.menu_machine_button.setGeometry(int(420 * X_rate), int(560 * Y_rate), int(250 * X_rate),
                                                 int(70 * Y_rate))
        self.menu_machine_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_machine_button.mousePressEvent = self.get_menu_machine_button_press_event
        self.menu_machine_button.mouseReleaseEvent = self.get_menu_machine_button_release_event


        self.menu_db_button = QtWidgets.QLabel(self)
        self.menu_db_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "DB Manager"
        self.menu_db_button.setText(text2)
        self.menu_db_button.setGeometry(int(100 * X_rate), int(680 * Y_rate), int(250 * X_rate),
                                                 int(70 * Y_rate))
        self.menu_db_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_db_button.mousePressEvent = self.get_menu_db_button_press_event
        self.menu_db_button.mouseReleaseEvent = self.get_menu_db_button_release_event


        self.menu_cancel_button = QtWidgets.QLabel(self)
        self.menu_cancel_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Schliessen"
        self.menu_cancel_button.setText(text2)
        self.menu_cancel_button.setGeometry(int(260 * X_rate), int(940 * Y_rate), int(250 * X_rate),
                                            int(70 * Y_rate))
        self.menu_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.menu_cancel_button.mousePressEvent = self.get_menu_cancel_button_press_event
        self.menu_cancel_button.mouseReleaseEvent = self.get_menu_cancel_button_release_event

        # ------------------ Certification screen -----------------
        self.cert_logo = QtWidgets.QLabel(self)
        self.cert_logo.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/logo.png")
        self.cert_logo.setPixmap(pix)
        self.cert_logo.setGeometry(int(285 * X_rate), int(100 * Y_rate), int(200 * X_rate), int(70 * Y_rate))
        self.cert_logo.setStyleSheet(LOGO_BACK_STYLE)

        self.cert_text = QtWidgets.QLabel(self)
        self.cert_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Oasis Certification Setting"
        self.cert_text.setText(text1)
        self.cert_text.setGeometry(int(0 * X_rate), int(250 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.cert_text.setStyleSheet(TEXT_STYLE_BIG)

        self.cert_url_text = QtWidgets.QLabel(self)
        self.cert_url_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "URL"
        self.cert_url_text.setText(text1)
        self.cert_url_text.setGeometry(int(100 * X_rate), int(360 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.cert_url_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.cert_url_value = QtWidgets.QLabel(self)
        self.cert_url_value.setText("https://oasis-tst-crt.hessen.de/oasisws/spielerstatus")
        self.cert_url_value.setGeometry(int(220 * X_rate), int(350 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.cert_url_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.cert_url_value.mousePressEvent = self.get_cert_url_value_press_event

        self.cert_user_text = QtWidgets.QLabel(self)
        self.cert_user_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Kennung"
        self.cert_user_text.setText(text1)
        self.cert_user_text.setGeometry(int(0 * X_rate), int(460 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.cert_user_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.cert_user_value = QtWidgets.QLabel(self)
        self.cert_user_value.setGeometry(int(220 * X_rate), int(450 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.cert_user_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.cert_user_value.mousePressEvent = self.get_cert_user_value_press_event

        self.cert_userpass_text = QtWidgets.QLabel(self)
        self.cert_userpass_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Passwort"
        self.cert_userpass_text.setText(text1)
        self.cert_userpass_text.setGeometry(int(0 * X_rate), int(560 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.cert_userpass_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.cert_userpass_value = QtWidgets.QLabel(self)
        self.cert_userpass_value.setGeometry(int(220 * X_rate), int(550 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.cert_userpass_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.cert_userpass_value.mousePressEvent = self.get_cert_userpass_value_press_event

        self.cert_filepath_text = QtWidgets.QLabel(self)
        self.cert_filepath_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Cert-File"
        self.cert_filepath_text.setText(text1)
        self.cert_filepath_text.setGeometry(int(100 * X_rate), int(660 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.cert_filepath_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.cert_filepath_value = QtWidgets.QLabel(self)
        self.cert_filepath_value.setGeometry(int(220 * X_rate), int(650 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.cert_filepath_value.setStyleSheet(MAIN_LINEEDIT_STYLE)

        self.cert_browse_button = QtWidgets.QLabel(self)
        self.cert_browse_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "..."
        self.cert_browse_button.setText(text2)
        self.cert_browse_button.setGeometry(int(640 * X_rate), int(650 * Y_rate), int(80 * X_rate),
                                            int(50 * Y_rate))
        self.cert_browse_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.cert_browse_button.mousePressEvent = self.get_cert_browse_button_press_event
        self.cert_browse_button.mouseReleaseEvent = self.get_cert_browse_button_release_event

        self.cert_pass_text = QtWidgets.QLabel(self)
        self.cert_pass_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Passwort"
        self.cert_pass_text.setText(text1)
        self.cert_pass_text.setGeometry(int(100 * X_rate), int(760 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.cert_pass_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.cert_pass_value = QtWidgets.QLabel(self)
        self.cert_pass_value.setGeometry(int(220 * X_rate), int(750 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.cert_pass_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.cert_pass_value.mousePressEvent = self.get_cert_pass_value_press_event

        self.cert_import_button = QtWidgets.QLabel(self)
        self.cert_import_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Import"
        self.cert_import_button.setText(text2)
        self.cert_import_button.setGeometry(int(100 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                            int(70 * Y_rate))
        self.cert_import_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.cert_import_button.mousePressEvent = self.get_cert_import_button_press_event
        self.cert_import_button.mouseReleaseEvent = self.get_cert_import_button_release_event

        self.cert_ok_button = QtWidgets.QLabel(self)
        self.cert_ok_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.cert_ok_button.setText(text2)
        self.cert_ok_button.setGeometry(int(310 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                        int(70 * Y_rate))
        self.cert_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.cert_ok_button.mousePressEvent = self.get_cert_ok_button_press_event
        self.cert_ok_button.mouseReleaseEvent = self.get_cert_ok_button_release_event

        self.cert_cancel_button = QtWidgets.QLabel(self)
        self.cert_cancel_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Cancel"
        self.cert_cancel_button.setText(text2)
        self.cert_cancel_button.setGeometry(int(520 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                            int(70 * Y_rate))
        self.cert_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.cert_cancel_button.mousePressEvent = self.get_cert_cancel_button_press_event
        self.cert_cancel_button.mouseReleaseEvent = self.get_cert_cancel_button_release_event

        # ------------------- Machine setting screen --------------------------
        self.machinesetting_1_text = QtWidgets.QLabel(self)
        self.machinesetting_1_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-1-IP"
        self.machinesetting_1_text.setText(text1)
        self.machinesetting_1_text.setGeometry(int(0 * X_rate), int(110 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_1_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_1_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_1_ip_value.setGeometry(int(220 * X_rate), int(100 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_1_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_1_ip_value.mousePressEvent = self.get_machinesetting_1_ip_value_press_event

        self.machinesetting_2_text = QtWidgets.QLabel(self)
        self.machinesetting_2_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-2-IP"
        self.machinesetting_2_text.setText(text1)
        self.machinesetting_2_text.setGeometry(int(0 * X_rate), int(170 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_2_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_2_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_2_ip_value.setGeometry(int(220 * X_rate), int(160 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_2_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_2_ip_value.mousePressEvent = self.get_machinesetting_2_ip_value_press_event

        self.machinesetting_3_text = QtWidgets.QLabel(self)
        self.machinesetting_3_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-3-IP"
        self.machinesetting_3_text.setText(text1)
        self.machinesetting_3_text.setGeometry(int(0 * X_rate), int(230 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_3_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_3_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_3_ip_value.setGeometry(int(220 * X_rate), int(220 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_3_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_3_ip_value.mousePressEvent = self.get_machinesetting_3_ip_value_press_event

        self.machinesetting_4_text = QtWidgets.QLabel(self)
        self.machinesetting_4_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-4-IP"
        self.machinesetting_4_text.setText(text1)
        self.machinesetting_4_text.setGeometry(int(0 * X_rate), int(290 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_4_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_4_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_4_ip_value.setGeometry(int(220 * X_rate), int(280 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_4_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_4_ip_value.mousePressEvent = self.get_machinesetting_4_ip_value_press_event

        self.machinesetting_5_text = QtWidgets.QLabel(self)
        self.machinesetting_5_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-5-IP"
        self.machinesetting_5_text.setText(text1)
        self.machinesetting_5_text.setGeometry(int(0 * X_rate), int(350 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_5_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_5_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_5_ip_value.setGeometry(int(220 * X_rate), int(340 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_5_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_5_ip_value.mousePressEvent = self.get_machinesetting_5_ip_value_press_event

        self.machinesetting_6_text = QtWidgets.QLabel(self)
        self.machinesetting_6_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-6-IP"
        self.machinesetting_6_text.setText(text1)
        self.machinesetting_6_text.setGeometry(int(0 * X_rate), int(410 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_6_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_6_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_6_ip_value.setGeometry(int(220 * X_rate), int(400 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_6_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_6_ip_value.mousePressEvent = self.get_machinesetting_6_ip_value_press_event

        self.machinesetting_7_text = QtWidgets.QLabel(self)
        self.machinesetting_7_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-7-IP"
        self.machinesetting_7_text.setText(text1)
        self.machinesetting_7_text.setGeometry(int(0 * X_rate), int(470 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_7_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_7_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_7_ip_value.setGeometry(int(220 * X_rate), int(460 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_7_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_7_ip_value.mousePressEvent = self.get_machinesetting_7_ip_value_press_event

        self.machinesetting_8_text = QtWidgets.QLabel(self)
        self.machinesetting_8_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-8-IP"
        self.machinesetting_8_text.setText(text1)
        self.machinesetting_8_text.setGeometry(int(0 * X_rate), int(530 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_8_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_8_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_8_ip_value.setGeometry(int(220 * X_rate), int(520 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_8_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_8_ip_value.mousePressEvent = self.get_machinesetting_8_ip_value_press_event

        self.machinesetting_9_text = QtWidgets.QLabel(self)
        self.machinesetting_9_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-9-IP"
        self.machinesetting_9_text.setText(text1)
        self.machinesetting_9_text.setGeometry(int(0 * X_rate), int(590 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_9_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_9_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_9_ip_value.setGeometry(int(220 * X_rate), int(580 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_9_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_9_ip_value.mousePressEvent = self.get_machinesetting_9_ip_value_press_event

        self.machinesetting_10_text = QtWidgets.QLabel(self)
        self.machinesetting_10_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-10-IP"
        self.machinesetting_10_text.setText(text1)
        self.machinesetting_10_text.setGeometry(int(0 * X_rate), int(650 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_10_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_10_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_10_ip_value.setGeometry(int(220 * X_rate), int(640 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_10_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_10_ip_value.mousePressEvent = self.get_machinesetting_10_ip_value_press_event

        self.machinesetting_11_text = QtWidgets.QLabel(self)
        self.machinesetting_11_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-11-IP"
        self.machinesetting_11_text.setText(text1)
        self.machinesetting_11_text.setGeometry(int(0 * X_rate), int(710 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_11_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_11_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_11_ip_value.setGeometry(int(220 * X_rate), int(700 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_11_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_11_ip_value.mousePressEvent = self.get_machinesetting_11_ip_value_press_event

        self.machinesetting_12_text = QtWidgets.QLabel(self)
        self.machinesetting_12_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "GSG-12-IP"
        self.machinesetting_12_text.setText(text1)
        self.machinesetting_12_text.setGeometry(int(0 * X_rate), int(770 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_12_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_12_ip_value = QtWidgets.QLabel(self)
        self.machinesetting_12_ip_value.setGeometry(int(220 * X_rate), int(760 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_12_ip_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_12_ip_value.mousePressEvent = self.get_machinesetting_12_ip_value_press_event

        self.machinesetting_pass_text = QtWidgets.QLabel(self)
        self.machinesetting_pass_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "VDAI-Pass"
        self.machinesetting_pass_text.setText(text1)
        self.machinesetting_pass_text.setGeometry(int(0 * X_rate), int(830 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.machinesetting_pass_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.machinesetting_pass_value = QtWidgets.QLabel(self)
        self.machinesetting_pass_value.setGeometry(int(220 * X_rate), int(820 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.machinesetting_pass_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.machinesetting_pass_value.mousePressEvent = self.get_machinesetting_pass_value_press_event

        self.machinesetting_ok_button = QtWidgets.QLabel(self)
        self.machinesetting_ok_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.machinesetting_ok_button.setText(text2)
        self.machinesetting_ok_button.setGeometry(int(310 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                           int(70 * Y_rate))
        self.machinesetting_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.machinesetting_ok_button.mousePressEvent = self.get_machinesetting_ok_button_press_event
        self.machinesetting_ok_button.mouseReleaseEvent = self.get_machinesetting_ok_button_release_event

        self.machinesetting_cancel_button = QtWidgets.QLabel(self)
        self.machinesetting_cancel_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Cancel"
        self.machinesetting_cancel_button.setText(text2)
        self.machinesetting_cancel_button.setGeometry(int(520 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                               int(70 * Y_rate))
        self.machinesetting_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.machinesetting_cancel_button.mousePressEvent = self.get_machinesetting_cancel_button_press_event
        self.machinesetting_cancel_button.mouseReleaseEvent = self.get_machinesetting_cancel_button_release_event

        # ------------------- DB Manager screen------------
        self.db_tablewidget = QtWidgets.QTableWidget(self)
        self.db_tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.db_tablewidget.setGeometry(int(X_rate * 20), int(Y_rate * 340), int(X_rate * 730), int(Y_rate * 560))
        self.db_tablewidget.setStyleSheet("background-color: rgb(255, 255, 255);" \
                                          "color: rgb(0, 0, 0);" \
                                          "font: 12pt \"Arial\";" \
                                          "border-color: rgb(255, 255, 255);" \
                                          "border-style: solid;" \
                                          "border-width: 1px;" \
                                          "border-radius: 2px;")

        self.db_label1 = QtWidgets.QLabel(self)
        self.db_label1.setText("Last Name")
        self.db_label1.setStyleSheet(TEXT_STYLE_BIG)
        self.db_label1.setGeometry(int(X_rate * 20), int(Y_rate * 190), int(X_rate * 200), int(Y_rate * 40))

        self.db_label2 = QtWidgets.QLabel(self)
        self.db_label2.setText("Birthday")
        self.db_label2.setStyleSheet(TEXT_STYLE_BIG)
        self.db_label2.setGeometry(int(X_rate * 390), int(Y_rate * 190), int(X_rate * 150), int(Y_rate * 40))

        self.db_lastname_value = QtWidgets.QLabel(self)
        self.db_lastname_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.db_lastname_value.setGeometry(int(X_rate * 20), int(Y_rate * 250), int(X_rate * 300), int(Y_rate * 60))
        self.db_lastname_value.mousePressEvent = self.get_db_lastname_value_press_event

        self.db_birth_value = QtWidgets.QLabel(self)
        self.db_birth_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.db_birth_value.setGeometry(int(X_rate * 390), int(Y_rate * 250), int(X_rate * 190), int(Y_rate * 60))
        self.db_birth_value.mousePressEvent = self.get_db_birth_value_press_event

        self.db_browse_btn = QtWidgets.QLabel(self)
        self.db_browse_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Open"
        self.db_browse_btn.setText(text2)
        self.db_browse_btn.setGeometry(int(590 * X_rate), int(100 * Y_rate), int(150 * X_rate), int(60 * Y_rate))
        self.db_browse_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.db_browse_btn.mousePressEvent = self.get_db_browse_btn_press_event
        self.db_browse_btn.mouseReleaseEvent = self.get_db_browse_btn_release_event

        self.db_search_btn = QtWidgets.QLabel(self)
        self.db_search_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Search"
        self.db_search_btn.setText(text2)
        self.db_search_btn.setGeometry(int(590 * X_rate), int(250 * Y_rate), int(150 * X_rate), int(60 * Y_rate))
        self.db_search_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.db_search_btn.mousePressEvent = self.get_db_search_btn_press_event
        self.db_search_btn.mouseReleaseEvent = self.get_db_search_btn_release_event

        self.db_path = QtWidgets.QLabel(self)
        self.db_path.setGeometry(int(20 * X_rate), int(100 * Y_rate), int(560 * X_rate), int(60 * Y_rate))
        self.db_path.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.db_delete_btn = QtWidgets.QLabel(self)
        self.db_delete_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Delete"
        self.db_delete_btn.setText(text2)
        self.db_delete_btn.setGeometry(int(420 * X_rate), int(940 * Y_rate), int(150 * X_rate), int(60 * Y_rate))
        self.db_delete_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.db_delete_btn.mousePressEvent = self.get_db_delete_btn_press_event
        self.db_delete_btn.mouseReleaseEvent = self.get_db_delete_btn_release_event


        self.db_cancel_btn = QtWidgets.QLabel(self)
        self.db_cancel_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Cancel"
        self.db_cancel_btn.setText(text2)
        self.db_cancel_btn.setGeometry(int(590 * X_rate), int(940 * Y_rate), int(150 * X_rate), int(60 * Y_rate))
        self.db_cancel_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.db_cancel_btn.mousePressEvent = self.get_db_cancel_btn_press_event
        self.db_cancel_btn.mouseReleaseEvent = self.get_db_cancel_btn_release_event

        # ------------------- WIFI setting screen ------------------------------
        self.wifi_logo = QtWidgets.QLabel(self)
        self.wifi_logo.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/logo.png")
        self.wifi_logo.setPixmap(pix)
        self.wifi_logo.setGeometry(int(285 * X_rate), int(100 * Y_rate), int(200 * X_rate), int(70 * Y_rate))
        self.wifi_logo.setStyleSheet(LOGO_BACK_STYLE)

        self.wifi_text = QtWidgets.QLabel(self)
        self.wifi_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "WiFi Setting"
        self.wifi_text.setText(text1)
        self.wifi_text.setGeometry(int(0 * X_rate), int(250 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.wifi_text.setStyleSheet(TEXT_STYLE_BIG)

        self.wifi_wlan_text = QtWidgets.QLabel(self)
        self.wifi_wlan_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "WLAN"
        self.wifi_wlan_text.setText(text1)
        self.wifi_wlan_text.setGeometry(int(100 * X_rate), int(360 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.wifi_wlan_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.wifi_wlan_value = QtWidgets.QLabel(self)
        self.wifi_wlan_value.setGeometry(int(220 * X_rate), int(350 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.wifi_wlan_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.wifi_wlan_value.mousePressEvent = self.get_wifi_wlan_value_press_event

        self.wifi_essid_text = QtWidgets.QLabel(self)
        self.wifi_essid_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "WLAN"
        self.wifi_essid_text.setText(text1)
        self.wifi_essid_text.setGeometry(int(100 * X_rate), int(460 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.wifi_essid_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.wifi_essid_value = QtWidgets.QLabel(self)
        self.wifi_essid_value.setGeometry(int(220 * X_rate), int(450 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.wifi_essid_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.wifi_essid_value.mousePressEvent = self.get_wifi_essid_value_press_event

        self.wifi_pass_text = QtWidgets.QLabel(self)
        self.wifi_pass_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Passwort"
        self.wifi_pass_text.setText(text1)
        self.wifi_pass_text.setGeometry(int(0 * X_rate), int(560 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.wifi_pass_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.wifi_pass_value = QtWidgets.QLabel(self)
        self.wifi_pass_value.setGeometry(int(220 * X_rate), int(550 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.wifi_pass_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.wifi_pass_value.mousePressEvent = self.get_wifi_pass_value_press_event

        self.wifi_ok_button = QtWidgets.QLabel(self)
        self.wifi_ok_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.wifi_ok_button.setText(text2)
        self.wifi_ok_button.setGeometry(int(310 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                        int(70 * Y_rate))
        self.wifi_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.wifi_ok_button.mousePressEvent = self.get_wifi_ok_button_press_event
        self.wifi_ok_button.mouseReleaseEvent = self.get_wifi_ok_button_release_event

        self.wifi_cancel_button = QtWidgets.QLabel(self)
        self.wifi_cancel_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Cancel"
        self.wifi_cancel_button.setText(text2)
        self.wifi_cancel_button.setGeometry(int(520 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                            int(70 * Y_rate))
        self.wifi_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.wifi_cancel_button.mousePressEvent = self.get_wifi_cancel_button_press_event
        self.wifi_cancel_button.mouseReleaseEvent = self.get_wifi_cancel_button_release_event

        # ------------------- Admin setting screen ------------------------------
        self.admin_logo = QtWidgets.QLabel(self)
        self.admin_logo.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/logo.png")
        self.admin_logo.setPixmap(pix)
        self.admin_logo.setGeometry(int(285 * X_rate), int(100 * Y_rate), int(200 * X_rate), int(70 * Y_rate))
        self.admin_logo.setStyleSheet(LOGO_BACK_STYLE)

        self.admin_text = QtWidgets.QLabel(self)
        self.admin_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Admin Setting"
        self.admin_text.setText(text1)
        self.admin_text.setGeometry(int(0 * X_rate), int(250 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.admin_text.setStyleSheet(TEXT_STYLE_BIG)

        self.admin_user_text = QtWidgets.QLabel(self)
        self.admin_user_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "User"
        self.admin_user_text.setText(text1)
        self.admin_user_text.setGeometry(int(100 * X_rate), int(360 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.admin_user_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.admin_user_value = QtWidgets.QLabel(self)
        self.admin_user_value.setGeometry(int(220 * X_rate), int(350 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.admin_user_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.admin_user_value.mousePressEvent = self.get_admin_user_value_press_event

        self.admin_pass_text = QtWidgets.QLabel(self)
        self.admin_pass_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Password"
        self.admin_pass_text.setText(text1)
        self.admin_pass_text.setGeometry(int(0 * X_rate), int(460 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.admin_pass_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.admin_pass_value = QtWidgets.QLabel(self)
        self.admin_pass_value.setGeometry(int(220 * X_rate), int(450 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.admin_pass_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.admin_pass_value.mousePressEvent = self.get_admin_pass_value_press_event

        self.admin_ok_button = QtWidgets.QLabel(self)
        self.admin_ok_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.admin_ok_button.setText(text2)
        self.admin_ok_button.setGeometry(int(310 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                         int(70 * Y_rate))
        self.admin_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.admin_ok_button.mousePressEvent = self.get_admin_ok_button_press_event
        self.admin_ok_button.mouseReleaseEvent = self.get_admin_ok_button_release_event

        self.admin_cancel_button = QtWidgets.QLabel(self)
        self.admin_cancel_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Cancel"
        self.admin_cancel_button.setText(text2)
        self.admin_cancel_button.setGeometry(int(520 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                             int(70 * Y_rate))
        self.admin_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.admin_cancel_button.mousePressEvent = self.get_admin_cancel_button_press_event
        self.admin_cancel_button.mouseReleaseEvent = self.get_admin_cancel_button_release_event

        # ------------------- About setting screen ------------------------------
        self.about_logo = QtWidgets.QLabel(self)
        self.about_logo.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/logo.png")
        self.about_logo.setPixmap(pix)
        self.about_logo.setGeometry(int(285 * X_rate), int(100 * Y_rate), int(200 * X_rate), int(70 * Y_rate))
        self.about_logo.setStyleSheet(LOGO_BACK_STYLE)

        self.about_text = QtWidgets.QLabel(self)
        self.about_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "About The Application"
        self.about_text.setText(text1)
        self.about_text.setGeometry(int(0 * X_rate), int(250 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.about_text.setStyleSheet(TEXT_STYLE_BIG)

        self.about_appname_text = QtWidgets.QLabel(self)
        self.about_appname_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Name"
        self.about_appname_text.setText(text1)
        self.about_appname_text.setGeometry(int(100 * X_rate), int(360 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.about_appname_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.about_appname_value = QtWidgets.QLabel(self)
        self.about_appname_value.setText("Oasis Premium v.2.01 \xa9 2023 StartLight UG")
        self.about_appname_value.setGeometry(int(220 * X_rate), int(350 * Y_rate), int(420 * X_rate), int(50 * Y_rate))
        self.about_appname_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac_addr = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        mac_str = str(uuid.getnode())
        serial_str = mac_str[-8:]

        self.about_macaddr_text = QtWidgets.QLabel(self)
        self.about_macaddr_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "MAC Address"
        self.about_macaddr_text.setText(text1)
        self.about_macaddr_text.setGeometry(int(0 * X_rate), int(460 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.about_macaddr_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.about_macaddr_value = QtWidgets.QLabel(self)
        self.about_macaddr_value.setText(mac_addr)
        self.about_macaddr_value.setGeometry(int(220 * X_rate), int(450 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.about_macaddr_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.about_serial_text = QtWidgets.QLabel(self)
        self.about_serial_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Serial"
        self.about_serial_text.setText(text1)
        self.about_serial_text.setGeometry(int(0 * X_rate), int(560 * Y_rate), int(200 * X_rate), int(50 * Y_rate))
        self.about_serial_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.about_serial_value = QtWidgets.QLabel(self)
        self.about_serial_value.setText(serial_str)
        self.about_serial_value.setGeometry(int(220 * X_rate), int(550 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.about_serial_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.about_total_request_text = QtWidgets.QLabel(self)
        self.about_total_request_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Total Requests"
        self.about_total_request_text.setText(text1)
        self.about_total_request_text.setGeometry(int(0 * X_rate), int(660 * Y_rate), int(200 * X_rate),
                                                  int(50 * Y_rate))
        self.about_total_request_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.about_total_request_value = QtWidgets.QLabel(self)
        self.about_total_request_value.setGeometry(int(220 * X_rate), int(650 * Y_rate), int(400 * X_rate),
                                                   int(50 * Y_rate))
        self.about_total_request_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.about_allow_request_text = QtWidgets.QLabel(self)
        self.about_allow_request_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "Allow Requests"
        self.about_allow_request_text.setText(text1)
        self.about_allow_request_text.setGeometry(int(0 * X_rate), int(760 * Y_rate), int(200 * X_rate),
                                                  int(50 * Y_rate))
        self.about_allow_request_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.about_allow_request_value = QtWidgets.QLabel(self)
        self.about_allow_request_value.setGeometry(int(220 * X_rate), int(750 * Y_rate), int(400 * X_rate),
                                                   int(50 * Y_rate))
        self.about_allow_request_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.about_notallow_request_text = QtWidgets.QLabel(self)
        self.about_notallow_request_text.setAlignment(QtCore.Qt.AlignRight)
        text1 = "NAllow Requests"
        self.about_notallow_request_text.setText(text1)
        self.about_notallow_request_text.setGeometry(int(0 * X_rate), int(860 * Y_rate), int(200 * X_rate),
                                                     int(50 * Y_rate))
        self.about_notallow_request_text.setStyleSheet(TEXT_STYLE_SMALL)

        self.about_notallow_request_value = QtWidgets.QLabel(self)
        self.about_notallow_request_value.setGeometry(int(220 * X_rate), int(850 * Y_rate), int(400 * X_rate),
                                                      int(50 * Y_rate))
        self.about_notallow_request_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.about_cancel_button = QtWidgets.QLabel(self)
        self.about_cancel_button.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "Cancel"
        self.about_cancel_button.setText(text2)
        self.about_cancel_button.setGeometry(int(520 * X_rate), int(940 * Y_rate), int(150 * X_rate),
                                             int(70 * Y_rate))
        self.about_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.about_cancel_button.mousePressEvent = self.get_about_cancel_button_press_event
        self.about_cancel_button.mouseReleaseEvent = self.get_about_cancel_button_release_event


        # ---------------- Main Screen -------------
        self.main_logo = QtWidgets.QLabel(self)
        self.main_logo.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/logo.png")
        self.main_logo.setPixmap(pix)
        self.main_logo.setGeometry(int(270 * X_rate), int(70 * Y_rate), int(200 * X_rate), int(80 * Y_rate))
        self.main_logo.setStyleSheet(LOGO_BACK_STYLE)

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Ausweis/Reisepass durch\nhineindruecken einscannen."
        self.main_text.setText(text1)
        self.main_text.setGeometry(int(0 * X_rate), int(170 * Y_rate), int(768 * X_rate), int(100 * Y_rate))
        self.main_text.setStyleSheet(TEXT_STYLE_BIG)

        self.main_face = QtWidgets.QLabel(self)
        self.main_face.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/face_icon.png")
        self.main_face.setPixmap(pix)
        self.main_face.setStyleSheet("background-color: rgb(80,80,80)")
        self.main_face.setGeometry(int(260 * X_rate), int(300 * Y_rate), int(220 * X_rate), int(250 * Y_rate))

        self.main_text_name = QtWidgets.QLabel(self)
        self.main_text_name.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Vorname, Nachname"
        self.main_text_name.setText(text1)
        self.main_text_name.setGeometry(int(0 * X_rate), int(560 * Y_rate), int(440 * X_rate), int(50 * Y_rate))
        self.main_text_name.setStyleSheet(TEXT_STYLE_SMALL)

        self.main_name_value = QtWidgets.QLabel(self)
        self.main_name_value.setAlignment(QtCore.Qt.AlignCenter)
        self.main_name_value.setGeometry(int(100 * X_rate), int(610 * Y_rate), int(500 * X_rate), int(60 * Y_rate))
        self.main_name_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.main_name_value.mousePressEvent = self.get_main_name_value_press_event

        self.main_text_birth = QtWidgets.QLabel(self)
        self.main_text_birth.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Geburtsdatum"
        self.main_text_birth.setText(text1)
        self.main_text_birth.setGeometry(int(0 * X_rate), int(680 * Y_rate), int(350 * X_rate), int(50 * Y_rate))
        self.main_text_birth.setStyleSheet(TEXT_STYLE_SMALL)

        self.main_birth_value = QtWidgets.QLabel(self)
        self.main_birth_value.setAlignment(QtCore.Qt.AlignCenter)
        self.main_birth_value.setGeometry(int(100 * X_rate), int(730 * Y_rate), int(200 * X_rate), int(60 * Y_rate))
        self.main_birth_value.setStyleSheet(MAIN_LINEEDIT_STYLE)
        self.main_birth_value.mousePressEvent = self.get_main_birth_value_press_event


        self.main_text_age = QtWidgets.QLabel(self)
        self.main_text_age.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Alter"
        self.main_text_age.setText(text1)
        self.main_text_age.setGeometry(int(330 * X_rate), int(680 * Y_rate), int(50 * X_rate), int(50 * Y_rate))
        self.main_text_age.setStyleSheet(TEXT_STYLE_SMALL)

        self.main_age_value = QtWidgets.QLabel(self)
        self.main_age_value.setAlignment(QtCore.Qt.AlignCenter)
        self.main_age_value.setGeometry(int(320 * X_rate), int(730 * Y_rate), int(90 * X_rate), int(60 * Y_rate))
        self.main_age_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.main_text_status = QtWidgets.QLabel(self)
        self.main_text_status.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Status"
        self.main_text_status.setText(text1)
        self.main_text_status.setGeometry(int(420 * X_rate), int(680 * Y_rate), int(100 * X_rate), int(50 * Y_rate))
        self.main_text_status.setStyleSheet(TEXT_STYLE_SMALL)

        self.main_status_value = QtWidgets.QLabel(self)
        self.main_status_value.setAlignment(QtCore.Qt.AlignCenter)
        self.main_status_value.setGeometry(int(430 * X_rate), int(730 * Y_rate), int(170 * X_rate), int(60 * Y_rate))
        self.main_status_value.setStyleSheet(MAIN_LINEEDIT_DISABLE_STYLE)

        self.main_text1 = QtWidgets.QLabel(self)
        self.main_text1.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Daten korrekt?"
        self.main_text1.setText(text1)
        self.main_text1.setGeometry(int(0 * X_rate), int(820 * Y_rate), int(400 * X_rate), int(50 * Y_rate))
        self.main_text1.setStyleSheet(TEXT_STYLE_BIG)

        self.main_ok_btn = QtWidgets.QLabel(self)
        self.main_ok_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.main_ok_btn.setText(text2)
        self.main_ok_btn.setGeometry(int(100 * X_rate), int(940 * Y_rate), int(120 * X_rate), int(70 * Y_rate))
        self.main_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.main_ok_btn.mousePressEvent = self.get_main_ok_btn_press_event
        self.main_ok_btn.mouseReleaseEvent = self.get_main_ok_btn_release_event

        self.main_hilfe_btn = QtWidgets.QLabel(self)
        self.main_hilfe_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "HILEF"
        self.main_hilfe_btn.setText(text2)
        self.main_hilfe_btn.setGeometry(int(240 * X_rate), int(940 * Y_rate), int(160 * X_rate), int(70 * Y_rate))
        self.main_hilfe_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.main_hilfe_btn.mousePressEvent = self.get_main_hilfe_btn_press_event
        self.main_hilfe_btn.mouseReleaseEvent = self.get_main_hilfe_btn_release_event
        self.main_hilfe_btn.hide()

        self.main_abbreuch_btn = QtWidgets.QLabel(self)
        self.main_abbreuch_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "ABBRUCH"
        self.main_abbreuch_btn.setText(text2)
        self.main_abbreuch_btn.setGeometry(int(420 * X_rate), int(940 * Y_rate), int(250 * X_rate), int(70 * Y_rate))
        self.main_abbreuch_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.main_abbreuch_btn.mousePressEvent = self.get_main_abbreuch_btn_press_event
        self.main_abbreuch_btn.mouseReleaseEvent = self.get_main_abbreuch_btn_release_event


        # ------------------ Gov Result Allow Screen ------
        self.allow_textedit = QtWidgets.QTextEdit(self)
        self.allow_textedit.setReadOnly(True)
        self.allow_textedit.setGeometry(int(100 * X_rate), int(250 * Y_rate), int(560 * X_rate), int(200 * Y_rate))
        self.allow_textedit.setStyleSheet(LAW_TEXTEDIT_STYLE)

        self.allow_text = QtWidgets.QLabel(self)
        self.allow_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Der Spieler ist nicht gesperrt!"
        self.allow_text.setText(text1)
        self.allow_text.setGeometry(int(0 * X_rate), int(500 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.allow_text.setStyleSheet(TEXT_STYLE_BIG)

        self.allow_icon = QtWidgets.QLabel(self)
        self.allow_icon.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/allow.png")
        self.allow_icon.setPixmap(pix)
        self.allow_icon.setStyleSheet(LOGO_BACK_STYLE)
        self.allow_icon.setGeometry(int(300 * X_rate), int(600 * Y_rate), int(150 * X_rate), int(150 * Y_rate))

        self.allow_ok_btn = QtWidgets.QLabel(self)
        self.allow_ok_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.allow_ok_btn.setText(text2)
        self.allow_ok_btn.setGeometry(int(320 * X_rate), int(940 * Y_rate), int(120 * X_rate), int(70 * Y_rate))
        self.allow_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.allow_ok_btn.mousePressEvent = self.get_allow_ok_btn_press_event
        self.allow_ok_btn.mouseReleaseEvent = self.get_allow_ok_btn_release_event

        # ------------------ Gov Result Not Allow Screen ----
        self.notallow_textedit = QtWidgets.QTextEdit(self)
        self.notallow_textedit.setReadOnly(True)
        self.notallow_textedit.setGeometry(int(100 * X_rate), int(250 * Y_rate), int(560 * X_rate), int(200 * Y_rate))
        self.notallow_textedit.setStyleSheet(LAW_TEXTEDIT_STYLE)

        self.notallow_text = QtWidgets.QLabel(self)
        self.notallow_text.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Der Spieler ist gesperrt!"
        self.notallow_text.setText(text1)
        self.notallow_text.setGeometry(int(0 * X_rate), int(500 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.notallow_text.setStyleSheet(TEXT_STYLE_BIG)

        self.notallow_icon = QtWidgets.QLabel(self)
        self.notallow_icon.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/notallow.png")
        self.notallow_icon.setPixmap(pix)
        self.notallow_icon.setStyleSheet(LOGO_BACK_STYLE)
        self.notallow_icon.setGeometry(int(300 * X_rate), int(600 * Y_rate), int(150 * X_rate), int(150 * Y_rate))

        self.notallow_ok_btn = QtWidgets.QLabel(self)
        self.notallow_ok_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "OK"
        self.notallow_ok_btn.setText(text2)
        self.notallow_ok_btn.setGeometry(int(320 * X_rate), int(940 * Y_rate), int(120 * X_rate), int(70 * Y_rate))
        self.notallow_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.notallow_ok_btn.mousePressEvent = self.get_notallow_ok_btn_press_event
        self.notallow_ok_btn.mouseReleaseEvent = self.get_notallow_ok_btn_release_event

        # ------------------ Machine Screen ---------
        self.machine_text1 = QtWidgets.QLabel(self)
        self.machine_text1.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Wählen Sie ihr Gerät"
        self.machine_text1.setText(text1)
        self.machine_text1.setGeometry(int(0 * X_rate), int(100 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.machine_text1.setStyleSheet(TEXT_STYLE_BIG)

        self.machine_text2 = QtWidgets.QLabel(self)
        self.machine_text2.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Geschafft! Nach wählen des Geräts\nerscheint Ihr Freischaltungscode."
        self.machine_text2.setText(text1)
        self.machine_text2.setGeometry(int(0 * X_rate), int(150 * Y_rate), int(768 * X_rate), int(100 * Y_rate))
        self.machine_text2.setStyleSheet(TEXT_STYLE_SMALL)

        self.machine_right_btn = QtWidgets.QLabel(self)
        self.machine_right_btn.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/right.png")
        self.machine_right_btn.setPixmap(pix)
        self.machine_right_btn.setGeometry(int(620 * X_rate), int(300 * Y_rate), int(150 * X_rate), int(300 * Y_rate))
        self.machine_right_btn.setStyleSheet(LOGO_BACK_STYLE)
        self.machine_right_btn.mousePressEvent = self.get_machine_right_btn_press_event
        self.machine_right_btn.mouseReleaseEvent = self.get_machine_right_btn_release_event

        self.machine_left_btn = QtWidgets.QLabel(self)
        self.machine_left_btn.setScaledContents(True)
        pix = QtGui.QPixmap(ROOT_DIR + "/src/images/left.png")
        self.machine_left_btn.setPixmap(pix)
        self.machine_left_btn.setGeometry(int(0 * X_rate), int(300 * Y_rate), int(150 * X_rate), int(300 * Y_rate))
        self.machine_left_btn.setStyleSheet(LOGO_BACK_STYLE)
        self.machine_left_btn.mousePressEvent = self.get_machine_left_btn_press_event
        self.machine_left_btn.mouseReleaseEvent = self.get_machine_left_btn_release_event

        self.machine_text3 = QtWidgets.QLabel(self)
        self.machine_text3.setAlignment(QtCore.Qt.AlignCenter)
        text1 = "Code zum freischalten des Geräte"
        self.machine_text3.setText(text1)
        self.machine_text3.setGeometry(int(0 * X_rate), int(650 * Y_rate), int(768 * X_rate), int(50 * Y_rate))
        self.machine_text3.setStyleSheet(TEXT_STYLE_BIG)

        self.machine_code = QtWidgets.QLabel(self)
        self.machine_code.setAlignment(QtCore.Qt.AlignCenter)
        # text1 = "1234"
        # self.machine_code.setText(text1)
        self.machine_code.setGeometry(int(280 * X_rate), int(720 * Y_rate), int(200 * X_rate), int(100 * Y_rate))
        self.machine_code.setStyleSheet(RECT_STYLE1)

        self.machine_hilfe_btn = QtWidgets.QLabel(self)
        self.machine_hilfe_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "HILEF"
        self.machine_hilfe_btn.setText(text2)
        self.machine_hilfe_btn.setGeometry(int(100 * X_rate), int(940 * Y_rate), int(160 * X_rate), int(70 * Y_rate))
        self.machine_hilfe_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.machine_hilfe_btn.mousePressEvent = self.get_machine_hilfe_btn_press_event
        self.machine_hilfe_btn.mouseReleaseEvent = self.get_machine_hilfe_btn_release_event

        self.machine_abbreuch_btn = QtWidgets.QLabel(self)
        self.machine_abbreuch_btn.setAlignment(QtCore.Qt.AlignCenter)
        text2 = "ABBRUCH"
        self.machine_abbreuch_btn.setText(text2)
        self.machine_abbreuch_btn.setGeometry(int(420 * X_rate), int(940 * Y_rate), int(250 * X_rate), int(70 * Y_rate))
        self.machine_abbreuch_btn.setStyleSheet(BUTTON_RELEASE_STYLE)
        self.machine_abbreuch_btn.mousePressEvent = self.get_machine_abbreuch_btn_press_event
        self.machine_abbreuch_btn.mouseReleaseEvent = self.get_machine_abbreuch_btn_release_event

        # ------------------- keyboard screen ----------------------------------
        self.key_back = QtWidgets.QLabel(self)
        self.key_back.setGeometry(int(0 * X_rate), int(0 * Y_rate), int(768 * X_rate), int(1024 * Y_rate))
        self.key_back.setStyleSheet(KEYBOARD_BACK_STYLE)

        self.key_editline_value = QtWidgets.QLabel(self)
        self.key_editline_value.setGeometry(KEY_W, KEY_H - int(60 * Y_rate), int(726 * X_rate), int(50 * Y_rate))
        self.key_editline_value.setStyleSheet(KEYBOARD_LINEEDIT_STYLE)

        self.key_1_btn = QtWidgets.QLabel(self)
        text = "!\n1"
        self.key_1_btn.setText(text)
        self.key_1_btn.setGeometry(KEY_W + int(0 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate), int(70 * Y_rate))
        self.key_1_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_1_btn.mousePressEvent = self.get_key_1_btn_press_event
        self.key_1_btn.mouseReleaseEvent = self.get_key_1_btn_release_event

        self.key_2_btn = QtWidgets.QLabel(self)
        text = "@\n2"
        self.key_2_btn.setText(text)
        self.key_2_btn.setGeometry(KEY_W + int(52 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_2_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_2_btn.mousePressEvent = self.get_key_2_btn_press_event
        self.key_2_btn.mouseReleaseEvent = self.get_key_2_btn_release_event

        self.key_3_btn = QtWidgets.QLabel(self)
        text = "#\n3"
        self.key_3_btn.setText(text)
        self.key_3_btn.setGeometry(KEY_W + int(104 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_3_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_3_btn.mousePressEvent = self.get_key_3_btn_press_event
        self.key_3_btn.mouseReleaseEvent = self.get_key_3_btn_release_event

        self.key_4_btn = QtWidgets.QLabel(self)
        text = "$\n4"
        self.key_4_btn.setText(text)
        self.key_4_btn.setGeometry(KEY_W + int(156 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_4_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_4_btn.mousePressEvent = self.get_key_4_btn_press_event
        self.key_4_btn.mouseReleaseEvent = self.get_key_4_btn_release_event

        self.key_5_btn = QtWidgets.QLabel(self)
        text = "%\n5"
        self.key_5_btn.setText(text)
        self.key_5_btn.setGeometry(KEY_W + int(208 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_5_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_5_btn.mousePressEvent = self.get_key_5_btn_press_event
        self.key_5_btn.mouseReleaseEvent = self.get_key_5_btn_release_event

        self.key_6_btn = QtWidgets.QLabel(self)
        text = "^\n6"
        self.key_6_btn.setText(text)
        self.key_6_btn.setGeometry(KEY_W + int(260 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_6_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_6_btn.mousePressEvent = self.get_key_6_btn_press_event
        self.key_6_btn.mouseReleaseEvent = self.get_key_6_btn_release_event

        self.key_7_btn = QtWidgets.QLabel(self)
        text = "&\n7"
        self.key_7_btn.setText(text)
        self.key_7_btn.setGeometry(KEY_W + int(312 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_7_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_7_btn.mousePressEvent = self.get_key_7_btn_press_event
        self.key_7_btn.mouseReleaseEvent = self.get_key_7_btn_release_event

        self.key_8_btn = QtWidgets.QLabel(self)
        text = "*\n8"
        self.key_8_btn.setText(text)
        self.key_8_btn.setGeometry(KEY_W + int(364 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_8_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_8_btn.mousePressEvent = self.get_key_8_btn_press_event
        self.key_8_btn.mouseReleaseEvent = self.get_key_8_btn_release_event

        self.key_9_btn = QtWidgets.QLabel(self)
        text = "(\n9"
        self.key_9_btn.setText(text)
        self.key_9_btn.setGeometry(KEY_W + int(416 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_9_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_9_btn.mousePressEvent = self.get_key_9_btn_press_event
        self.key_9_btn.mouseReleaseEvent = self.get_key_9_btn_release_event

        self.key_0_btn = QtWidgets.QLabel(self)
        text = ")\n0"
        self.key_0_btn.setText(text)
        self.key_0_btn.setGeometry(KEY_W + int(468 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_0_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_0_btn.mousePressEvent = self.get_key_0_btn_press_event
        self.key_0_btn.mouseReleaseEvent = self.get_key_0_btn_release_event

        self.key_underline_btn = QtWidgets.QLabel(self)
        text = "-\n_"
        self.key_underline_btn.setText(text)
        self.key_underline_btn.setGeometry(KEY_W + int(520 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                           int(70 * Y_rate))
        self.key_underline_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_underline_btn.mousePressEvent = self.get_key_underline_btn_press_event
        self.key_underline_btn.mouseReleaseEvent = self.get_key_underline_btn_release_event

        self.key_plus_btn = QtWidgets.QLabel(self)
        text = "+\n="
        self.key_plus_btn.setText(text)
        self.key_plus_btn.setGeometry(KEY_W + int(572 * X_rate), KEY_H + int(0 * Y_rate), int(50 * X_rate),
                                      int(70 * Y_rate))
        self.key_plus_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_plus_btn.mousePressEvent = self.get_key_plus_btn_press_event
        self.key_plus_btn.mouseReleaseEvent = self.get_key_plus_btn_release_event

        self.key_backspace_btn = QtWidgets.QLabel(self)
        text = "BkSp"
        self.key_backspace_btn.setText(text)
        self.key_backspace_btn.setGeometry(KEY_W + int(624 * X_rate), KEY_H + int(0 * Y_rate), int(102 * X_rate),
                                           int(70 * Y_rate))
        self.key_backspace_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_backspace_btn.mousePressEvent = self.get_key_backspace_btn_press_event
        self.key_backspace_btn.mouseReleaseEvent = self.get_key_backspace_btn_release_event

        self.key_none1_btn = QtWidgets.QLabel(self)
        self.key_none1_btn.setGeometry(KEY_W + int(0 * X_rate), KEY_H + int(80 * Y_rate), int(28 * X_rate),
                                       int(70 * Y_rate))
        self.key_none1_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        self.key_q_btn = QtWidgets.QLabel(self)
        text = "Q"
        self.key_q_btn.setText(text)
        self.key_q_btn.setGeometry(KEY_W + int(30 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_q_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_q_btn.mousePressEvent = self.get_key_q_btn_press_event
        self.key_q_btn.mouseReleaseEvent = self.get_key_q_btn_release_event

        self.key_w_btn = QtWidgets.QLabel(self)
        text = "W"
        self.key_w_btn.setText(text)
        self.key_w_btn.setGeometry(KEY_W + int(82 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_w_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_w_btn.mousePressEvent = self.get_key_w_btn_press_event
        self.key_w_btn.mouseReleaseEvent = self.get_key_w_btn_release_event

        self.key_e_btn = QtWidgets.QLabel(self)
        text = "E"
        self.key_e_btn.setText(text)
        self.key_e_btn.setGeometry(KEY_W + int(134 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_e_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_e_btn.mousePressEvent = self.get_key_e_btn_press_event
        self.key_e_btn.mouseReleaseEvent = self.get_key_e_btn_release_event

        self.key_r_btn = QtWidgets.QLabel(self)
        text = "R"
        self.key_r_btn.setText(text)
        self.key_r_btn.setGeometry(KEY_W + int(186 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_r_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_r_btn.mousePressEvent = self.get_key_r_btn_press_event
        self.key_r_btn.mouseReleaseEvent = self.get_key_r_btn_release_event

        self.key_t_btn = QtWidgets.QLabel(self)
        text = "T"
        self.key_t_btn.setText(text)
        self.key_t_btn.setGeometry(KEY_W + int(238 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_t_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_t_btn.mousePressEvent = self.get_key_t_btn_press_event
        self.key_t_btn.mouseReleaseEvent = self.get_key_t_btn_release_event

        self.key_y_btn = QtWidgets.QLabel(self)
        text = "Y"
        self.key_y_btn.setText(text)
        self.key_y_btn.setGeometry(KEY_W + int(290 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_y_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_y_btn.mousePressEvent = self.get_key_y_btn_press_event
        self.key_y_btn.mouseReleaseEvent = self.get_key_y_btn_release_event

        self.key_u_btn = QtWidgets.QLabel(self)
        text = "U"
        self.key_u_btn.setText(text)
        self.key_u_btn.setGeometry(KEY_W + int(342 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_u_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_u_btn.mousePressEvent = self.get_key_u_btn_press_event
        self.key_u_btn.mouseReleaseEvent = self.get_key_u_btn_release_event

        self.key_i_btn = QtWidgets.QLabel(self)
        text = "I"
        self.key_i_btn.setText(text)
        self.key_i_btn.setGeometry(KEY_W + int(394 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_i_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_i_btn.mousePressEvent = self.get_key_i_btn_press_event
        self.key_i_btn.mouseReleaseEvent = self.get_key_i_btn_release_event

        self.key_o_btn = QtWidgets.QLabel(self)
        text = "O"
        self.key_o_btn.setText(text)
        self.key_o_btn.setGeometry(KEY_W + int(446 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_o_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_o_btn.mousePressEvent = self.get_key_o_btn_press_event
        self.key_o_btn.mouseReleaseEvent = self.get_key_o_btn_release_event

        self.key_p_btn = QtWidgets.QLabel(self)
        text = "P"
        self.key_p_btn.setText(text)
        self.key_p_btn.setGeometry(KEY_W + int(498 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_p_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_p_btn.mousePressEvent = self.get_key_p_btn_press_event
        self.key_p_btn.mouseReleaseEvent = self.get_key_p_btn_release_event

        self.key_PT1_btn = QtWidgets.QLabel(self)
        text = "{\n["
        self.key_PT1_btn.setText(text)
        self.key_PT1_btn.setGeometry(KEY_W + int(550 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT1_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT1_btn.mousePressEvent = self.get_key_PT1_btn_press_event
        self.key_PT1_btn.mouseReleaseEvent = self.get_key_PT1_btn_release_event

        self.key_PT2_btn = QtWidgets.QLabel(self)
        text = "}\n]"
        self.key_PT2_btn.setText(text)
        self.key_PT2_btn.setGeometry(KEY_W + int(602 * X_rate), KEY_H + int(80 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT2_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT2_btn.mousePressEvent = self.get_key_PT2_btn_press_event
        self.key_PT2_btn.mouseReleaseEvent = self.get_key_PT2_btn_release_event

        self.key_PT3_btn = QtWidgets.QLabel(self)
        text = "|\n\\"
        self.key_PT3_btn.setText(text)
        self.key_PT3_btn.setGeometry(KEY_W + int(654 * X_rate), KEY_H + int(80 * Y_rate), int(72 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT3_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT3_btn.mousePressEvent = self.get_key_PT3_btn_press_event
        self.key_PT3_btn.mouseReleaseEvent = self.get_key_PT3_btn_release_event

        self.key_tab_btn = QtWidgets.QLabel(self)
        text = "Tab"
        self.key_tab_btn.setText(text)
        self.key_tab_btn.setGeometry(KEY_W + int(0 * X_rate), KEY_H + int(160 * Y_rate), int(58 * X_rate),
                                     int(70 * Y_rate))
        self.key_tab_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_tab_btn.mousePressEvent = self.get_key_tab_btn_press_event
        self.key_tab_btn.mouseReleaseEvent = self.get_key_tab_btn_release_event

        self.key_a_btn = QtWidgets.QLabel(self)
        text = "A"
        self.key_a_btn.setText(text)
        self.key_a_btn.setGeometry(KEY_W + int(60 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_a_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_a_btn.mousePressEvent = self.get_key_a_btn_press_event
        self.key_a_btn.mouseReleaseEvent = self.get_key_a_btn_release_event

        self.key_s_btn = QtWidgets.QLabel(self)
        text = "S"
        self.key_s_btn.setText(text)
        self.key_s_btn.setGeometry(KEY_W + int(112 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_s_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_s_btn.mousePressEvent = self.get_key_s_btn_press_event
        self.key_s_btn.mouseReleaseEvent = self.get_key_s_btn_release_event

        self.key_d_btn = QtWidgets.QLabel(self)
        text = "D"
        self.key_d_btn.setText(text)
        self.key_d_btn.setGeometry(KEY_W + int(164 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_d_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_d_btn.mousePressEvent = self.get_key_d_btn_press_event
        self.key_d_btn.mouseReleaseEvent = self.get_key_d_btn_release_event

        self.key_f_btn = QtWidgets.QLabel(self)
        text = "F"
        self.key_f_btn.setText(text)
        self.key_f_btn.setGeometry(KEY_W + int(216 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_f_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_f_btn.mousePressEvent = self.get_key_f_btn_press_event
        self.key_f_btn.mouseReleaseEvent = self.get_key_f_btn_release_event

        self.key_g_btn = QtWidgets.QLabel(self)
        text = "G"
        self.key_g_btn.setText(text)
        self.key_g_btn.setGeometry(KEY_W + int(268 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_g_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_g_btn.mousePressEvent = self.get_key_g_btn_press_event
        self.key_g_btn.mouseReleaseEvent = self.get_key_g_btn_release_event

        self.key_h_btn = QtWidgets.QLabel(self)
        text = "H"
        self.key_h_btn.setText(text)
        self.key_h_btn.setGeometry(KEY_W + int(320 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_h_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_h_btn.mousePressEvent = self.get_key_h_btn_press_event
        self.key_h_btn.mouseReleaseEvent = self.get_key_h_btn_release_event

        self.key_j_btn = QtWidgets.QLabel(self)
        text = "J"
        self.key_j_btn.setText(text)
        self.key_j_btn.setGeometry(KEY_W + int(372 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_j_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_j_btn.mousePressEvent = self.get_key_j_btn_press_event
        self.key_j_btn.mouseReleaseEvent = self.get_key_j_btn_release_event

        self.key_k_btn = QtWidgets.QLabel(self)
        text = "K"
        self.key_k_btn.setText(text)
        self.key_k_btn.setGeometry(KEY_W + int(424 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_k_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_k_btn.mousePressEvent = self.get_key_k_btn_press_event
        self.key_k_btn.mouseReleaseEvent = self.get_key_k_btn_release_event

        self.key_l_btn = QtWidgets.QLabel(self)
        text = "L"
        self.key_l_btn.setText(text)
        self.key_l_btn.setGeometry(KEY_W + int(476 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_l_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_l_btn.mousePressEvent = self.get_key_l_btn_press_event
        self.key_l_btn.mouseReleaseEvent = self.get_key_l_btn_release_event

        self.key_PT4_btn = QtWidgets.QLabel(self)
        text = ":\n;"
        self.key_PT4_btn.setText(text)
        self.key_PT4_btn.setGeometry(KEY_W + int(528 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT4_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT4_btn.mousePressEvent = self.get_key_PT4_btn_press_event
        self.key_PT4_btn.mouseReleaseEvent = self.get_key_PT4_btn_release_event

        self.key_PT5_btn = QtWidgets.QLabel(self)
        text = '"\n'"'"''
        self.key_PT5_btn.setText(text)
        self.key_PT5_btn.setGeometry(KEY_W + int(580 * X_rate), KEY_H + int(160 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT5_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT5_btn.mousePressEvent = self.get_key_PT5_btn_press_event
        self.key_PT5_btn.mouseReleaseEvent = self.get_key_PT5_btn_release_event

        self.key_enter_btn = QtWidgets.QLabel(self)
        text = 'Enter'
        self.key_enter_btn.setText(text)
        self.key_enter_btn.setGeometry(KEY_W + int(632 * X_rate), KEY_H + int(160 * Y_rate), int(94 * X_rate),
                                       int(70 * Y_rate))
        self.key_enter_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_enter_btn.mousePressEvent = self.get_key_enter_btn_press_event
        self.key_enter_btn.mouseReleaseEvent = self.get_key_enter_btn_release_event

        self.key_shift_btn = QtWidgets.QLabel(self)
        text = 'Shift'
        self.key_shift_btn.setText(text)
        self.key_shift_btn.setGeometry(KEY_W + int(0 * X_rate), KEY_H + int(240 * Y_rate), int(88 * X_rate),
                                       int(70 * Y_rate))
        self.key_shift_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_shift_btn.mousePressEvent = self.get_key_shift_btn_press_event
        self.key_shift_btn.mouseReleaseEvent = self.get_key_shift_btn_release_event

        self.key_z_btn = QtWidgets.QLabel(self)
        text = 'Z'
        self.key_z_btn.setText(text)
        self.key_z_btn.setGeometry(KEY_W + int(90 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_z_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_z_btn.mousePressEvent = self.get_key_z_btn_press_event
        self.key_z_btn.mouseReleaseEvent = self.get_key_z_btn_release_event

        self.key_x_btn = QtWidgets.QLabel(self)
        text = 'X'
        self.key_x_btn.setText(text)
        self.key_x_btn.setGeometry(KEY_W + int(142 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_x_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_x_btn.mousePressEvent = self.get_key_x_btn_press_event
        self.key_x_btn.mouseReleaseEvent = self.get_key_x_btn_release_event

        self.key_c_btn = QtWidgets.QLabel(self)
        text = 'C'
        self.key_c_btn.setText(text)
        self.key_c_btn.setGeometry(KEY_W + int(194 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_c_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_c_btn.mousePressEvent = self.get_key_c_btn_press_event
        self.key_c_btn.mouseReleaseEvent = self.get_key_c_btn_release_event

        self.key_v_btn = QtWidgets.QLabel(self)
        text = 'V'
        self.key_v_btn.setText(text)
        self.key_v_btn.setGeometry(KEY_W + int(246 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_v_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_v_btn.mousePressEvent = self.get_key_v_btn_press_event
        self.key_v_btn.mouseReleaseEvent = self.get_key_v_btn_release_event

        self.key_b_btn = QtWidgets.QLabel(self)
        text = 'B'
        self.key_b_btn.setText(text)
        self.key_b_btn.setGeometry(KEY_W + int(298 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_b_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_b_btn.mousePressEvent = self.get_key_b_btn_press_event
        self.key_b_btn.mouseReleaseEvent = self.get_key_b_btn_release_event

        self.key_n_btn = QtWidgets.QLabel(self)
        text = 'N'
        self.key_n_btn.setText(text)
        self.key_n_btn.setGeometry(KEY_W + int(350 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_n_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_n_btn.mousePressEvent = self.get_key_n_btn_press_event
        self.key_n_btn.mouseReleaseEvent = self.get_key_n_btn_release_event

        self.key_m_btn = QtWidgets.QLabel(self)
        text = 'M'
        self.key_m_btn.setText(text)
        self.key_m_btn.setGeometry(KEY_W + int(402 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                   int(70 * Y_rate))
        self.key_m_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_m_btn.mousePressEvent = self.get_key_m_btn_press_event
        self.key_m_btn.mouseReleaseEvent = self.get_key_m_btn_release_event

        self.key_PT6_btn = QtWidgets.QLabel(self)
        text = '<\n,'
        self.key_PT6_btn.setText(text)
        self.key_PT6_btn.setGeometry(KEY_W + int(454 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT6_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT6_btn.mousePressEvent = self.get_key_PT6_btn_press_event
        self.key_PT6_btn.mouseReleaseEvent = self.get_key_PT6_btn_release_event

        self.key_PT7_btn = QtWidgets.QLabel(self)
        text = '>\n.'
        self.key_PT7_btn.setText(text)
        self.key_PT7_btn.setGeometry(KEY_W + int(506 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT7_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT7_btn.mousePressEvent = self.get_key_PT7_btn_press_event
        self.key_PT7_btn.mouseReleaseEvent = self.get_key_PT7_btn_release_event

        self.key_PT8_btn = QtWidgets.QLabel(self)
        text = '?\n/'
        self.key_PT8_btn.setText(text)
        self.key_PT8_btn.setGeometry(KEY_W + int(558 * X_rate), KEY_H + int(240 * Y_rate), int(50 * X_rate),
                                     int(70 * Y_rate))
        self.key_PT8_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_PT8_btn.mousePressEvent = self.get_key_PT8_btn_press_event
        self.key_PT8_btn.mouseReleaseEvent = self.get_key_PT8_btn_release_event

        self.key_space_btn = QtWidgets.QLabel(self)
        text = 'Space'
        self.key_space_btn.setText(text)
        self.key_space_btn.setGeometry(KEY_W + int(610 * X_rate), KEY_H + int(240 * Y_rate), int(116 * X_rate),
                                       int(70 * Y_rate))
        self.key_space_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)
        self.key_space_btn.mousePressEvent = self.get_key_space_btn_press_event
        self.key_space_btn.mouseReleaseEvent = self.get_key_space_btn_release_event

        # ------------------------------------------
        # self.hide_login_screen()
        self.hide_login_success_screen()
        self.hide_login_failed_screen()
        self.hide_menu_screen()
        self.hide_cert_screen()
        self.hide_machinesetting_screen()
        self.hide_wifi_screen()
        self.hide_admin_screen()
        self.hide_about_screen()
        self.hide_main_screen()
        self.hide_allow_screen()
        self.hide_notallow_screen()
        self.hide_machine_screen()
        self.hide_db_screen()
        self.hide_keyboard_screen()
        
        # --------------------------
        self.key_enter_pressed_signal.connect(self.on_key_enter_pressed)

        # ----- Start Keystroke Listener ---
        self.key_listen_thread = Thread(target=self.real_key_listen)
        self.key_listen_thread.setDaemon(True)
        self.key_listen_thread.start()
        
        # -----------------------------------------
        # self.setFixedSize(768, 1024)
        
        self.hide_login_screen()
        self.show_menu_screen()
        #self.show_main_screen()
        
        self.showFullScreen()

    def on_real_key_press(self, key):
        if key == Key.enter:
            self.key_enter_pressed_signal.emit()
        else:
            try:
                if self.edit_admin_password_flag:
                    text = self.key_editline_value.text()
                    if key == Key.backspace and len(text) > 0:
                        self.key_typed_string = self.key_typed_string[:-1]
                        text = text[:-1]
                    else:
                        if key == Key.space:
                            text += '*'
                            self.key_typed_string += ' '
                        else:
                            text += '*'
                            self.key_typed_string += key.char

                    self.key_editline_value.setText(text)
                else:
                    text = self.key_editline_value.text()
                    if key == Key.backspace and len(text) > 0:
                        self.key_typed_string = self.key_typed_string[:-1]
                        text = text[:-1]
                    else:
                        if key == Key.space:
                            text += ' '
                            self.key_typed_string += ' '
                        else:
                            text += key.char
                            self.key_typed_string += key.char

                    self.key_editline_value.setText(text)

            except:
                pass

    def real_key_listen(self):
        with Listener(on_press=self.on_real_key_press) as listener:
            listener.join()
    # ------------------------
    def on_key_enter_pressed(self):
        # ------- admin login ----------------------
        if self.edit_admin_id_flag:
            self.login_id_value.setText(self.key_editline_value.text())
            self.admin_id_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_admin_id_flag = False

        if self.edit_admin_password_flag:
            self.login_password_value.setText(self.key_editline_value.text())
            self.admin_password_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_admin_password_flag = False

        # --------- Oasis certification ------------
        if self.edit_cert_url_flag:
            self.cert_url_value.setText(self.key_editline_value.text())
            self.cert_url_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_url_flag = False

        if self.edit_cert_user_flag:
            self.cert_user_value.setText(self.key_editline_value.text())
            self.cert_user_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_user_flag = False

        if self.edit_cert_userpass_flag:
            self.cert_userpass_value.setText(self.key_editline_value.text())
            self.cert_userpass_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_userpass_flag = False

        if self.edit_cert_pass_flag:
            self.cert_pass_value.setText(self.key_editline_value.text())
            self.cert_pass_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_pass_flag = False

        # -------- admin setting -----------------
        if self.edit_adminsetting_user_flag:
            self.admin_user_value.setText(self.key_editline_value.text())
            self.adminsetting_user_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_adminsetting_user_flag = False

        if self.edit_adminsetting_password_flag:
            self.admin_pass_value.setText(self.key_editline_value.text())
            self.adminsetting_password_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_adminsetting_password_flag = False

        # ----------- WiFi setting -------------
        if self.edit_wifisetting_wlan_flag:
            self.wifi_wlan_value.setText(self.key_editline_value.text())
            self.wifisetting_wlan_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_wifisetting_wlan_flag = False

        if self.edit_wifisetting_essid_flag:
            self.wifi_essid_value.setText(self.key_editline_value.text())
            self.wifisetting_essid_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_wifisetting_essid_flag = False

        if self.edit_wifisetting_password_flag:
            self.wifi_pass_value.setText(self.key_editline_value.text())
            self.wifisetting_password_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_wifisetting_password_flag = False

        # ------------ Machine setting ----------
        if self.edit_machine_1_ip_flag:
            self.machinesetting_1_ip_value.setText(self.key_editline_value.text())
            self.machine_1_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_1_ip_flag = False

        if self.edit_machine_2_ip_flag:
            self.machinesetting_2_ip_value.setText(self.key_editline_value.text())
            self.machine_2_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_2_ip_flag = False

        if self.edit_machine_3_ip_flag:
            self.machinesetting_3_ip_value.setText(self.key_editline_value.text())
            self.machine_3_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_3_ip_flag = False

        if self.edit_machine_4_ip_flag:
            self.machinesetting_4_ip_value.setText(self.key_editline_value.text())
            self.machine_4_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_4_ip_flag = False

        if self.edit_machine_5_ip_flag:
            self.machinesetting_5_ip_value.setText(self.key_editline_value.text())
            self.machine_5_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_5_ip_flag = False

        if self.edit_machine_6_ip_flag:
            self.machinesetting_6_ip_value.setText(self.key_editline_value.text())
            self.machine_6_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_6_ip_flag = False

        if self.edit_machine_7_ip_flag:
            self.machinesetting_7_ip_value.setText(self.key_editline_value.text())
            self.machine_7_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_7_ip_flag = False

        if self.edit_machine_8_ip_flag:
            self.machinesetting_8_ip_value.setText(self.key_editline_value.text())
            self.machine_8_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_8_ip_flag = False

        if self.edit_machine_9_ip_flag:
            self.machinesetting_9_ip_value.setText(self.key_editline_value.text())
            self.machine_9_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_9_ip_flag = False

        if self.edit_machine_10_ip_flag:
            self.machinesetting_10_ip_value.setText(self.key_editline_value.text())
            self.machine_10_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_10_ip_flag = False

        if self.edit_machine_11_ip_flag:
            self.machinesetting_11_ip_value.setText(self.key_editline_value.text())
            self.machine_11_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_11_ip_flag = False

        if self.edit_machine_12_ip_flag:
            self.machinesetting_12_ip_value.setText(self.key_editline_value.text())
            self.machine_12_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_12_ip_flag = False

        if self.edit_machine_pass_flag:
            self.machinesetting_pass_value.setText(self.key_editline_value.text())
            self.machine_pass_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_pass_flag = False
        # ------ edit db manager info --------
        if self.edit_db_lastname_flag:
            self.db_lastname_value.setText(self.key_editline_value.text())
            self.key_typed_string = ''
            self.edit_db_lastname_flag = False

        if self.edit_db_birth_flag:
            self.db_birth_value.setText(self.key_editline_value.text())
            self.key_typed_string = ''
            self.edit_db_birth_flag = False
        # ---------- edit main info -----------
        if self.edit_name_flag:
            self.main_name_value.setText(self.key_editline_value.text())
            name = self.key_typed_string
            self.key_typed_string = ''
            try:
                self.card_firstname = name.split(' ')[0]
                self.card_lastname = name.split(' ')[1]
            except:
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(14)

                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Please Type Full name like format : Firstname LastName")
                msg.setWindowTitle("Invalid Name")
                msg.setFont(font)
                msg.exec_()

            self.check_info()

            self.edit_name_flag = False

        if self.edit_birth_flag:
            self.main_birth_value.setText(self.key_editline_value.text())
            self.card_birth = self.key_typed_string
            self.key_typed_string = ''

            try:
                self.card_age = self.calc_age(self.card_birth)
                if self.card_age > 18:
                    self.card_statue = 'Allow'
                else:
                    self.card_statue = 'Not Allow'

                self.main_age_value.setText(str(self.card_age))
                self.main_status_value.setText(self.card_statue)

            except:
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(14)

                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Please Type Birthday like format : DD.MM.YYYY")
                msg.setWindowTitle("Invalid Birthday")
                msg.setFont(font)
                msg.exec_()

            self.check_info()

            self.edit_birth_flag = False

        self.key_editline_value.clear()
        self.hide_keyboard_screen()



    def auto_hide_allow_screen(self):
        if self.auto_hide_allow_screen_flag:
            self.hide_allow_screen()
            self.show_menu_screen()
            self.auto_hide_allow_screen_flag = False

    def auto_hide_notallow_screen(self):
        if self.auto_hide_notallow_screen_flag:
            self.hide_notallow_screen()
            self.show_menu_screen()
            self.auto_hide_notallow_screen_flag = False

    def auto_hide_machine_screen(self):
        if self.auto_hide_machine_screen_flag:
            
            self.active_machine_screen = False
            
            self.hide_machine_screen()
            self.show_menu_screen()
            self.auto_hide_machine_screen_flag = False

    def show_login_screen(self):
        self.login_logo.show()
        self.login_text1.show()
        self.login_text2.show()
        self.login_id_value.show()
        self.login_password_value.show()
        self.login_btn.show()
        self.close_btn.show()

    def hide_login_screen(self):
        self.login_logo.hide()
        self.login_text1.hide()
        self.login_text2.hide()
        self.login_id_value.hide()
        self.login_password_value.hide()
        self.login_btn.hide()
        self.close_btn.hide()

    def show_login_success_screen(self):
        self.login_success_text.show()
        self.login_success_icon.show()
        self.login_success_ok_btn.show()

    def hide_login_success_screen(self):
        self.login_success_text.hide()
        self.login_success_icon.hide()
        self.login_success_ok_btn.hide()

    def show_login_failed_screen(self):
        self.login_failed_text.show()
        self.login_failed_icon.show()
        self.login_failed_ok_btn.show()

    def hide_login_failed_screen(self):
        self.login_failed_text.hide()
        self.login_failed_icon.hide()
        self.login_failed_ok_btn.hide()

    def show_menu_screen(self):
        self.menu_certsetting_button.show()
        self.menu_machinesetting_button.show()
        self.menu_wifisetting_button.show()
        self.menu_adminsetting_button.show()
        self.menu_about_button.show()
        self.menu_manual_button.show()
        self.menu_update_button.show()
        self.menu_machine_button.show()
        self.menu_db_button.show()
        self.menu_cancel_button.show()

    def hide_menu_screen(self):
        self.menu_certsetting_button.hide()
        self.menu_machinesetting_button.hide()
        self.menu_wifisetting_button.hide()
        self.menu_adminsetting_button.hide()
        self.menu_about_button.hide()
        self.menu_manual_button.hide()
        self.menu_update_button.hide()
        self.menu_machine_button.hide()
        self.menu_db_button.hide()
        self.menu_cancel_button.hide()

    def show_cert_screen(self):
        self.cert_logo.show()
        self.cert_text.show()
        self.cert_url_text.show()
        self.cert_url_value.show()
        self.cert_user_text.show()
        self.cert_user_value.show()
        self.cert_userpass_text.show()
        self.cert_userpass_value.show()
        self.cert_filepath_text.show()
        self.cert_filepath_value.show()
        self.cert_browse_button.show()
        self.cert_pass_text.show()
        self.cert_pass_value.show()
        self.cert_import_button.show()
        self.cert_ok_button.show()
        self.cert_cancel_button.show()

        filepath = './cert_files/cert_info.bin'

        if os.path.exists(filepath):
            self.set_cert_values(filepath)

    def hide_cert_screen(self):
        self.cert_logo.hide()
        self.cert_text.hide()
        self.cert_url_text.hide()
        self.cert_url_value.hide()
        self.cert_user_text.hide()
        self.cert_user_value.hide()
        self.cert_userpass_text.hide()
        self.cert_userpass_value.hide()
        self.cert_filepath_text.hide()
        self.cert_filepath_value.hide()
        self.cert_browse_button.hide()
        self.cert_pass_text.hide()
        self.cert_pass_value.hide()
        self.cert_import_button.hide()
        self.cert_ok_button.hide()
        self.cert_cancel_button.hide()

    def show_machinesetting_screen(self):
        paramFile = ROOT_DIR + "/config.ini"
        config = configparser.ConfigParser()
        config.read(paramFile)

        self.machinesetting_1_ip_value.setText(config.get("machine", "GSG-1-IP"))
        self.machinesetting_2_ip_value.setText(config.get("machine", "GSG-2-IP"))
        self.machinesetting_3_ip_value.setText(config.get("machine", "GSG-3-IP"))
        self.machinesetting_4_ip_value.setText(config.get("machine", "GSG-4-IP"))
        self.machinesetting_5_ip_value.setText(config.get("machine", "GSG-5-IP"))
        self.machinesetting_6_ip_value.setText(config.get("machine", "GSG-6-IP"))
        self.machinesetting_7_ip_value.setText(config.get("machine", "GSG-7-IP"))
        self.machinesetting_8_ip_value.setText(config.get("machine", "GSG-8-IP"))
        self.machinesetting_9_ip_value.setText(config.get("machine", "GSG-9-IP"))
        self.machinesetting_10_ip_value.setText(config.get("machine", "GSG-10-IP"))
        self.machinesetting_11_ip_value.setText(config.get("machine", "GSG-11-IP"))
        self.machinesetting_12_ip_value.setText(config.get("machine", "GSG-12-IP"))
        
        self.machinesetting_pass_value.setText(config.get("machine", "VDAI-Pass"))

        self.machinesetting_1_text.show()
        self.machinesetting_1_ip_value.show()
        self.machinesetting_2_text.show()
        self.machinesetting_2_ip_value.show()
        self.machinesetting_3_text.show()
        self.machinesetting_3_ip_value.show()
        self.machinesetting_4_text.show()
        self.machinesetting_4_ip_value.show()
        self.machinesetting_5_text.show()
        self.machinesetting_5_ip_value.show()
        self.machinesetting_6_text.show()
        self.machinesetting_6_ip_value.show()
        self.machinesetting_7_text.show()
        self.machinesetting_7_ip_value.show()
        self.machinesetting_8_text.show()
        self.machinesetting_8_ip_value.show()
        self.machinesetting_9_text.show()
        self.machinesetting_9_ip_value.show()
        self.machinesetting_10_text.show()
        self.machinesetting_10_ip_value.show()
        self.machinesetting_11_text.show()
        self.machinesetting_11_ip_value.show()
        self.machinesetting_12_text.show()
        self.machinesetting_12_ip_value.show()
        self.machinesetting_pass_text.show()
        self.machinesetting_pass_value.show()
        self.machinesetting_ok_button.show()
        self.machinesetting_cancel_button.show()

    def hide_machinesetting_screen(self):
        self.machinesetting_1_text.hide()
        self.machinesetting_1_ip_value.hide()
        self.machinesetting_2_text.hide()
        self.machinesetting_2_ip_value.hide()
        self.machinesetting_3_text.hide()
        self.machinesetting_3_ip_value.hide()
        self.machinesetting_4_text.hide()
        self.machinesetting_4_ip_value.hide()
        self.machinesetting_5_text.hide()
        self.machinesetting_5_ip_value.hide()
        self.machinesetting_6_text.hide()
        self.machinesetting_6_ip_value.hide()
        self.machinesetting_7_text.hide()
        self.machinesetting_7_ip_value.hide()
        self.machinesetting_8_text.hide()
        self.machinesetting_8_ip_value.hide()
        self.machinesetting_9_text.hide()
        self.machinesetting_9_ip_value.hide()
        self.machinesetting_10_text.hide()
        self.machinesetting_10_ip_value.hide()
        self.machinesetting_11_text.hide()
        self.machinesetting_11_ip_value.hide()
        self.machinesetting_12_text.hide()
        self.machinesetting_12_ip_value.hide()
        self.machinesetting_pass_text.hide()
        self.machinesetting_pass_value.hide()
        self.machinesetting_ok_button.hide()
        self.machinesetting_cancel_button.hide()

    def show_db_screen(self):
        self.db_tablewidget.show()
        self.db_label1.show()
        self.db_label2.show()
        self.db_lastname_value.show()
        self.db_birth_value.show()
        self.db_browse_btn.show()
        self.db_search_btn.show()
        self.db_path.show()
        self.db_delete_btn.show()
        self.db_cancel_btn.show()
        
    def hide_db_screen(self):
        self.db_tablewidget.hide()
        self.db_label1.hide()
        self.db_label2.hide()
        self.db_lastname_value.hide()
        self.db_birth_value.hide()
        self.db_browse_btn.hide()
        self.db_search_btn.hide()
        self.db_path.hide()
        self.db_delete_btn.hide()
        self.db_cancel_btn.hide()

    def show_wifi_screen(self):
        self.wifi_logo.show()
        self.wifi_text.show()
        # self.wifi_wlan_text.show()
        # self.wifi_wlan_value.show()
        self.wifi_essid_text.show()
        self.wifi_essid_value.show()
        self.wifi_pass_text.show()
        self.wifi_pass_value.show()
        self.wifi_ok_button.show()
        self.wifi_cancel_button.show()

    def hide_wifi_screen(self):
        self.wifi_logo.hide()
        self.wifi_text.hide()
        self.wifi_wlan_text.hide()
        self.wifi_wlan_value.hide()
        self.wifi_essid_text.hide()
        self.wifi_essid_value.hide()
        self.wifi_pass_text.hide()
        self.wifi_pass_value.hide()
        self.wifi_ok_button.hide()
        self.wifi_cancel_button.hide()

    def show_admin_screen(self):
        self.admin_logo.show()
        self.admin_text.show()
        self.admin_user_text.show()
        self.admin_user_value.show()
        self.admin_pass_text.show()
        self.admin_pass_value.show()
        self.admin_ok_button.show()
        self.admin_cancel_button.show()

    def hide_admin_screen(self):
        self.admin_logo.hide()
        self.admin_text.hide()
        self.admin_user_text.hide()
        self.admin_user_value.hide()
        self.admin_pass_text.hide()
        self.admin_pass_value.hide()
        self.admin_ok_button.hide()
        self.admin_cancel_button.hide()

    def show_about_screen(self):
        self.about_logo.show()
        self.about_text.show()
        self.about_appname_text.show()
        self.about_appname_value.show()
        self.about_macaddr_text.show()
        self.about_macaddr_value.show()
        self.about_serial_text.show()
        self.about_serial_value.show()
        self.about_total_request_text.show()
        self.about_total_request_value.setText(str(self.request_allow_counts + self.request_notallow_counts))
        self.about_total_request_value.show()
        self.about_allow_request_text.show()
        self.about_allow_request_value.setText(str(self.request_allow_counts))
        self.about_allow_request_value.show()
        self.about_notallow_request_text.show()
        self.about_notallow_request_value.setText(str(self.request_notallow_counts))
        self.about_notallow_request_value.show()
        self.about_cancel_button.show()

    def hide_about_screen(self):
        self.about_logo.hide()
        self.about_text.hide()
        self.about_appname_text.hide()
        self.about_appname_value.hide()
        self.about_macaddr_text.hide()
        self.about_macaddr_value.hide()
        self.about_serial_text.hide()
        self.about_serial_value.hide()
        self.about_total_request_text.hide()
        self.about_total_request_value.hide()
        self.about_allow_request_text.hide()
        self.about_allow_request_value.hide()
        self.about_notallow_request_text.hide()
        self.about_notallow_request_value.hide()
        self.about_cancel_button.hide()

    def show_main_screen(self):
        self.main_name_value.clear()
        self.main_birth_value.clear()
        self.main_age_value.clear()
        self.main_status_value.clear()
        
        self.main_logo.show()
        self.main_text.show()
        self.main_face.show()
        self.main_text_name.show()
        self.main_name_value.show()
        self.main_text_birth.show()
        self.main_birth_value.show()
        self.main_text_age.show()
        self.main_age_value.show()
        self.main_text_status.show()
        self.main_status_value.show()
        self.main_text1.show()
        self.main_ok_btn.show()
        # self.main_hilfe_btn.show()
        self.main_abbreuch_btn.show()

    def hide_main_screen(self):
        self.main_logo.hide()
        self.main_text.hide()
        self.main_face.hide()
        self.main_text_name.hide()
        self.main_name_value.hide()
        self.main_text_birth.hide()
        self.main_birth_value.hide()
        self.main_text_age.hide()
        self.main_age_value.hide()
        self.main_text_status.hide()
        self.main_status_value.hide()
        self.main_text1.hide()
        self.main_ok_btn.hide()
        self.main_hilfe_btn.hide()
        self.main_abbreuch_btn.hide()

    def show_allow_screen(self):
        self.allow_textedit.show()
        self.allow_text.show()
        self.allow_icon.show()
        self.allow_ok_btn.show()

    def hide_allow_screen(self):
        self.allow_textedit.hide()
        self.allow_text.hide()
        self.allow_icon.hide()
        self.allow_ok_btn.hide()

    def show_notallow_screen(self):
        self.notallow_textedit.show()
        self.notallow_text.show()
        self.notallow_icon.show()
        self.notallow_ok_btn.show()

    def hide_notallow_screen(self):
        self.notallow_textedit.hide()
        self.notallow_text.hide()
        self.notallow_icon.hide()
        self.notallow_ok_btn.hide()

    def show_machine_screen(self):
        self.machine_text1.show()
        self.machine_text2.show()
        self.machine_right_btn.show()
        self.machine_left_btn.show()
        self.machine_text3.show()
        self.machine_code.show()
        self.machine_hilfe_btn.show()
        self.machine_abbreuch_btn.show()

    def hide_machine_screen(self):
        self.machine_text1.hide()
        self.machine_text2.hide()
        self.machine_right_btn.hide()
        self.machine_left_btn.hide()
        self.machine_text3.hide()
        self.machine_code.clear()
        self.machine_code.hide()
        self.machine_hilfe_btn.hide()
        self.machine_abbreuch_btn.hide()

    def show_keyboard_screen(self):
        self.key_back.show()
        self.key_editline_value.show()
        self.key_1_btn.show()
        self.key_2_btn.show()
        self.key_3_btn.show()
        self.key_4_btn.show()
        self.key_5_btn.show()
        self.key_6_btn.show()
        self.key_7_btn.show()
        self.key_8_btn.show()
        self.key_9_btn.show()
        self.key_0_btn.show()
        self.key_underline_btn.show()
        self.key_plus_btn.show()
        self.key_backspace_btn.show()
        self.key_none1_btn.show()
        self.key_q_btn.show()
        self.key_w_btn.show()
        self.key_e_btn.show()
        self.key_r_btn.show()
        self.key_t_btn.show()
        self.key_y_btn.show()
        self.key_u_btn.show()
        self.key_i_btn.show()
        self.key_o_btn.show()
        self.key_p_btn.show()
        self.key_PT1_btn.show()
        self.key_PT2_btn.show()
        self.key_PT3_btn.show()
        self.key_tab_btn.show()
        self.key_a_btn.show()
        self.key_s_btn.show()
        self.key_d_btn.show()
        self.key_f_btn.show()
        self.key_g_btn.show()
        self.key_h_btn.show()
        self.key_j_btn.show()
        self.key_k_btn.show()
        self.key_l_btn.show()
        self.key_PT4_btn.show()
        self.key_PT5_btn.show()
        self.key_enter_btn.show()
        self.key_space_btn.show()
        self.key_z_btn.show()
        self.key_x_btn.show()
        self.key_c_btn.show()
        self.key_v_btn.show()
        self.key_b_btn.show()
        self.key_n_btn.show()
        self.key_m_btn.show()
        self.key_PT6_btn.show()
        self.key_PT7_btn.show()
        self.key_PT8_btn.show()
        self.key_shift_btn.show()

    def hide_keyboard_screen(self):
        self.key_back.hide()
        self.key_editline_value.hide()
        self.key_1_btn.hide()
        self.key_2_btn.hide()
        self.key_3_btn.hide()
        self.key_4_btn.hide()
        self.key_5_btn.hide()
        self.key_6_btn.hide()
        self.key_7_btn.hide()
        self.key_8_btn.hide()
        self.key_9_btn.hide()
        self.key_0_btn.hide()
        self.key_underline_btn.hide()
        self.key_plus_btn.hide()
        self.key_backspace_btn.hide()
        self.key_none1_btn.hide()
        self.key_q_btn.hide()
        self.key_w_btn.hide()
        self.key_e_btn.hide()
        self.key_r_btn.hide()
        self.key_t_btn.hide()
        self.key_y_btn.hide()
        self.key_u_btn.hide()
        self.key_i_btn.hide()
        self.key_o_btn.hide()
        self.key_p_btn.hide()
        self.key_PT1_btn.hide()
        self.key_PT2_btn.hide()
        self.key_PT3_btn.hide()
        self.key_tab_btn.hide()
        self.key_a_btn.hide()
        self.key_s_btn.hide()
        self.key_d_btn.hide()
        self.key_f_btn.hide()
        self.key_g_btn.hide()
        self.key_h_btn.hide()
        self.key_j_btn.hide()
        self.key_k_btn.hide()
        self.key_l_btn.hide()
        self.key_PT4_btn.hide()
        self.key_PT5_btn.hide()
        self.key_enter_btn.hide()
        self.key_space_btn.hide()
        self.key_z_btn.hide()
        self.key_x_btn.hide()
        self.key_c_btn.hide()
        self.key_v_btn.hide()
        self.key_b_btn.hide()
        self.key_n_btn.hide()
        self.key_m_btn.hide()
        self.key_PT6_btn.hide()
        self.key_PT7_btn.hide()
        self.key_PT8_btn.hide()
        self.key_shift_btn.hide()

    # ---------- Log in screen event -------
    def get_login_id_value_press_event(self, event):
        self.edit_admin_id_flag = True

        self.show_keyboard_screen()

    def get_login_password_value_press_event(self, event):
        self.edit_admin_password_flag = True

        self.show_keyboard_screen()

    def get_login_btn_press_event(self, event):
        self.login_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_login_btn_release_event(self, event):
        self.login_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        file = open(ROOT_DIR + '/admin_info/admin_info.bin', 'rb')
        encrypted_data = file.read()
        decrypted_data = self.encryptor.decrypt(encrypted_data).decode()

        user = decrypted_data.split('***')[0]
        password = decrypted_data.split('***')[1]

        if self.admin_id_value_string == user and self.admin_password_value_string == password:
            self.show_login_success_screen()
        else:
            self.show_login_failed_screen()

        self.hide_login_screen()

        self.admin_id_value_string = ''
        self.admin_password_value_string = ''
        self.login_id_value.clear()
        self.login_password_value.clear()

    def get_close_btn_press_event(self, event):
        self.close_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_close_btn_release_event(self, event):
        self.close_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.close()

    # ---------- Log in success screen event ---------
    def get_login_success_ok_btn_press_event(self, event):
        self.login_success_ok_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_login_success_ok_btn_release_event(self, event):
        self.login_success_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_login_success_screen()
        self.show_menu_screen()

    # ---------- Log in failed screen event ---------
    def get_login_failed_ok_btn_press_event(self, event):
        self.login_failed_ok_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_login_failed_ok_btn_release_event(self, event):
        self.login_failed_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_login_failed_screen()
        self.show_login_screen()

    # ----------- Menu screen event -----------------
    def get_menu_certsetting_button_press_event(self, event):
        self.menu_certsetting_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_certsetting_button_release_event(self, event):
        self.menu_certsetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_menu_screen()
        self.show_cert_screen()

    def get_menu_machinesetting_button_press_event(self, event):
        self.menu_machinesetting_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_machinesetting_button_release_event(self, event):
        self.menu_machinesetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_menu_screen()
        self.show_machinesetting_screen()

    def get_menu_wifisetting_button_press_event(self, event):
        self.menu_wifisetting_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_wifisetting_button_release_event(self, event):
        self.menu_wifisetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_menu_screen()
        self.show_wifi_screen()

    def get_menu_manual_button_press_event(self, event):
        self.menu_manual_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_manual_button_release_event(self, event):
        self.menu_manual_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_menu_screen()
        self.show_main_screen()

    def get_menu_update_button_press_event(self, event):
        self.menu_update_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_update_button_release_event(self, event):
        self.menu_update_button.setStyleSheet(BUTTON_RELEASE_STYLE)

    def get_menu_db_button_press_event(self, event):
        self.menu_db_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_db_button_release_event(self, event):
        self.menu_db_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        
        self.hide_menu_screen()
        self.show_db_screen()

    def get_menu_machine_button_press_event(self, event):
        self.menu_machine_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_machine_button_release_event(self, event):
        self.menu_machine_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        
        # if self.active_machine_screen:
        self.hide_menu_screen()
        self.show_machine_screen()
        
        self.auto_hide_machine_screen_flag = True
        self.timer.singleShot(16000, self.auto_hide_machine_screen)


    def get_menu_adminsetting_button_press_event(self, event):
        self.menu_adminsetting_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_adminsetting_button_release_event(self, event):
        self.menu_adminsetting_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_menu_screen()
        self.show_admin_screen()

    def get_menu_about_button_press_event(self, event):
        self.menu_about_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_about_button_release_event(self, event):
        self.menu_about_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_menu_screen()
        self.show_about_screen()

    def get_menu_cancel_button_press_event(self, event):
        self.menu_cancel_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_menu_cancel_button_release_event(self, event):
        self.menu_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        
        self.close()
        #self.hide_menu_screen()
        #self.show_login_screen()

    # --------------------- Certification screen event -----------------
    def get_cert_url_value_press_event(self, event):
        self.edit_cert_url_flag = True

        self.show_keyboard_screen()

    def get_cert_user_value_press_event(self, event):
        self.edit_cert_user_flag = True

        self.show_keyboard_screen()

    def get_cert_userpass_value_press_event(self, event):
        self.edit_cert_userpass_flag = True

        self.show_keyboard_screen()

    def get_cert_pass_value_press_event(self, event):
        self.edit_cert_pass_flag = True

        self.show_keyboard_screen()

    def get_cert_browse_button_press_event(self, event):
        self.cert_browse_button.setStyleSheet(BUTTON_PRESS_STYLE)


    def get_cert_browse_button_release_event(self, event):
        self.cert_browse_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        self.cert_filepath_value.setText(fileName)
        self.cert_filepath_value_string = fileName

    def get_cert_import_button_press_event(self, event):
        self.cert_import_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_cert_import_button_release_event(self, event):
        self.cert_import_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            f.close()

            for line in lines:
                if 'Kennung' in line:
                    self.cert_user_value.setText(line.split(':', 1)[1].replace(' ', '').replace('\n', ''))
                    self.cert_user_value_string = line.split(':', 1)[1].replace(' ', '').replace('\n', '')

                if 'Pass1' in line:
                    self.cert_userpass_value.setText(line.split(':', 1)[1].replace(' ', '').replace('\n', ''))
                    self.cert_userpass_value_string = line.split(':', 1)[1].replace(' ', '').replace('\n', '')
                if 'Pass2' in line:
                    self.cert_pass_value.setText(line.split(':', 1)[1].replace(' ', '').replace('\n', ''))
                    self.cert_pass_value_string = line.split(':', 1)[1].replace(' ', '').replace('\n', '')

        except:
            pass

    def get_cert_ok_button_press_event(self, event):
        self.cert_ok_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def encrypt_cert(self, url, user, userpass, certpass):
        data_str = url + '***' + user + '***' + userpass + '***' + certpass
        encrypted_data = self.encryptor.encrypt(data_str.encode())

        file = open('./cert_files/cert_info.bin', 'wb')
        file.write(encrypted_data)
        file.close()

    def get_cert_ok_button_release_event(self, event):
        self.cert_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        print('####################')
        print(self.cert_url_value_string)
        if self.cert_url_value_string != '' \
                and self.cert_user_value_string != '' \
                and self.cert_userpass_value_string != '' \
                and self.cert_filepath_value_string != '' \
                and self.cert_pass_value_string != '':
            cert_file_path = ROOT_DIR + '/cert_files/cert_file.p12'
            print('#########################')
            print(cert_file_path )
            copy2(self.cert_filepath_value_string, cert_file_path)

            info = []
            info.append(self.cert_url_value_string)
            info.append(self.cert_user_value_string)
            info.append(self.cert_userpass_value_string)
            info.append(self.cert_filepath_value_string)
            info.append(self.cert_pass_value_string)
            self.certification_info = info

            self.encrypt_cert(info[0], info[1], info[2], info[4])

            self.hide_cert_screen()
            self.show_menu_screen()

    def set_cert_values(self, filepath):
        try:
            f = open(filepath, 'rb')
            encrypted_data = f.read()
            f.close()
            decrypted_data = self.encryptor.decrypt(encrypted_data).decode()

            list = decrypted_data.split('***')

            self.cert_url_value.setText(list[0])
            self.cert_url_value_string = list[0]

            self.cert_user_value.setText(list[1])
            self.cert_user_value_string = list[1]

            self.cert_userpass_value.setText(list[2])
            self.cert_userpass_value_string = list[2]

            self.cert_pass_value.setText(list[3])
            self.cert_pass_value_string = list[3]

        except:
            pass

    def get_cert_cancel_button_press_event(self, event):
        self.cert_cancel_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_cert_cancel_button_release_event(self, event):
        self.cert_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_cert_screen()
        self.show_menu_screen()
        
    # ------------------- db manager screen event ------
    def show_db_data(self, data):
        self.db_tablewidget.clearContents()

        if len(data) > 0:
            self.db_tablewidget.setRowCount(len(data))
            self.db_tablewidget.setColumnCount(len(data[0]))
            self.db_tablewidget.setHorizontalHeaderLabels(
                ["Index", "Date", "First Name", "Last Name", "Birthday", "Statue", "Encodding", "Address"])
            for i, (idx, date, statue, encodding, firstname, lastname, birth, save) in enumerate(data):
                item_idx = QtWidgets.QTableWidgetItem(str(idx))
                item_idx.setBackground(QtGui.QColor(255, 255, 245))
                item_date = QtWidgets.QTableWidgetItem(date)
                item_date.setBackground(QtGui.QColor(255, 245, 255))
                item_statue = QtWidgets.QTableWidgetItem(statue)
                item_statue.setBackground(QtGui.QColor(245, 255, 255))
                item_encodding = QtWidgets.QTableWidgetItem(encodding)
                item_encodding.setBackground(QtGui.QColor(245, 245, 255))
                item_firstname = QtWidgets.QTableWidgetItem(firstname)
                item_firstname.setBackground(QtGui.QColor(245, 255, 245))
                item_lastname = QtWidgets.QTableWidgetItem(lastname)
                item_lastname.setBackground(QtGui.QColor(255, 245, 245))
                item_birth = QtWidgets.QTableWidgetItem(birth)
                item_birth.setBackground(QtGui.QColor(245, 245, 245))
                item_save = QtWidgets.QTableWidgetItem(save)
                item_save.setBackground(QtGui.QColor(245, 245, 255))

                print(lastname)
                print(birth)

                self.db_tablewidget.setItem(i, 0, item_idx)
                self.db_tablewidget.setItem(i, 1, item_date)
                self.db_tablewidget.setItem(i, 2, item_firstname)
                self.db_tablewidget.setItem(i, 3, item_lastname)
                self.db_tablewidget.setItem(i, 4, item_birth)
                self.db_tablewidget.setItem(i, 5, item_statue)
                self.db_tablewidget.setItem(i, 6, item_encodding)
                self.db_tablewidget.setItem(i, 7, item_save)

    def get_db_search_btn_press_event(self, event):
        self.db_search_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_db_search_btn_release_event(self, event):
        self.db_search_btn.setStyleSheet(BUTTON_RELEASE_STYLE)


        if len(self.db_data) > 0:
            if self.db_lastname_value.text() == '' and self.db_birth_value.text() == '':
                self.show_db_data(self.db_data)

            else:
                search_result = []
                for i, (idx, date, statue, encodding, firstname, lastname, birth, save) in enumerate(self.db_data):
                    if lastname.lower() == self.db_lastname_value.text().lower() or birth.lower() == self.db_birth_value.text().lower():
                        search_result.append((idx, date, statue, encodding, firstname, lastname, birth, save))

                self.show_db_data(search_result)

    def get_db_browse_btn_press_event(self, event):
        self.db_browse_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_db_browse_btn_release_event(self, event):
        self.db_browse_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        self.db_path.setText(fileName)
        self.db_file_path = fileName

        self.db_data = self.fetch_data(self.db_file_path)
        self.show_db_data(self.db_data)

    def fetch_data(self, path):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    
        query = "SELECT * FROM `face_encoding_table`"
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
    
        print(rows)
    
        return rows
    
    
    def delete_data(self, path, firstname, lastname, birth):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    
        cursor.execute("DELETE FROM `face_encoding_table` WHERE name =? AND surname = ? AND birthday = ?", (firstname, lastname, birth ))
        connection.commit()
        connection.close()

    def get_db_delete_btn_press_event(self, event):
        self.db_delete_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_db_delete_btn_release_event(self, event):
        self.db_delete_btn.setStyleSheet(BUTTON_RELEASE_STYLE)


        selected_row = self.db_tablewidget.currentRow()
        if selected_row != -1:

            idx = str(self.db_tablewidget.item(selected_row, 0).text())
            first_name = self.db_tablewidget.item(selected_row, 2).text()
            last_name = self.db_tablewidget.item(selected_row, 3).text()
            birth = self.db_tablewidget.item(selected_row, 4).text()
            print(idx)

            self.delete_data(self.db_file_path, first_name, last_name, birth)

            self.db_tablewidget.removeRow(selected_row)

    def get_db_cancel_btn_press_event(self, event):
        self.db_cancel_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_db_cancel_btn_release_event(self, event):
        self.db_cancel_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_db_screen()
        self.show_menu_screen()

    def get_db_lastname_value_press_event(self, event):
        self.edit_db_lastname_flag = True
        self.show_keyboard_screen()

    def get_db_birth_value_press_event(self, event):
        self.edit_db_birth_flag = True
        self.show_keyboard_screen()

    # --------------------- machinesetting setting screen event ---------------
    def get_machinesetting_1_ip_value_press_event(self, event):
        self.edit_machine_1_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_2_ip_value_press_event(self, event):
        self.edit_machine_2_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_3_ip_value_press_event(self, event):
        self.edit_machine_3_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_4_ip_value_press_event(self, event):
        self.edit_machine_4_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_5_ip_value_press_event(self, event):
        self.edit_machine_5_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_6_ip_value_press_event(self, event):
        self.edit_machine_6_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_7_ip_value_press_event(self, event):
        self.edit_machine_7_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_8_ip_value_press_event(self, event):
        self.edit_machine_8_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_9_ip_value_press_event(self, event):
        self.edit_machine_9_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_10_ip_value_press_event(self, event):
        self.edit_machine_10_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_11_ip_value_press_event(self, event):
        self.edit_machine_11_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_12_ip_value_press_event(self, event):
        self.edit_machine_12_ip_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_pass_value_press_event(self, event):
        self.edit_machine_pass_flag = True

        self.show_keyboard_screen()

    def get_machinesetting_ok_button_press_event(self, event):
        self.machinesetting_ok_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_machinesetting_ok_button_release_event(self, event):
        self.machinesetting_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        paramFile = ROOT_DIR + "/config.ini"
        config = configparser.ConfigParser()
        config.read(paramFile)

        if self.machine_1_ip_value_string != '':
            config.set("machine", "GSG-1-IP", self.machine_1_ip_value_string)
        if self.machine_2_ip_value_string != '':
            config.set("machine", "GSG-2-IP", self.machine_2_ip_value_string)
        if self.machine_3_ip_value_string != '':
            config.set("machine", "GSG-3-IP", self.machine_3_ip_value_string)
        if self.machine_4_ip_value_string != '':
            config.set("machine", "GSG-4-IP", self.machine_4_ip_value_string)
        if self.machine_5_ip_value_string != '':
            config.set("machine", "GSG-5-IP", self.machine_5_ip_value_string)
        if self.machine_6_ip_value_string != '':
            config.set("machine", "GSG-6-IP", self.machine_6_ip_value_string)
        if self.machine_7_ip_value_string != '':
            config.set("machine", "GSG-7-IP", self.machine_7_ip_value_string)
        if self.machine_8_ip_value_string != '':
            config.set("machine", "GSG-8-IP", self.machine_8_ip_value_string)
        if self.machine_9_ip_value_string != '':
            config.set("machine", "GSG-9-IP", self.machine_9_ip_value_string)
        if self.machine_10_ip_value_string != '':
            config.set("machine", "GSG-10-IP", self.machine_10_ip_value_string)
        if self.machine_11_ip_value_string != '':
            config.set("machine", "GSG-11-IP", self.machine_11_ip_value_string)
        if self.machine_12_ip_value_string != '':
            config.set("machine", "GSG-12-IP", self.machine_12_ip_value_string)
        if self.machine_pass_value_string != '':
            config.set("machine", "VDAI-Pass", self.machine_pass_value_string)

        with open(paramFile, 'w') as file:
            config.write(file)

        self.hide_machinesetting_screen()
        self.show_menu_screen()

    def get_machinesetting_cancel_button_press_event(self, event):
        self.machinesetting_cancel_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_machinesetting_cancel_button_release_event(self, event):
        self.machinesetting_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_machinesetting_screen()
        self.show_menu_screen()

    # --------------------- WIFI setting screen event ---------------
    def get_wifi_wlan_value_press_event(self, event):
        self.edit_wifisetting_wlan_flag = True

        self.show_keyboard_screen()

    def get_wifi_essid_value_press_event(self, event):
        self.edit_wifisetting_essid_flag = True

        self.show_keyboard_screen()

    def get_wifi_pass_value_press_event(self, event):
        self.edit_wifisetting_password_flag = True

        self.show_keyboard_screen()

    def get_wifi_ok_button_press_event(self, event):
        self.wifi_ok_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_wifi_ok_button_release_event(self, event):
        self.wifi_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)
        
               
        if self.wifisetting_essid_value_string != '' \
                and self.wifisetting_password_value_string != '':
            # os.system('iwconfig ' + self.wifisetting_wlan_value_string + ' essid ' + self.wifisetting_essid_value_string + ' key ' + self.wifisetting_password_value_string)
            
            #setting up file contents
            config_lines = [
                'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
                'update_config=1',
                'country=DE',
                '\n',
                'network={',
                '\tssid="{}"'.format(self.wifisetting_essid_value_string),
                '\tpsk="{}"'.format(self.wifisetting_password_value_string),
                '}'
                ]
            config = '\n'.join(config_lines)
            
            # display additions
            print(config)
            
            # give access and writing. may have to do this manually beforehand
            os.popen("sudo chmod 0777 /etc/wpa_supplicant/wpa_supplicant.conf")
            
            # writing to file
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
                wifi.write(config)
            
            # displaying success
            print("wifi config added")
            
            # Reboot
            os.popen("sudo reboot")
            
            self.hide_wifi_screen()
            self.show_menu_screen()

    def get_wifi_cancel_button_press_event(self, event):
        self.wifi_cancel_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_wifi_cancel_button_release_event(self, event):
        self.wifi_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_wifi_screen()
        self.show_menu_screen()

    # --------------------- Admin setting screen event ---------------
    def get_admin_user_value_press_event(self, event):
        self.edit_adminsetting_user_flag = True

        self.show_keyboard_screen()

    def get_admin_pass_value_press_event(self, event):
        self.edit_adminsetting_password_flag = True

        self.show_keyboard_screen()

    def get_admin_ok_button_press_event(self, event):
        self.admin_ok_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_admin_ok_button_release_event(self, event):
        self.admin_ok_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        if self.adminsetting_user_value_string != '' \
                and self.adminsetting_password_value_string != '':
            data_str = self.adminsetting_user_value_string + '***' + self.adminsetting_password_value_string
            encrypted_data = self.encryptor.encrypt(data_str.encode())

            file = open(ROOT_DIR + '/admin_info/admin_info.bin', 'wb')
            file.write(encrypted_data)
            file.close()

            self.hide_admin_screen()
            self.show_menu_screen()

    def get_admin_cancel_button_press_event(self, event):
        self.admin_cancel_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_admin_cancel_button_release_event(self, event):
        self.admin_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_admin_screen()
        self.show_menu_screen()

    # --------------------- Admin setting screen event ---------------
    def get_about_cancel_button_press_event(self, event):
        self.about_cancel_button.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_about_cancel_button_release_event(self, event):
        self.about_cancel_button.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_about_screen()
        self.show_menu_screen()
    # ------------- Main Screen Event --------------
    def get_main_name_value_press_event(self, event):
        self.edit_name_flag = True
        self.show_keyboard_screen()

    def get_main_birth_value_press_event(self, event):
        self.edit_birth_flag = True
        self.show_keyboard_screen()

    def get_main_ok_btn_press_event(self, event):
        self.main_ok_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_main_ok_btn_release_event(self, event):
        self.main_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        if self.active_gov_request:
            try:
                print("Request info to server : ", self.card_firstname, self.card_lastname, self.card_birth)
                gov_msg = connect_gov("1234", self.card_firstname, self.card_lastname, self.card_birth, self.encryptor)
                # gov_msg = "Der Spieler ist nicht gesperrt."
                if gov_msg == "Der Spieler ist nicht gesperrt.":
                    # self.allow_textedit.clear()
                    
                    self.active_machine_screen = True
                    
                    self.allow_textedit.setText(gov_msg)

                    self.hide_main_screen()
                    self.show_allow_screen()

                    ########### AUto Hide ###########
                    self.auto_hide_allow_screen_flag = True
                    self.timer.singleShot(16000, self.auto_hide_allow_screen)
                    self.request_allow_counts += 1
                else:
                    # self.notallow_textedit.clear()
                    self.notallow_textedit.setText(gov_msg)

                    self.hide_main_screen()
                    self.show_notallow_screen()

                    ############ Auto Hide #######
                    self.auto_hide_notallow_screen_flag = True
                    self.timer.singleShot(16000, self.auto_hide_notallow_screen)
                    self.request_notallow_counts += 1
                
                file = open("statistical_counts.txt", 'w')
                file.write(str(self.request_allow_counts) + ':' + str(self.request_notallow_counts))
                file.close()
                
            except:
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(14)

                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("WIFI Connection is Failed!\n\nPlease connect WIFI and try again.")
                msg.setWindowTitle("WiFi Connection Failed")
                msg.setFont(font)
                msg.exec_()


    def get_main_hilfe_btn_press_event(self, event):
        self.main_hilfe_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_main_hilfe_btn_release_event(self, event):
        self.main_hilfe_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

    def get_main_abbreuch_btn_press_event(self, event):
        self.main_abbreuch_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_main_abbreuch_btn_release_event(self, event):
        self.main_abbreuch_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_main_screen()
        self.show_menu_screen()

    # ------------ Gov Allow Screen Event -------
    def get_allow_ok_btn_press_event(self, event):
        self.allow_ok_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_allow_ok_btn_release_event(self, event):
        self.allow_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_allow_screen()
        self.show_menu_screen()

        self.auto_hide_allow_screen_flag = False

    # ------------ Gov Not Allow Screen Event -------
    def get_notallow_ok_btn_press_event(self, event):
        self.notallow_ok_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_notallow_ok_btn_release_event(self, event):
        self.notallow_ok_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.hide_notallow_screen()
        self.show_menu_screen()

        self.auto_hide_notallow_screen_flag = False

    # ------------- Machine Screen Event -------------
    def get_machine_right_btn_press_event(self, event):
        self.machine_right_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_machine_right_btn_release_event(self, event):
        self.machine_right_btn.setStyleSheet(LOGO_BACK_STYLE)


        paramFile = ROOT_DIR + "/config.ini"
        config_params = configparser.ConfigParser()
        config_params.read(paramFile)
        
        ip_address = config_params.get("machine", "gsg-2-ip")
        vdai_pass = config_params.get("machine", "vdai-pass")
        
        try:
            statue_query = "https://vdai:" + vdai_pass + "@" + ip_address + "/api/unlock/status"
            res = requests.get(statue_query, verify=False)
            statue_txt = res.text
            
            temp = statue_txt.split(',')[0]
            statue_val = temp.split(':')[1].split('"')[1]

            if statue_val == '1':
                gene_query = "https://vdai:" + vdai_pass + "@" + ip_address + "/api/unlock/generate_pin"
                res = requests.get(gene_query, verify=False)
                pin_txt = res.text

                pin_val = pin_txt.split(':')[1].split('"')[1]

                if len(pin_val) < 4:
                    pin_val = '0' + pin_val

                self.machine_code.setText(pin_val)
                # print (pin_val)

            else:
                self.machine_code.setText("Machine is not Ready")
                # print("Machine is not Ready")
        except:
            print("Machine is not online")
    def get_machine_left_btn_press_event(self, event):
        self.machine_left_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_machine_left_btn_release_event(self, event):
        self.machine_left_btn.setStyleSheet(LOGO_BACK_STYLE)

        paramFile = ROOT_DIR + "/config.ini"
        config_params = configparser.ConfigParser()
        config_params.read(paramFile)
        
        ip_address = config_params.get("machine", "gsg-1-ip")
        vdai_pass = config_params.get("machine", "vdai-pass")
        
        try:
            statue_query = "https://vdai:" + vdai_pass + "@" + ip_address + "/api/unlock/status"
            res = requests.get(statue_query, verify=False)
            statue_txt = res.text
            
            print(statue_txt)
            
            temp = statue_txt.split(',')[0]
            statue_val = temp.split(':')[1].split('"')[1]

            if statue_val == '1':
                gene_query = "https://vdai:" + vdai_pass + "@" + ip_address + "/api/unlock/generate_pin"
                res = requests.get(gene_query, verify=False)
                pin_txt = res.text

                pin_val = pin_txt.split(':')[1].split('"')[1]

                if len(pin_val) < 4:
                    pin_val = '0' + pin_val

                self.machine_code.setText(pin_val)
                # print (pin_val)

            else:
                self.machine_code.setText("Machine is not Ready")
                # print("Machine is not Ready")

        except:
            print("Machine is not online")

    def get_machine_hilfe_btn_press_event(self, event):
        self.machine_hilfe_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_machine_hilfe_btn_release_event(self, event):
        self.machine_hilfe_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

    def get_machine_abbreuch_btn_press_event(self, event):
        self.machine_abbreuch_btn.setStyleSheet(BUTTON_PRESS_STYLE)

    def get_machine_abbreuch_btn_release_event(self, event):
        self.machine_abbreuch_btn.setStyleSheet(BUTTON_RELEASE_STYLE)

        self.auto_hide_machine_screen_flag = False

        self.active_machine_screen = False
        
        self.hide_machine_screen()
        self.show_menu_screen()


    # --------------------- keyboard screen event -----------------------
    def get_key_1_btn_press_event(self, event):
        self.key_1_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_1_btn_release_event(self, event):
        self.key_1_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '!'
            else:
                self.key_typed_string += '1'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '!'
                self.key_typed_string += '!'
            else:
                text = self.key_editline_value.text() + '1'
                self.key_typed_string += '1'
        self.key_editline_value.setText(text)

    def get_key_2_btn_press_event(self, event):
        self.key_2_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_2_btn_release_event(self, event):
        self.key_2_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '@'
            else:
                self.key_typed_string += '2'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '@'
                self.key_typed_string += '@'
            else:
                text = self.key_editline_value.text() + '2'
                self.key_typed_string += '2'
        self.key_editline_value.setText(text)

    def get_key_3_btn_press_event(self, event):
        self.key_3_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_3_btn_release_event(self, event):
        self.key_3_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '#'
            else:
                self.key_typed_string += '3'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '#'
                self.key_typed_string += '#'
            else:
                text = self.key_editline_value.text() + '3'
                self.key_typed_string += '3'
        self.key_editline_value.setText(text)

    def get_key_4_btn_press_event(self, event):
        self.key_4_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_4_btn_release_event(self, event):
        self.key_4_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '$'
            else:
                self.key_typed_string += '4'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '$'
                self.key_typed_string += '$'
            else:
                text = self.key_editline_value.text() + '4'
                self.key_typed_string += '4'
        self.key_editline_value.setText(text)

    def get_key_5_btn_press_event(self, event):
        self.key_5_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_5_btn_release_event(self, event):
        self.key_5_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '%'
            else:
                self.key_typed_string += '5'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '%'
                self.key_typed_string += '%'
            else:
                text = self.key_editline_value.text() + '5'
                self.key_typed_string += '5'
        self.key_editline_value.setText(text)

    def get_key_6_btn_press_event(self, event):
        self.key_6_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_6_btn_release_event(self, event):
        self.key_6_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '^'
            else:
                self.key_typed_string += '6'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '^'
                self.key_typed_string += '^'
            else:
                text = self.key_editline_value.text() + '6'
                self.key_typed_string += '6'
        self.key_editline_value.setText(text)

    def get_key_7_btn_press_event(self, event):
        self.key_7_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_7_btn_release_event(self, event):
        self.key_7_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '&'
            else:
                self.key_typed_string += '7'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '&'
                self.key_typed_string += '&'
            else:
                text = self.key_editline_value.text() + '7'
                self.key_typed_string += '7'
        self.key_editline_value.setText(text)

    def get_key_8_btn_press_event(self, event):
        self.key_8_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_8_btn_release_event(self, event):
        self.key_8_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '*'
            else:
                self.key_typed_string += '8'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '*'
                self.key_typed_string += '*'
            else:
                text = self.key_editline_value.text() + '8'
                self.key_typed_string += '8'
        self.key_editline_value.setText(text)

    def get_key_9_btn_press_event(self, event):
        self.key_9_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_9_btn_release_event(self, event):
        self.key_9_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '('
            else:
                self.key_typed_string += '9'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '('
                self.key_typed_string += '('
            else:
                text = self.key_editline_value.text() + '9'
                self.key_typed_string += '9'
        self.key_editline_value.setText(text)

    def get_key_0_btn_press_event(self, event):
        self.key_0_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_0_btn_release_event(self, event):
        self.key_0_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += ')'
            else:
                self.key_typed_string += '0'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + ')'
                self.key_typed_string += ')'
            else:
                text = self.key_editline_value.text() + '0'
                self.key_typed_string += '0'
        self.key_editline_value.setText(text)

    def get_key_underline_btn_press_event(self, event):
        self.key_underline_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_underline_btn_release_event(self, event):
        self.key_underline_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '_'
            else:
                self.key_typed_string += '-'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '_'
                self.key_typed_string += '_'
            else:
                text = self.key_editline_value.text() + '-'
                self.key_typed_string += '-'
        self.key_editline_value.setText(text)

    def get_key_plus_btn_press_event(self, event):
        self.key_plus_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_plus_btn_release_event(self, event):
        self.key_plus_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '+'
            else:
                self.key_typed_string += '='
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '+'
                self.key_typed_string += '+'
            else:
                text = self.key_editline_value.text() + '='
                self.key_typed_string += '='
        self.key_editline_value.setText(text)

    def get_key_backspace_btn_press_event(self, event):
        self.key_backspace_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_backspace_btn_release_event(self, event):
        self.key_backspace_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        text = self.key_editline_value.text()
        if len(text) > 0:
            self.key_editline_value.setText(text[:-1])
            self.key_typed_string = self.key_typed_string[:-1]
        else:
            self.key_editline_value.setText(text)

    def get_key_q_btn_press_event(self, event):
        self.key_q_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_q_btn_release_event(self, event):
        self.key_q_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'Q'
            else:
                self.key_typed_string += 'q'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'Q'
                self.key_typed_string += 'Q'
            else:
                text = self.key_editline_value.text() + 'q'
                self.key_typed_string += 'q'
        self.key_editline_value.setText(text)

    def get_key_w_btn_press_event(self, event):
        self.key_w_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_w_btn_release_event(self, event):
        self.key_w_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'W'
            else:
                self.key_typed_string += 'w'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'W'
                self.key_typed_string += 'W'
            else:
                text = self.key_editline_value.text() + 'w'
                self.key_typed_string += 'w'
        self.key_editline_value.setText(text)

    def get_key_e_btn_press_event(self, event):
        self.key_e_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_e_btn_release_event(self, event):
        self.key_e_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'E'
            else:
                self.key_typed_string += 'e'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'E'
                self.key_typed_string += 'E'
            else:
                text = self.key_editline_value.text() + 'e'
                self.key_typed_string += 'e'
        self.key_editline_value.setText(text)

    def get_key_r_btn_press_event(self, event):
        self.key_r_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_r_btn_release_event(self, event):
        self.key_r_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'R'
            else:
                self.key_typed_string += 'r'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'R'
                self.key_typed_string += 'R'
            else:
                text = self.key_editline_value.text() + 'r'
                self.key_typed_string += 'r'
        self.key_editline_value.setText(text)

    def get_key_t_btn_press_event(self, event):
        self.key_t_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_t_btn_release_event(self, event):
        self.key_t_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'T'
            else:
                self.key_typed_string += 't'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'T'
                self.key_typed_string += 'T'
            else:
                text = self.key_editline_value.text() + 't'
                self.key_typed_string += 't'
        self.key_editline_value.setText(text)

    def get_key_y_btn_press_event(self, event):
        self.key_y_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_y_btn_release_event(self, event):
        self.key_y_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'Y'
            else:
                self.key_typed_string += 'y'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'Y'
                self.key_typed_string += 'Y'
            else:
                text = self.key_editline_value.text() + 'y'
                self.key_typed_string += 'y'
        self.key_editline_value.setText(text)

    def get_key_u_btn_press_event(self, event):
        self.key_u_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_u_btn_release_event(self, event):
        self.key_u_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'U'
            else:
                self.key_typed_string += 'u'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'U'
                self.key_typed_string += 'U'
            else:
                text = self.key_editline_value.text() + 'u'
                self.key_typed_string += 'u'
        self.key_editline_value.setText(text)

    def get_key_i_btn_press_event(self, event):
        self.key_i_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_i_btn_release_event(self, event):
        self.key_i_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'I'
            else:
                self.key_typed_string += 'i'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'I'
                self.key_typed_string += 'I'
            else:
                text = self.key_editline_value.text() + 'i'
                self.key_typed_string += 'i'
        self.key_editline_value.setText(text)

    def get_key_o_btn_press_event(self, event):
        self.key_o_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_o_btn_release_event(self, event):
        self.key_o_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'A'
            else:
                self.key_typed_string += 'a'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'A'
                self.key_typed_string += 'A'
            else:
                text = self.key_editline_value.text() + 'a'
                self.key_typed_string += 'a'
        self.key_editline_value.setText(text)

    def get_key_p_btn_press_event(self, event):
        self.key_p_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_p_btn_release_event(self, event):
        self.key_p_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'P'
            else:
                self.key_typed_string += 'p'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'P'
                self.key_typed_string += 'P'
            else:
                text = self.key_editline_value.text() + 'p'
                self.key_typed_string += 'p'
        self.key_editline_value.setText(text)

    def get_key_PT1_btn_press_event(self, event):
        self.key_PT1_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT1_btn_release_event(self, event):
        self.key_PT1_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '{'
            else:
                self.key_typed_string += '['
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '{'
                self.key_typed_string += '{'
            else:
                text = self.key_editline_value.text() + '['
                self.key_typed_string += '['
        self.key_editline_value.setText(text)

    def get_key_PT2_btn_press_event(self, event):
        self.key_PT2_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT2_btn_release_event(self, event):
        self.key_PT2_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '}'
            else:
                self.key_typed_string += ']'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '}'
                self.key_typed_string += '}'
            else:
                text = self.key_editline_value.text() + ']'
                self.key_typed_string += ']'
        self.key_editline_value.setText(text)

    def get_key_PT3_btn_press_event(self, event):
        self.key_PT3_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT3_btn_release_event(self, event):
        self.key_PT3_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '|'
            else:
                self.key_typed_string += '\\'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '|'
                self.key_typed_string += '|'
            else:
                text = self.key_editline_value.text() + '\\'
                self.key_typed_string += '\\'
        self.key_editline_value.setText(text)

    def get_key_a_btn_press_event(self, event):
        self.key_a_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_a_btn_release_event(self, event):
        self.key_a_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'A'
            else:
                self.key_typed_string += 'a'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'A'
                self.key_typed_string += 'A'
            else:
                text = self.key_editline_value.text() + 'a'
                self.key_typed_string += 'a'
        self.key_editline_value.setText(text)

    def get_key_s_btn_press_event(self, event):
        self.key_s_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_s_btn_release_event(self, event):
        self.key_s_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'S'
            else:
                self.key_typed_string += 's'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'S'
                self.key_typed_string += 'S'
            else:
                text = self.key_editline_value.text() + 's'
                self.key_typed_string += 's'
        self.key_editline_value.setText(text)

    def get_key_d_btn_press_event(self, event):
        self.key_d_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_d_btn_release_event(self, event):
        self.key_d_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'D'
            else:
                self.key_typed_string += 'd'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'D'
                self.key_typed_string += 'D'
            else:
                text = self.key_editline_value.text() + 'd'
                self.key_typed_string += 'd'
        self.key_editline_value.setText(text)

    def get_key_f_btn_press_event(self, event):
        self.key_f_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_f_btn_release_event(self, event):
        self.key_f_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'F'
            else:
                self.key_typed_string += 'f'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'F'
                self.key_typed_string += 'F'
            else:
                text = self.key_editline_value.text() + 'f'
                self.key_typed_string += 'f'
        self.key_editline_value.setText(text)

    def get_key_g_btn_press_event(self, event):
        self.key_g_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_g_btn_release_event(self, event):
        self.key_g_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'G'
            else:
                self.key_typed_string += 'g'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'G'
                self.key_typed_string += 'G'
            else:
                text = self.key_editline_value.text() + 'g'
                self.key_typed_string += 'g'
        self.key_editline_value.setText(text)

    def get_key_h_btn_press_event(self, event):
        self.key_h_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_h_btn_release_event(self, event):
        self.key_h_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'H'
            else:
                self.key_typed_string += 'h'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'H'
                self.key_typed_string += 'H'
            else:
                text = self.key_editline_value.text() + 'h'
                self.key_typed_string += 'h'
        self.key_editline_value.setText(text)

    def get_key_j_btn_press_event(self, event):
        self.key_j_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_j_btn_release_event(self, event):
        self.key_j_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'J'
            else:
                self.key_typed_string += 'j'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'J'
                self.key_typed_string += 'J'
            else:
                text = self.key_editline_value.text() + 'j'
                self.key_typed_string += 'j'
        self.key_editline_value.setText(text)

    def get_key_k_btn_press_event(self, event):
        self.key_k_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_k_btn_release_event(self, event):
        self.key_k_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'K'
            else:
                self.key_typed_string += 'k'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'K'
                self.key_typed_string += 'K'
            else:
                text = self.key_editline_value.text() + 'k'
                self.key_typed_string += 'k'
        self.key_editline_value.setText(text)

    def get_key_l_btn_press_event(self, event):
        self.key_l_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_l_btn_release_event(self, event):
        self.key_l_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'L'
            else:
                self.key_typed_string += 'l'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'L'
                self.key_typed_string += 'L'
            else:
                text = self.key_editline_value.text() + 'l'
                self.key_typed_string += 'l'
        self.key_editline_value.setText(text)

    def get_key_PT4_btn_press_event(self, event):
        self.key_PT4_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT4_btn_release_event(self, event):
        self.key_PT4_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += ':'
            else:
                self.key_typed_string += ';'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + ':'
                self.key_typed_string += ':'
            else:
                text = self.key_editline_value.text() + ';'
                self.key_typed_string += ';'
        self.key_editline_value.setText(text)

    def get_key_PT5_btn_press_event(self, event):
        self.key_PT5_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT5_btn_release_event(self, event):
        self.key_PT5_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '"'
            else:
                self.key_typed_string += "'"
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '"'
                self.key_typed_string += '"'
            else:
                text = self.key_editline_value.text() + "'"
                self.key_typed_string += "'"
        self.key_editline_value.setText(text)

    def get_key_enter_btn_press_event(self, event):
        self.key_enter_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_enter_btn_release_event(self, event):
        self.key_enter_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        # ------- admin login ----------------------
        if self.edit_admin_id_flag:
            self.login_id_value.setText(self.key_editline_value.text())
            self.admin_id_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_admin_id_flag = False

        if self.edit_admin_password_flag:
            self.login_password_value.setText(self.key_editline_value.text())
            self.admin_password_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_admin_password_flag = False

        # --------- Oasis certification ------------
        if self.edit_cert_url_flag:
            self.cert_url_value.setText(self.key_editline_value.text())
            self.cert_url_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_url_flag = False

        if self.edit_cert_user_flag:
            self.cert_user_value.setText(self.key_editline_value.text())
            self.cert_user_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_user_flag = False

        if self.edit_cert_userpass_flag:
            self.cert_userpass_value.setText(self.key_editline_value.text())
            self.cert_userpass_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_userpass_flag = False

        if self.edit_cert_pass_flag:
            self.cert_pass_value.setText(self.key_editline_value.text())
            self.cert_pass_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_cert_pass_flag = False

        # -------- admin setting -----------------
        if self.edit_adminsetting_user_flag:
            self.admin_user_value.setText(self.key_editline_value.text())
            self.adminsetting_user_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_adminsetting_user_flag = False

        if self.edit_adminsetting_password_flag:
            self.admin_pass_value.setText(self.key_editline_value.text())
            self.adminsetting_password_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_adminsetting_password_flag = False

        # ----------- WiFi setting -------------
        if self.edit_wifisetting_wlan_flag:
            self.wifi_wlan_value.setText(self.key_editline_value.text())
            self.wifisetting_wlan_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_wifisetting_wlan_flag = False

        if self.edit_wifisetting_essid_flag:
            self.wifi_essid_value.setText(self.key_editline_value.text())
            self.wifisetting_essid_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_wifisetting_essid_flag = False

        if self.edit_wifisetting_password_flag:
            self.wifi_pass_value.setText(self.key_editline_value.text())
            self.wifisetting_password_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_wifisetting_password_flag = False

        # ------------ Machine setting ----------
        if self.edit_machine_1_ip_flag:
            self.machinesetting_1_ip_value.setText(self.key_editline_value.text())
            self.machine_1_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_1_ip_flag = False

        if self.edit_machine_2_ip_flag:
            self.machinesetting_2_ip_value.setText(self.key_editline_value.text())
            self.machine_2_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_2_ip_flag = False

        if self.edit_machine_3_ip_flag:
            self.machinesetting_3_ip_value.setText(self.key_editline_value.text())
            self.machine_3_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_3_ip_flag = False

        if self.edit_machine_4_ip_flag:
            self.machinesetting_4_ip_value.setText(self.key_editline_value.text())
            self.machine_4_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_4_ip_flag = False

        if self.edit_machine_5_ip_flag:
            self.machinesetting_5_ip_value.setText(self.key_editline_value.text())
            self.machine_5_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_5_ip_flag = False

        if self.edit_machine_6_ip_flag:
            self.machinesetting_6_ip_value.setText(self.key_editline_value.text())
            self.machine_6_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_6_ip_flag = False

        if self.edit_machine_7_ip_flag:
            self.machinesetting_7_ip_value.setText(self.key_editline_value.text())
            self.machine_7_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_7_ip_flag = False

        if self.edit_machine_8_ip_flag:
            self.machinesetting_8_ip_value.setText(self.key_editline_value.text())
            self.machine_8_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_8_ip_flag = False

        if self.edit_machine_9_ip_flag:
            self.machinesetting_9_ip_value.setText(self.key_editline_value.text())
            self.machine_9_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_9_ip_flag = False

        if self.edit_machine_10_ip_flag:
            self.machinesetting_10_ip_value.setText(self.key_editline_value.text())
            self.machine_10_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_10_ip_flag = False

        if self.edit_machine_11_ip_flag:
            self.machinesetting_11_ip_value.setText(self.key_editline_value.text())
            self.machine_11_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_11_ip_flag = False

        if self.edit_machine_12_ip_flag:
            self.machinesetting_12_ip_value.setText(self.key_editline_value.text())
            self.machine_12_ip_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_12_ip_flag = False

        if self.edit_machine_pass_flag:
            self.machinesetting_pass_value.setText(self.key_editline_value.text())
            self.machine_pass_value_string = self.key_typed_string
            self.key_typed_string = ''
            self.edit_machine_pass_flag = False
        # ------ edit db manager info --------
        if self.edit_db_lastname_flag:
            self.db_lastname_value.setText(self.key_editline_value.text())
            self.key_typed_string = ''
            self.edit_db_lastname_flag = False

        if self.edit_db_birth_flag:
            self.db_birth_value.setText(self.key_editline_value.text())
            self.key_typed_string = ''
            self.edit_db_birth_flag = False
        # ---------- edit main info -----------
        if self.edit_name_flag:
            self.main_name_value.setText(self.key_editline_value.text())
            name = self.key_typed_string
            self.key_typed_string = ''
            try:
                self.card_firstname = name.split(' ')[0]
                self.card_lastname = name.split(' ')[1]
            except:
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(14)

                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Please Type Full name like format : Firstname LastName")
                msg.setWindowTitle("Invalid Name")
                msg.setFont(font)
                msg.exec_()

            self.check_info()

            self.edit_name_flag = False

        if self.edit_birth_flag:
            self.main_birth_value.setText(self.key_editline_value.text())
            self.card_birth = self.key_typed_string
            self.key_typed_string = ''

            try:
                self.card_age = self.calc_age(self.card_birth)
                if self.card_age > 18:
                    self.card_statue = 'Allow'
                else:
                    self.card_statue = 'Not Allow'

                self.main_age_value.setText(str(self.card_age))
                self.main_status_value.setText(self.card_statue)

            except:
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(14)

                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Please Type Birthday like format : DD.MM.YYYY")
                msg.setWindowTitle("Invalid Birthday")
                msg.setFont(font)
                msg.exec_()

            self.check_info()

            self.edit_birth_flag = False

        self.key_editline_value.clear()
        self.hide_keyboard_screen()

    def calc_age(self, birth_str):
        b_year = int(birth_str.split('.')[2])
        b_month = int(birth_str.split('.')[1].replace('0', ''))
        b_day = int(birth_str.split('.')[0].replace('0', ''))
        birth_date = date(b_year, b_month, b_day)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def check_info(self):
        if len(self.card_firstname) > 2 \
                and len(self.card_lastname) > 2 \
                and len(self.card_birth) > 2 \
                and self.card_statue == 'Allow':

            self.active_gov_request = True

    def get_key_z_btn_press_event(self, event):
        self.key_z_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_z_btn_release_event(self, event):
        self.key_z_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'Z'
            else:
                self.key_typed_string += 'z'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'Z'
                self.key_typed_string += 'Z'
            else:
                text = self.key_editline_value.text() + 'z'
                self.key_typed_string += 'z'
        self.key_editline_value.setText(text)

    def get_key_x_btn_press_event(self, event):
        self.key_x_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_x_btn_release_event(self, event):
        self.key_x_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'X'
            else:
                self.key_typed_string += 'x'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'X'
                self.key_typed_string += 'X'
            else:
                text = self.key_editline_value.text() + 'x'
                self.key_typed_string += 'x'
        self.key_editline_value.setText(text)

    def get_key_c_btn_press_event(self, event):
        self.key_c_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_c_btn_release_event(self, event):
        self.key_c_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'C'
            else:
                self.key_typed_string += 'c'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'C'
                self.key_typed_string += 'C'
            else:
                text = self.key_editline_value.text() + 'c'
                self.key_typed_string += 'c'
        self.key_editline_value.setText(text)

    def get_key_v_btn_press_event(self, event):
        self.key_v_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_v_btn_release_event(self, event):
        self.key_v_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'V'
            else:
                self.key_typed_string += 'v'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'V'
                self.key_typed_string += 'V'
            else:
                text = self.key_editline_value.text() + 'v'
                self.key_typed_string += 'v'
        self.key_editline_value.setText(text)

    def get_key_b_btn_press_event(self, event):
        self.key_b_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_b_btn_release_event(self, event):
        self.key_b_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'B'
            else:
                self.key_typed_string += 'b'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'B'
                self.key_typed_string += 'B'
            else:
                text = self.key_editline_value.text() + 'b'
                self.key_typed_string += 'b'
        self.key_editline_value.setText(text)

    def get_key_n_btn_press_event(self, event):
        self.key_n_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_n_btn_release_event(self, event):
        self.key_n_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'N'
            else:
                self.key_typed_string += 'n'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'N'
                self.key_typed_string += 'N'
            else:
                text = self.key_editline_value.text() + 'n'
                self.key_typed_string += 'n'
        self.key_editline_value.setText(text)

    def get_key_m_btn_press_event(self, event):
        self.key_m_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_m_btn_release_event(self, event):
        self.key_m_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += 'M'
            else:
                self.key_typed_string += 'm'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + 'M'
                self.key_typed_string += 'M'
            else:
                text = self.key_editline_value.text() + 'm'
                self.key_typed_string += 'm'
        self.key_editline_value.setText(text)

    def get_key_PT6_btn_press_event(self, event):
        self.key_PT6_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT6_btn_release_event(self, event):
        self.key_PT6_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '<'
            else:
                self.key_typed_string += ','
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '<'
                self.key_typed_string += '<'
            else:
                text = self.key_editline_value.text() + ','
                self.key_typed_string += ','
        self.key_editline_value.setText(text)

    def get_key_PT7_btn_press_event(self, event):
        self.key_PT7_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT7_btn_release_event(self, event):
        self.key_PT7_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '>'
            else:
                self.key_typed_string += '.'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '>'
                self.key_typed_string += '>'
            else:
                text = self.key_editline_value.text() + '.'
                self.key_typed_string += '.'
        self.key_editline_value.setText(text)

    def get_key_PT8_btn_press_event(self, event):
        self.key_PT8_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_PT8_btn_release_event(self, event):
        self.key_PT8_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            if self.key_shift_pressed_flag:
                self.key_typed_string += '?'
            else:
                self.key_typed_string += '/'
        else:
            if self.key_shift_pressed_flag:
                text = self.key_editline_value.text() + '?'
                self.key_typed_string += '?'
            else:
                text = self.key_editline_value.text() + '/'
                self.key_typed_string += '/'
        self.key_editline_value.setText(text)

    def get_key_shift_btn_press_event(self, event):
        self.key_shift_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_shift_btn_release_event(self, event):
        self.key_shift_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        self.key_shift_pressed_flag = not self.key_shift_pressed_flag

        if self.key_shift_pressed_flag:
            self.key_shift_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

        else:
            self.key_shift_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

    def get_key_space_btn_press_event(self, event):
        self.key_space_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_space_btn_release_event(self, event):
        self.key_space_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        if self.edit_admin_password_flag:
            text = self.key_editline_value.text() + '*'
            self.key_typed_string += ' '
        else:
            text = self.key_editline_value.text() + ' '
            self.key_typed_string += ' '

        self.key_editline_value.setText(text)

    def get_key_tab_btn_press_event(self, event):
        self.key_tab_btn.setStyleSheet(KEY_BUTTON_PRESS_STYLE)

    def get_key_tab_btn_release_event(self, event):
        self.key_tab_btn.setStyleSheet(KEY_BUTTON_RELEASE_STYLE)

        text = self.key_editline_value.text() + ' ' * 4
        self.key_typed_string += ' ' * 4
        self.key_editline_value.setText(text)

    ##############################################


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    X_rate = size.width() / 768
    Y_rate = size.height() / 1024

    # X_rate = 1
    # Y_rate = 1

    print('Size: %d x %d' % (size.width(), size.height()))
    window = AdminWindow(X_rate, Y_rate)

    window.show()
    sys.exit(app.exec_())

