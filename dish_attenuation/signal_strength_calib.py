#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: maraly
# GNU Radio version: v3.9.2.0-85-g08bb05c1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import signal_strength_calib_epy_block_0 as epy_block_0  # embedded python block
import signal_strength_calib_epy_block_1 as epy_block_1  # embedded python block
import signal_strength_calib_epy_block_2 as epy_block_2  # embedded python block
import signal_strength_calib_epy_block_3 as epy_block_3  # embedded python block


def snipfcn_snippet_0(self):
    #Bugfix 1: the control should never be written into self.var. Since this makes it impossible to have two user inputs that are needed in the same calculation
    #Bugfix 2: .getValue() calls .getFrequency() but doesn't return it
    self.freq = self._freq_msgdigctl_win.getFrequency()
    self.sig_delta = self._sig_delta_msgdigctl_win.getFrequency()

def snipfcn_snippet_1(self):
    self.epy_block_0.setup(self._gain_win.d_widget.counter ,self._agc_mode_combo_box)


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)
    snipfcn_snippet_1(tb)

from gnuradio import qtgui

class signal_strength_calib(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "signal_strength_calib")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sig_delta = sig_delta = 213828
        self.show_lpf = show_lpf = 1
        self.samp_rate = samp_rate = 3000000
        self.gain = gain = 0
        self.freq = freq = 436600000
        self.exp_name = exp_name = '0'
        self.exp_angle = exp_angle = 0
        self.agc_mode = agc_mode = 0

        ##################################################
        # Blocks
        ##################################################
        self._sig_delta_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl = 'Signal offset', min_freq_hz = 100000, max_freq_hz=1000000, parent=self,  thousands_separator=",",background_color="black",fontColor="white", var_callback=self.set_sig_delta,outputmsgname="'sig_delta'".replace("'",""))
        self._sig_delta_msgdigctl_win.setValue(213828)
        self._sig_delta_msgdigctl_win.setReadOnly(False)
        self.sig_delta = self._sig_delta_msgdigctl_win

        self.top_grid_layout.addWidget(self._sig_delta_msgdigctl_win, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        if int == bool:
        	self._show_lpf_choices = {'Pressed': bool(1), 'Released': bool(0)}
        elif int == str:
        	self._show_lpf_choices = {'Pressed': "1".replace("'",""), 'Released': "0".replace("'","")}
        else:
        	self._show_lpf_choices = {'Pressed': 1, 'Released': 0}

        _show_lpf_toggle_button = qtgui.GrToggleSwitch(self.set_show_lpf, 'Show LPF', self._show_lpf_choices, True,"green","gray",4, 50, 1, 1,self,"'value'".replace("'",""))
        self.show_lpf = _show_lpf_toggle_button

        self.top_grid_layout.addWidget(_show_lpf_toggle_button, 0, 8, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(8, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0, 73, 1, 0, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Input gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 1, 4, 1, 5)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl = 'Center frequency', min_freq_hz = 80e6, max_freq_hz=3.5e9, parent=self,  thousands_separator=",",background_color="black",fontColor="white", var_callback=self.set_freq,outputmsgname="'freq'".replace("'",""))
        self._freq_msgdigctl_win.setValue(436600000)
        self._freq_msgdigctl_win.setReadOnly(False)
        self.freq = self._freq_msgdigctl_win

        self.top_grid_layout.addWidget(self._freq_msgdigctl_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._exp_name_tool_bar = Qt.QToolBar(self)
        self._exp_name_tool_bar.addWidget(Qt.QLabel('Dish name' + ": "))
        self._exp_name_line_edit = Qt.QLineEdit(str(self.exp_name))
        self._exp_name_tool_bar.addWidget(self._exp_name_line_edit)
        self._exp_name_line_edit.returnPressed.connect(
            lambda: self.set_exp_name(str(str(self._exp_name_line_edit.text()))))
        self.top_grid_layout.addWidget(self._exp_name_tool_bar, 0, 4, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._exp_angle_tool_bar = Qt.QToolBar(self)
        self._exp_angle_tool_bar.addWidget(Qt.QLabel('Angle' + ": "))
        self._exp_angle_line_edit = Qt.QLineEdit(str(self.exp_angle))
        self._exp_angle_tool_bar.addWidget(self._exp_angle_line_edit)
        self._exp_angle_line_edit.returnPressed.connect(
            lambda: self.set_exp_angle(eng_notation.str_to_num(str(self._exp_angle_line_edit.text()))))
        self.top_grid_layout.addWidget(self._exp_angle_tool_bar, 0, 5, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._agc_mode_options = [0, 1, 2]
        # Create the labels list
        self._agc_mode_labels = ['Off', 'Sweep', 'AGC']
        # Create the combo box
        self._agc_mode_tool_bar = Qt.QToolBar(self)
        self._agc_mode_tool_bar.addWidget(Qt.QLabel("agc_mode: "))
        self._agc_mode_combo_box = Qt.QComboBox()
        self._agc_mode_tool_bar.addWidget(self._agc_mode_combo_box)
        for _label in self._agc_mode_labels: self._agc_mode_combo_box.addItem(_label)
        self._agc_mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._agc_mode_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._agc_mode_options.index(i)))
        self._agc_mode_callback(self.agc_mode)
        self._agc_mode_combo_box.currentIndexChanged.connect(
            lambda i: self.set_agc_mode(self._agc_mode_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._agc_mode_tool_bar, 0, 6, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_plutosdr_source_0 = None
        dev = 'driver=plutosdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_plutosdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_plutosdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_plutosdr_source_0.set_bandwidth(0, 0)
        self.soapy_plutosdr_source_0.set_gain_mode(0, False)
        self.soapy_plutosdr_source_0.set_frequency(0, freq)
        self.soapy_plutosdr_source_0.set_gain(0, min(max(gain, 0.0), 73.0))
        self.save_button = _save_button_toggle_button = qtgui.MsgPushButton('Save', 'pressed',True,"default","default")
        self.save_button = _save_button_toggle_button

        self.top_grid_layout.addWidget(_save_button_toggle_button, 0, 7, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(7, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            16384, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            False, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_win, 2, 0, 5, 9)
        for r in range(2, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0_0_0.set_update_time(0.01)
        self.qtgui_number_sink_0_0_0_0.set_title("RMS")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_0_win, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0_0.set_update_time(0.01)
        self.qtgui_number_sink_0_0_0.set_title("Amplitude")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Saturation")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, samp_rate, 5000, 200, window.WIN_HAMMING, 6.76), 1)
        self.epy_block_3 = epy_block_3.blk(filename="test.csv", fmts=["%s","%d","%f","%f"], columns=[exp_name,freq+sig_delta,exp_angle,gain])
        self.epy_block_2 = epy_block_2.blk(batch_length=65536)
        self.epy_block_1 = epy_block_1.blk(batch_length=65536)
        self.epy_block_0 = epy_block_0.blk(strength=0.01, gain=gain, agc_mode=agc_mode, sweep_delay=100, sweep_step=1)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,show_lpf,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((-sig_delta)*6.28318530718 /samp_rate, False)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 10)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.audio_sink_0 = audio.sink(20000, '', True)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=300000,
        	audio_decim=15,
        	deviation=5000,
        	audio_pass=2000,
        	audio_stop=5000,
        	gain=1.0,
        	tau=75e-6,
        )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'messageOutput'), (self.epy_block_3, 'saveButton'))
        self.msg_connect((self.save_button, 'pressed'), (self.epy_block_3, 'saveButton'))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.epy_block_2, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_1, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.epy_block_2, 0), (self.epy_block_3, 0))
        self.connect((self.epy_block_2, 1), (self.epy_block_3, 1))
        self.connect((self.epy_block_2, 0), (self.qtgui_number_sink_0_0_0, 0))
        self.connect((self.epy_block_2, 1), (self.qtgui_number_sink_0_0_0_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.epy_block_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "signal_strength_calib")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sig_delta(self):
        return self.sig_delta

    def set_sig_delta(self, sig_delta):
        self.sig_delta = sig_delta
        self.blocks_rotator_cc_0.set_phase_inc((-self.sig_delta)*6.28318530718 /self.samp_rate)
        self.epy_block_3.columns = [self.exp_name,self.freq+self.sig_delta,self.exp_angle,self.gain]

    def get_show_lpf(self):
        return self.show_lpf

    def set_show_lpf(self, show_lpf):
        self.show_lpf = show_lpf
        self.blocks_selector_0.set_input_index(self.show_lpf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc((-self.sig_delta)*6.28318530718 /self.samp_rate)
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 200, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.soapy_plutosdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.epy_block_0.gain = self.gain
        self.epy_block_3.columns = [self.exp_name,self.freq+self.sig_delta,self.exp_angle,self.gain]
        self.soapy_plutosdr_source_0.set_gain(0, min(max(self.gain, 0.0), 73.0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.epy_block_3.columns = [self.exp_name,self.freq+self.sig_delta,self.exp_angle,self.gain]
        self.soapy_plutosdr_source_0.set_frequency(0, self.freq)

    def get_exp_name(self):
        return self.exp_name

    def set_exp_name(self, exp_name):
        self.exp_name = exp_name
        Qt.QMetaObject.invokeMethod(self._exp_name_line_edit, "setText", Qt.Q_ARG("QString", str(self.exp_name)))
        self.epy_block_3.columns = [self.exp_name,self.freq+self.sig_delta,self.exp_angle,self.gain]

    def get_exp_angle(self):
        return self.exp_angle

    def set_exp_angle(self, exp_angle):
        self.exp_angle = exp_angle
        Qt.QMetaObject.invokeMethod(self._exp_angle_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.exp_angle)))
        self.epy_block_3.columns = [self.exp_name,self.freq+self.sig_delta,self.exp_angle,self.gain]

    def get_agc_mode(self):
        return self.agc_mode

    def set_agc_mode(self, agc_mode):
        self.agc_mode = agc_mode
        self._agc_mode_callback(self.agc_mode)
        self.epy_block_0.agc_mode = self.agc_mode




def main(top_block_cls=signal_strength_calib, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
