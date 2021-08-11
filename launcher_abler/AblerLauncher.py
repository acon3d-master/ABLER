"""
    Copyright 2016-2019 Tobias Kummer/Overmind Studios.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import configparser
import json
import logging
import os
import os.path
import platform
import shutil
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime
from distutils.dir_util import copy_tree
from distutils.version import StrictVersion

import requests

import mainwindow
import qdarkstyle

from PySide2 import QtWidgets, QtCore, QtGui

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

app = QtWidgets.QApplication(sys.argv)

app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

appversion = "1.9.8"
dir_ = "C:/Program Files (x86)/ABLER"
launcherdir_ = os.getenv('APPDATA') + "\\Blender Foundation\\Blender\\2.93\\updater"
config = configparser.ConfigParser()
btn = {}
lastversion = ""
installedversion = ""
launcher_installed = ""
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename="AblerLauncher.log", format=LOG_FORMAT, level=logging.DEBUG, filemode="w"
)

logger = logging.getLogger()


class WorkerThread(QtCore.QThread):
    """Does all the actual work in the background, informs GUI about status"""

    update = QtCore.Signal(int)
    finishedDL = QtCore.Signal()
    finishedEX = QtCore.Signal()
    finishedCP = QtCore.Signal()
    finishedCL = QtCore.Signal()

    def __init__(self, url, file):
        super(WorkerThread, self).__init__(parent=app)
        self.filename = file
        self.url = url
        if "macOS" in file:
            config.set("main", "lastdl", "OSX")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()
        elif "win32" in file:
            config.set("main", "lastdl", "Windows 32bit")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()
        elif "win64" in file:
            config.set("main", "lastdl", "Windows 64bit")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()
        elif "glibc211-i686" in file:
            config.set("main", "lastdl", "Linux glibc211 i686")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()
        elif "glibc211-x86_64" in file:
            config.set("main", "lastdl", "Linux glibc211 x86_64")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()
        elif "glibc219-i686" in file:
            config.set("main", "lastdl", "Linux glibc219 i686")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()
        elif "glibc219-x86_64" in file:
            config.set("main", "lastdl", "Linux glibc219 x86_64")
            with open("config.ini", "w") as f:
                config.write(f)
                f.close()

    def progress(self, count, blockSize, totalSize):
        """Updates progress bar"""
        percent = int(count * blockSize * 100 / totalSize)
        self.update.emit(percent)

    def run(self):
        urllib.request.urlretrieve(self.url, self.filename, reporthook=self.progress)
        self.finishedDL.emit()
        shutil.unpack_archive(self.filename, "./blendertemp/")
        self.finishedEX.emit()
        source = next(os.walk("./blendertemp/"))[1]
        copy_tree(os.path.join("./blendertemp/", source[0]), dir_)
        self.finishedCP.emit()
        shutil.rmtree("./blendertemp")
        self.finishedCL.emit()


class BlenderUpdater(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        logger.info(f"Running version {appversion}")
        logger.debug("Constructing UI")
        super(BlenderUpdater, self).__init__(parent)
        self.setupUi(self)
        self.btn_oneclick.hide()
        self.lbl_quick.hide()
        self.lbl_caution.hide()
        self.btn_newVersion.hide()
        self.btn_update.hide()
        self.btn_execute.hide()
        self.lbl_caution.setStyleSheet("background: rgb(255, 155, 8);\n" "color: white")
        global lastversion
        global dir_
        global config
        global installedversion
        global launcher_installed
        if os.path.isfile("./config.ini"):
            config_exist = True
            logger.info("Reading existing configuration file")
            config.read("config.ini")
            lastcheck = config.get("main", "lastcheck")
            lastversion = config.get("main", "lastdl")
            installedversion = config.get("main", "installed")
            launcher_installed = config.get("main", "launcher")
            flavor = config.get("main", "flavor")
            if lastversion != "":
                self.btn_oneclick.setText(f"{flavor} | {lastversion}")
            else:
                pass

        else:
            logger.debug("No previous config found")
            self.btn_oneclick.hide()
            config_exist = False
            config.read("config.ini")
            config.add_section("main")
            config.set("main", "path", "")
            lastcheck = "Never"
            config.set("main", "lastcheck", lastcheck)
            config.set("main", "lastdl", "")
            config.set("main", "installed", "")
            config.set("main", "launcher", "")
            config.set("main", "flavor", "")
            with open("config.ini", "w") as f:
                config.write(f)
        self.btn_cancel.hide()
        self.frm_progress.hide()
        self.btngrp_filter.hide()
        self.btn_acon.setFocus()
        self.lbl_available.hide()
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.lbl_task.hide()
        self.statusbar.showMessage(f"Ready - Last check: {lastcheck}")
        self.btn_Quit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.btn_about.clicked.connect(self.about)
        self.btn_acon.clicked.connect(self.open_acon3d)

        if not(self.check_launcher()):
            self.check_once()



    def open_acon3d(self):
        url = QtCore.QUrl("https://www.acon3d.com/")
        QtGui.QDesktopServices.openUrl(url)

    def about(self):
        aboutText = (
            '<html><head/><body><p>Utility to update ABLER to the latest version available at<br> \
        <a href="https://builder.blender.org/download/"><span style=" text-decoration: underline; color:#2980b9;">\
        https://builder.blender.org/download/</span></a></p><p><br/>Developed by Tobias Kummer for \
        <a href="http://www.overmind-studios.de"><span style="text-decoration:underline; color:#2980b9;"> \
        Overmind Studios</span></a></p><p>\
        Licensed under the <a href="https://www.gnu.org/licenses/gpl-3.0-standalone.html"><span style=" text-decoration:\
        underline; color:#2980b9;">GPL v3 license</span></a></p><p>Project home: \
        <a href="https://overmindstudios.github.io/BlenderUpdater/"><span style=" text-decoration:\
        underline; color:#2980b9;">https://overmindstudios.github.io/BlenderUpdater/</a></p> \
        <p style="text-align: center;"></p> \
        <p>Application based on the version: '
            + launcher_installed
            + "</p></body></html> "
        )
        QtWidgets.QMessageBox.about(self, "About", aboutText)


    def hbytes(self, num):
        """Translate to human readable file size."""
        for x in [" bytes", " KB", " MB", " GB"]:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, " TB")


    def check_once(self):
        global dir_
        global lastversion
        global installedversion
        url = "https://api.github.com/repos/acon3d/ABLER/releases/latest"
        # Do path settings save here, in case user has manually edited it
        global config
        config.read("config.ini")
        config.set("main", "path", dir_)
        with open("config.ini", "w") as f:
            config.write(f)
        f.close()
        try:
            req = requests.get(url)
        except Exception:
            self.statusBar().showMessage(
                "Error reaching server - check your internet connection"
            )
            logger.error("No connection to Blender nightly builds server")
            self.frm_start.show()
        results = []

        version_tag = req.json()['name'][1:]
        for asset in req.json()['assets']:
            opsys = platform.system()
            if opsys == "Windows":
                if "Windows" in asset['browser_download_url'] and "zip" in asset['browser_download_url']:
                    info = {}
                    info["url"] = asset['browser_download_url']
                    info["os"] = "Windows"
                    info["filename"] = asset['browser_download_url'].split("/")[-1]
                    info["version"] = version_tag
                    info["arch"] = "x64"
                    results.append(info)
            if opsys.lower == "darwin":
                self.btn_execute.clicked.connect(self.exec_osx)
            if opsys == "Linux":
                self.btn_execute.clicked.connect(self.exec_linux)
        finallist = results
        if len(finallist) != 0:
            if StrictVersion(finallist[0]["version"]) > StrictVersion(installedversion):
                self.btn_update.show()
                self.btn_update.clicked.connect(
                    lambda throwaway=0, entry=finallist[0]: self.download(entry)
                )
                self.btn_execute.hide()
                self.btn_update_launcher.hide()
            else:
                self.btn_update.hide()
                self.btn_update_launcher.hide()
                self.btn_execute.show()
                opsys = platform.system()
                if opsys == "Windows":
                    self.btn_execute.clicked.connect(self.exec_windows)
                if opsys.lower == "darwin":
                    self.btn_execute.clicked.connect(self.exec_osx)
                if opsys == "Linux":
                    self.btn_execute.clicked.connect(self.exec_linux)
        else:
            self.btn_update.hide()
            self.btn_update_launcher.hide()
            self.btn_execute.show()
            opsys = platform.system()
            if opsys == "Windows":
                self.btn_execute.clicked.connect(self.exec_windows)
            if opsys.lower == "darwin":
                self.btn_execute.clicked.connect(self.exec_osx)
            if opsys == "Linux":
                self.btn_execute.clicked.connect(self.exec_linux)

    def check_launcher(self):
        launcher_need_install = False
        global dir_
        global lastversion
        global installedversion
        global launcher_installed
        global launcherdir_
        url = "https://api.github.com/repos/acon3d/ABLER/releases/latest"
        # Do path settings save here, in case user has manually edited it
        global config
        config.read("config.ini")
        launcher_installed = config.get("main", "launcher")
        config.set("main", "path", dir_)
        with open("config.ini", "w") as f:
            config.write(f)
        f.close()
        try:
            req = requests.get(url)
        except Exception:
            self.statusBar().showMessage(
                "Error reaching server - check your internet connection"
            )
            logger.error("No connection to Blender nightly builds server")
            self.frm_start.show()
        results = []

        for asset in req.json()['assets']:
            opsys = platform.system()
            if opsys == "Windows":
                target = asset['browser_download_url']
                if "Windows" in target and "launcher" in target and "zip" in target:
                    info = {}
                    info["url"] = asset['browser_download_url']
                    info["os"] = "Windows"
                    info["filename"] = asset['browser_download_url'].split("/")[-1]
                    #file name should be "ABLER Launcher v0.0.2.zip"
                    info["version"] = info["filename"].split(' ')[-1][1:-4]
                    info["arch"] = "x64"
                    results.append(info)
            if opsys.lower == "darwin":
                self.btn_execute.clicked.connect(self.exec_osx)
            if opsys == "Linux":
                self.btn_execute.clicked.connect(self.exec_linux)
        finallist = results
        if len(finallist) != 0:
            if StrictVersion(finallist[0]["version"]) > StrictVersion(launcher_installed):
                self.btn_execute.hide()
                self.btn_update.hide()
                self.btn_update_launcher.show()
                self.btn_update_launcher.clicked.connect(
                    lambda throwaway=0, entry=finallist[0]: self.download_launcher(entry)
                )
                launcher_need_install = True
        else:
            self.btn_update_launcher.hide()
        return launcher_need_install


    def download(self, entry):
        """Download routines."""
        global dir_

        url = entry["url"]
        version = entry["version"]
        variation = entry["arch"]

        if os.path.isdir("./blendertemp"):
            shutil.rmtree("./blendertemp")

        os.makedirs("./blendertemp")
        file = urllib.request.urlopen(url)
        totalsize = file.info()["Content-Length"]
        size_readable = self.hbytes(float(totalsize))

        global config
        config.read("config.ini")
        config.set("main", "path", dir_)
        config.set("main", "flavor", variation)
        config.set("main", "installed", version)

        with open("config.ini", "w") as f:
            config.write(f)
        f.close()

        ##########################
        # Do the actual download #
        ##########################

        dir_ = os.path.join(dir_, "")
        filename = "./blendertemp/" + entry["filename"]

        for i in btn:
            btn[i].hide()
        logger.info(f"Starting download thread for {url}{version}")

        self.lbl_available.hide()
        self.lbl_caution.hide()
        self.progressBar.show()
        self.btngrp_filter.hide()
        self.lbl_task.setText("Downloading")
        self.lbl_task.show()
        self.frm_progress.show()
        nowpixmap = QtGui.QPixmap(":/newPrefix/images/Actions-arrow-right-icon.png")
        self.lbl_download_pic.setPixmap(nowpixmap)
        self.lbl_downloading.setText(f"<b>Downloading {version}</b>")
        self.progressBar.setValue(0)
        self.statusbar.showMessage(f"Downloading {size_readable}")

        thread = WorkerThread(url, filename)
        thread.update.connect(self.updatepb)
        thread.finishedDL.connect(self.extraction)
        thread.finishedEX.connect(self.finalcopy)
        thread.finishedCP.connect(self.cleanup)
        thread.finishedCL.connect(self.done)
        thread.start()


    def download_launcher(self, entry):
        """Download routines."""
        global launcherdir_

        url = entry["url"]
        version = entry["version"]
        variation = entry["arch"]

        if os.path.isdir("./launchertemp"):
            shutil.rmtree("./launchertemp")

        os.makedirs("./launchertemp")
        file = urllib.request.urlopen(url)
        totalsize = file.info()["Content-Length"]
        size_readable = self.hbytes(float(totalsize))

        global config
        config.read("config.ini")
        config.set("main", "launcher", version)

        with open("config.ini", "w") as f:
            config.write(f)
        f.close()

        ##########################
        # Do the actual download #
        ##########################

        launcherdir_ = os.path.join(launcherdir_, "")
        filename = "./launchertemp/" + entry["filename"]

        logger.info(f"Starting download thread for {url}{version}")

        self.lbl_available.hide()
        self.lbl_caution.hide()
        self.progressBar.show()
        self.btngrp_filter.hide()
        self.lbl_task.setText("Downloading")
        self.lbl_task.show()
        self.frm_progress.show()
        nowpixmap = QtGui.QPixmap(":/newPrefix/images/Actions-arrow-right-icon.png")
        self.lbl_download_pic.setPixmap(nowpixmap)
        self.lbl_downloading.setText(f"<b>Downloading Launcher {version}</b>")
        self.progressBar.setValue(0)
        self.statusbar.showMessage(f"Downloading {size_readable}")

        thread = WorkerThread(url, filename)
        thread.update.connect(self.updatepb)
        thread.finishedDL.connect(self.extraction)
        thread.finishedEX.connect(self.finalcopy)
        thread.finishedCP.connect(self.cleanup)
        thread.finishedCL.connect(self.done_launcher)
        thread.start()

    def updatepb(self, percent):
        self.progressBar.setValue(percent)

    def extraction(self):
        logger.info("Extracting to temp directory")
        self.lbl_task.setText("Extracting...")
        self.btn_Quit.setEnabled(False)
        nowpixmap = QtGui.QPixmap(":/newPrefix/images/Actions-arrow-right-icon.png")
        donepixmap = QtGui.QPixmap(":/newPrefix/images/Check-icon.png")
        self.lbl_download_pic.setPixmap(donepixmap)
        self.lbl_extract_pic.setPixmap(nowpixmap)
        self.lbl_extraction.setText("<b>Extraction</b>")
        self.statusbar.showMessage("Extracting to temporary folder, please wait...")
        self.progressBar.setMaximum(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(-1)

    def finalcopy(self):
        logger.info("Copying to " + dir_)
        nowpixmap = QtGui.QPixmap(":/newPrefix/images/Actions-arrow-right-icon.png")
        donepixmap = QtGui.QPixmap(":/newPrefix/images/Check-icon.png")
        self.lbl_extract_pic.setPixmap(donepixmap)
        self.lbl_copy_pic.setPixmap(nowpixmap)
        self.lbl_copying.setText("<b>Copying</b>")
        self.lbl_task.setText("Copying files...")
        self.statusbar.showMessage(f"Copying files to {dir_}, please wait... ")

    def cleanup(self):
        logger.info("Cleaning up temp files")
        nowpixmap = QtGui.QPixmap(":/newPrefix/images/Actions-arrow-right-icon.png")
        donepixmap = QtGui.QPixmap(":/newPrefix/images/Check-icon.png")
        self.lbl_copy_pic.setPixmap(donepixmap)
        self.lbl_clean_pic.setPixmap(nowpixmap)
        self.lbl_cleanup.setText("<b>Cleaning up</b>")
        self.lbl_task.setText("Cleaning up...")
        self.statusbar.showMessage("Cleaning temporary files")

    def done(self):
        logger.info("Finished")
        donepixmap = QtGui.QPixmap(":/newPrefix/images/Check-icon.png")
        self.lbl_clean_pic.setPixmap(donepixmap)
        self.statusbar.showMessage("Ready")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        self.lbl_task.setText("Finished")
        self.btn_Quit.setEnabled(True)
        self.btn_update.hide()
        self.btn_update_launcher.hide()
        self.btn_execute.show()
        opsys = platform.system()
        if opsys == "Windows":
            self.btn_execute.clicked.connect(self.exec_windows)
        if opsys.lower == "darwin":
            self.btn_execute.clicked.connect(self.exec_osx)
        if opsys == "Linux":
            self.btn_execute.clicked.connect(self.exec_linux)


    def done_launcher(self):
        logger.info("Finished")
        donepixmap = QtGui.QPixmap(":/newPrefix/images/Check-icon.png")
        self.lbl_clean_pic.setPixmap(donepixmap)
        self.statusbar.showMessage("Ready")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        self.lbl_task.setText("Finished")
        self.btn_Quit.setEnabled(True)
        self.check_once()


    def exec_windows(self):
        _ = subprocess.Popen(os.path.join('"' + dir_ + "\\blender.exe" + '"'))
        logger.info(f"Executing {dir_}blender.exe")

    def exec_osx(self):
        BlenderOSXPath = os.path.join(
            '"' + dir_ + "\\blender.app/Contents/MacOS/blender" + '"'
        )
        os.system("chmod +x " + BlenderOSXPath)
        _ = subprocess.Popen(BlenderOSXPath)
        logger.info(f"Executing {BlenderOSXPath}")

    def exec_linux(self):
        _ = subprocess.Popen(os.path.join(f"{dir_}/blender"))
        logger.info(f"Executing {dir_}blender")


def main():
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    window = BlenderUpdater()
    window.setWindowTitle(f"ABLER Launcher")
    window.statusbar.setSizeGripEnabled(False)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
