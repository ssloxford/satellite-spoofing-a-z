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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore


def snipfcn_snippet_0(self):
    #Bugfix 1: the control should never be written into self.var. Since this makes it impossible to have two user inputs that are needed in the same calculation
    #Bugfix 2: .getValue() calls .getFrequency() but doesn't return it
    self.freq = self._freq_msgdigctl_win.getFrequency()
    self.sig_delta = self._sig_delta_msgdigctl_win.getFrequency()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

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
        self.samp_rate = samp_rate = 3000000
        self.gain = gain = 0
        self.freq = freq = 143800000

        ##################################################
        # Blocks
        ##################################################
        self._sig_delta_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl = 'Signal offset', min_freq_hz = 100000, max_freq_hz=500000, parent=self,  thousands_separator=",",background_color="black",fontColor="white", var_callback=self.set_sig_delta,outputmsgname="'sig_delta'".replace("'",""))
        self._sig_delta_msgdigctl_win.setValue(213828)
        self._sig_delta_msgdigctl_win.setReadOnly(False)
        self.sig_delta = self._sig_delta_msgdigctl_win

        self.top_layout.addWidget(self._sig_delta_msgdigctl_win)
        self._gain_range = Range(0, 73, 1, 0, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Input gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self._freq_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl = 'Center frequency', min_freq_hz = 100e6, max_freq_hz=1e9, parent=self,  thousands_separator=",",background_color="black",fontColor="white", var_callback=self.set_freq,outputmsgname="'freq'".replace("'",""))
        self._freq_msgdigctl_win.setValue(143800000)
        self._freq_msgdigctl_win.setReadOnly(False)
        self.freq = self._freq_msgdigctl_win

        self.top_layout.addWidget(self._freq_msgdigctl_win)
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
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            4096, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq+sig_delta, #fc
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

        self.qtgui_sink_x_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
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
            self.qtgui_number_sink_0_0_0.set_max(i, 1000)
            self.qtgui_number_sink_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_0_0_win)
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
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, samp_rate, 5000, 200, window.WIN_HAMMING, 6.76), 1)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((-sig_delta)*6.28318530718 /samp_rate, False)
        self.blocks_moving_average_xx_1_0 = blocks.moving_average_ff(1000, 1.58/1000, 4000, 1)
        self.blocks_moving_average_xx_1 = blocks.moving_average_ff(1000, 1.58/1000, 4000, 1)
        self.blocks_moving_average_xx_0_0_0 = blocks.moving_average_ff(262144, 1000/262144, 65536, 1)
        self.blocks_max_xx_0 = blocks.max_ff(1, 1)
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 262144)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_abs_xx_0_0 = blocks.abs_ff(1)
        self.blocks_abs_xx_0 = blocks.abs_ff(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_abs_xx_0, 0), (self.blocks_moving_average_xx_1, 0))
        self.connect((self.blocks_abs_xx_0_0, 0), (self.blocks_moving_average_xx_1_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_abs_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_abs_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_moving_average_xx_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.qtgui_number_sink_0_0_0, 0))
        self.connect((self.blocks_max_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_1, 0), (self.blocks_max_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_1_0, 0), (self.blocks_max_xx_0, 1))
        self.connect((self.blocks_rotator_cc_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.blocks_rotator_cc_0, 0))


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
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq+self.sig_delta, self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc((-self.sig_delta)*6.28318530718 /self.samp_rate)
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 200, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq+self.sig_delta, self.samp_rate)
        self.soapy_plutosdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_plutosdr_source_0.set_gain(0, min(max(self.gain, 0.0), 73.0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq+self.sig_delta, self.samp_rate)
        self.soapy_plutosdr_source_0.set_frequency(0, self.freq)




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
