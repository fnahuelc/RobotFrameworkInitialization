import datetime
import sounddevice as sd
from acoustics import Signal, generator
import numpy as np
import math


class SoundCheck:
    ROBOT_LIBRARY_SCOPE = 'AS SOUND CHECK'

    def __init__(self):
        self.fs = 44100
        self.duration = 1
        self.atenuation = .1


    def rec_recall_curves_free_field(self):
        """ Free field correction curve"""
        pass

    def rec_recall_curves_a(self):
        """Recall A weighting curve"""
        from acoustics.standards.iec_61672_1_2013 import WEIGHTING_VALUES
        self.curve_a = WEIGHTING_VALUES['A']

    def mes_enter_test_level(self, test_level):
        self.test_level = float(test_level)

    def mes_enter_impedance(self, impedance):
        self.impedance_level = self.test_level/float(self.sq_root(self.conversion(float(impedance))))

    @staticmethod
    def conversion(r):
        """ ohm > milliohm conversion"""
        return r*1000

    @staticmethod
    def sq_root(num):
        """ Calculates voltage for 1 mW stimulus level"""
        return num ** .5

    def gen_500_hz(self, amp, duration):
        f = 500
        fun_sin = lambda t: math.sin(2.0*math.pi*f*t)
        return [amp*fun_sin(dt) for dt in np.arange(0.0, duration, 1.0/self.fs)]

    def sti_tone_500_hz_v(self):
        """500 Hz stimulus using test level"""
        tone = self.gen_500_hz(self.test_level, self.duration)
        self.tone_v = Signal(tone, fs=self.fs)

    def sti_tone_500_hz_mw(self):
        """500 Hz stimulus @ 1 mW"""
        tone = self.gen_500_hz(self.impedance_level, self.duration)
        self.tone_mv = Signal(tone, fs=self.fs)

    def sti_wav(self, audio_file):
        """Simulated program stimulus IEC 268_1 pink (15s).wav"""
        self.wav = Signal.from_wav(audio_file)

    def play_and_record(self, signal):
        data = sd.playrec(signal, samplerate=self.fs, channels=1, dtype='float64', blocking=True).transpose()
        return data

    def acq_play_and_record_v(self):
        self.rec_v = Signal(self.play_and_record(self.tone_v), fs=self.fs)

    def acq_play_and_record_mv(self):
        self.rec_mv = Signal(self.play_and_record(self.tone_mv), fs=self.fs)

    def acq_play_and_record_simulated_program_sig(self):
        self.rec_wav = Signal(self.play_and_record(self.wav), fs=self.fs)

    def ana_fundamental_v(self):
        self.fundamental_v = self.rec_v.power_spectrum()[1].max()

    def ana_fundamental_mv(self):
        self.fundamental_mv = self.rec_mv.power_spectrum()[1].max()

    def ana_rta_spectrum(self):
        self.rta_spectrum = self.rec_wav.power_spectrum()[1]

    def pos_a_wight_RTA(self):
        """Applies A weighting to the Simulated Program spectra"""
        self.rta_spectrum_a = self.rec_wav.weigh('A').power_spectrum()[1]

    def pos_ff_correct_rta(self):
        """Applies Free Field correction to the A weighted curves"""
        self.ff_correct_rta = self.rta_spectrum_a

    def pos_power_sum_cs(self):
        """Power sums weighted/corrected spectrum [L]"""
        self.power_sum_cs = np.sum(self.ff_correct_rta)

    def pos_power_sum(self):
        """Power sums spectrum [L]"""
        self.power_sum = np.sum(self.rta_spectrum)

    def pos_curve_average_v(self):
        """500 Hz sensitivity (V) [L]"""
        self.curve_average_v = self.fundamental_v / self.test_level

    def pos_curve_average_mv(self):
        """500 Hz sensitivity (mV) [L]"""
        self.curve_average_mv = self.fundamental_mv / self.impedance_level

    def get_parameters(self):
        return{
            'power_sum_cs': self.power_sum_cs,
            'power_sum': self.power_sum,
            'curve_average_v':  self.curve_average_v,
            'curve_average_mv': self.curve_average_mv
        }

    def get_plots(self):
        return list(map(self.save_spectrum, [
            self.rec_wav.weigh('A').plot_third_octaves(**{'xlim':[20, 20000]}),
            self.rec_wav.weigh('A').plot_power_spectrum(**{'xlim':[20, 20000]})
        ]))

    @staticmethod
    def save_spectrum(fig):
        filename = '%s.png' % str(datetime.datetime.now())
        fig.savefig('spectrums/%s' % filename)
        return '<img src="http://localhost:63342/custom/spectrums/%s">' % filename

if __name__ == "__main__":
    sh = SoundCheck()
    sh.rec_recall_curves_free_field()
    sh.rec_recall_curves_a()
    sh.mes_enter_test_level(1)
    sh.mes_enter_impedance(8)
    sh.sti_tone_500_hz_v()
    sh.sti_tone_500_hz_mw()
    sh.sti_wav('../Audios/IEC 268_1 pink (15s).wav')
    sh.acq_play_and_record_v()
    sh.acq_play_and_record_mv()
    sh.acq_play_and_record_simulated_program_sig()
    sh.ana_fundamental_v()
    sh.ana_fundamental_mv()
    sh.ana_rta_spectrum()
    sh.pos_a_wight_RTA()
    sh.pos_ff_correct_rta()
    sh.pos_power_sum_cs()
    sh.pos_power_sum()
    sh.pos_curve_average_v()
    sh.pos_curve_average_mv()
    sh.dis_headphone_spl()
