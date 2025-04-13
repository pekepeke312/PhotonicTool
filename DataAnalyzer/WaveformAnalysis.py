import logging

log = logging.getLogger(__name__)

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np


class WaveformAnalysis():
    def __init__(self, x, y):
        try:
            self.x = x
            if len(x) == len(y):
                self.y = y
        except Exception as ex:
            try:
                log.error(f"Data Length does not match between x and y: {ex}")
            finally:
                # Re-raise the exception
                raise ex

    def plot(self, title="", xlabel="", ylabel=""):
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(1, 1, 1)
        self.axis.plot(self.x, self.y)
        self.axis.set_title(title)
        self.axis.set_xlabel(xlabel)
        self.axis.set_ylabel(ylabel)

    def get_rise_time(self, time="", signal="", thresh_low=0.1, thresh_high=0.9):
        """
        Calculate the rise time of a waveform.
        
        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.
    
        Returns:
        - rise_time (float): The rise time of the waveform.
        """

        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Find the min and max signal values
        min_val = np.min(signal)
        max_val = np.max(signal)

        # Calculate the 10% and 90% levels of the signal
        low_level = min_val + thresh_low * (max_val - min_val)
        high_level = min_val + thresh_high * (max_val - min_val)

        # Find the time indices where the signal crosses these levels
        low_index = None
        high_index = None

        for i in range(1, len(signal)):
            if signal[i - 1] < low_level <= signal[i]:
                low_index = i
            if signal[i - 1] < high_level <= signal[i]:
                high_index = i
                break

        # If we found valid low and high indices, calculate the rise time
        if low_index is not None and high_index is not None:
            rise_time = time[high_index] - time[low_index]
        else:
            rise_time = 0.0  # If the rise couldn't be detected

        if rise_time >= 0:
            return rise_time
        else:
            return "No rise signal"

    def get_fall_time(self, time="", signal="", thresh_low=0.1, thresh_high=0.9):
        """
        Calculate the fall time of a waveform.

        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.

        Returns:
        - fall_time (float): The fall time of the waveform.
        """

        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Find the min and max signal values
        min_val = np.min(signal)
        max_val = np.max(signal)

        # Calculate the 10% and 90% levels of the signal
        low_level = min_val + thresh_low * (max_val - min_val)
        high_level = min_val + thresh_high * (max_val - min_val)

        # Find the time indices where the signal crosses these levels
        low_index = None
        high_index = None

        for i in range(1, len(signal)):
            if signal[i - 1] > high_level >= signal[i]:
                high_index = i
            if signal[i - 1] > low_level >= signal[i]:
                low_index = i
                break

        # If we found valid low and high indices, calculate the rise time
        if low_index is not None and high_index is not None:
            fall_time = time[low_index] - time[high_index]
        else:
            fall_time = 0.0  # If the rise couldn't be detected

        if fall_time >= 0:
            return fall_time
        else:
            return "No fall signal"

    def get_pulse_count(self, time="", signal="", threshold=None):
        """
        Count the number of pulses in a waveform.

        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.
        - threshold (float): The threshold value to distinguish between high and low levels.
                             If None, the average of the signal's min and max values is used.

        Returns:
        - pulse_count (int): The number of pulses in the waveform.
        """

        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Determine the threshold level if not provided
        if threshold is None:
            min_val = np.min(signal)
            max_val = np.max(signal)
            threshold = (min_val + max_val) / 2

        # Initialize pulse count
        pulse_count = 0

        # Track whether we're in a high state
        in_high_state = False

        # Loop through the signal to count pulses
        for i in range(1, len(signal)):
            if signal[i] >= threshold and not in_high_state:
                # Transition from low to high
                pulse_count += 1
                in_high_state = True
            elif signal[i] < threshold and in_high_state:
                # Transition from high to low
                in_high_state = False

        return pulse_count

    def get_pulse_duty(self, time="", signal="", threshold=None):
        """
        Calculate the duty cycle of a waveform.

        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.
        - threshold (float): The threshold value to distinguish between high and low levels.
                             If None, the average of the signal's min and max values is used.

        Returns:
        - duty_cycle (float): The duty cycle of the waveform as a percentage.
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Determine the threshold level if not provided
        if threshold is None:
            min_val = np.min(signal)
            max_val = np.max(signal)
            threshold = (min_val + max_val) / 2

        # Find where the signal is above the threshold
        high_indices = np.where(signal >= threshold)[0]

        if len(high_indices) == 0:
            return 0.0

        # Calculate the total high time
        high_time = 0.0
        start_time = None

        for i in range(1, len(high_indices)):
            if high_indices[i] != high_indices[i - 1] + 1:
                # We've reached the end of a high pulse
                if start_time is not None:
                    high_time += time[high_indices[i - 1]] - start_time
                    start_time = None
            if start_time is None:
                start_time = time[high_indices[i]]

        # Add the last high pulse time
        if start_time is not None:
            high_time += time[high_indices[-1]] - start_time

        # Calculate the period of the waveform
        period = time[-1] - time[0]

        # Calculate the duty cycle as a percentage
        duty_cycle = (high_time / period)

        return duty_cycle

    def get_minus_duty(self, time="", signal="", threshold=None):
        """
        Calculate the duty cycle of a waveform.

        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.
        - threshold (float): The threshold value to distinguish between high and low levels.
                             If None, the average of the signal's min and max values is used.

        Returns:
        - duty_cycle (float): The duty cycle of the waveform as a percentage.
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Determine the threshold level if not provided
        if threshold is None:
            min_val = np.min(signal)
            max_val = np.max(signal)
            threshold = (min_val + max_val) / 2

        # Find where the signal is above the threshold
        low_indices = np.where(signal <= threshold)[0]

        if len(low_indices) == 0:
            return 0.0

        # Calculate the total high time
        low_time = 0
        start_time = None

        for i in range(1, len(low_indices)):
            if low_indices[i] != low_indices[i - 1] + 1:
                # We've reached the end of a high pulse
                if start_time is not None:
                    low_time += time[low_indices[i - 1]] - start_time
                    start_time = None
            if start_time is None:
                start_time = time[low_indices[i]]


        # Add the last high pulse time
        if start_time is not None:
            low_time += time[low_indices[-1]] - start_time

        # Calculate the period of the waveform
        period = time[-1] - time[0]

        # Calculate the duty cycle as a percentage
        duty_cycle = (low_time / period)

        return duty_cycle

    def get_data_point(self, time="", signal=""):
        """
        Calculate the data point of a waveform.

        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.

        Returns:
        - datapoint[0] (int): datapoint of time.
        - datapoint[1] (int): datapoint of signal
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        datapoint = {}
        datapoint[0] = len(time)
        datapoint[1] = len(signal)

        return datapoint

    def get_frequency(self, time="", signal=""):
        """
        Calculate the dominant frequency of a waveform using FFT.

        Parameters:
        - time (array-like): The time values corresponding to the signal.
        - signal (array-like): The signal values.

        Returns:
        - dominant_frequency (float): The dominant frequency of the waveform in Hz.
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Number of sample points
        N = self.get_data_point()[0]

        # Sample spacing
        T = time[1] - time[0]  # Assuming uniform sampling

        # Perform FFT
        yf = np.fft.fft(signal)

        # Compute the frequency values
        xf = np.fft.fftfreq(N, T)
        xf = np.fft.fftshift(xf)  # Shift zero frequency component to center
        yf = np.fft.fftshift(yf)  # Shift zero frequency component to center

        # Compute the magnitude of the FFT
        magnitude = np.abs(yf[:N // 2])

        # Find the peak in the magnitude, which corresponds to the dominant frequency
        idx = np.argmax(magnitude)
        dominant_frequency = np.abs(xf[idx])

        return dominant_frequency

    def get_moving_average(self, signal=""):
        """
            Calculate the moving average of a 1D array.

            Parameters:
                data (numpy array): The input data array.

            Returns:
                numpy array: The array of moving average values, same length as input data.
        """
        if signal == "":
            signal = self.y

        #window_size = self.get_data_point()[1] // self.get_pulse_count()
        window_size = 10

        # Pad the data on both ends
        pad_width = window_size // 2
        padded_data = np.pad(signal, (pad_width, pad_width), mode='edge')

        smoothed_data = np.convolve(padded_data, np.ones(window_size) / window_size, mode='valid')

        return smoothed_data

    def get_top(self, signal="", threshold=0.90):
        """
            Calculate the moving average of a 1D array.

            Parameters:
                data (numpy array): The input data array.
                threshold: Setting for stable definition

            Returns:
                numpy array: The array of moving average values, same length as input data.
        """
        if signal == "":
            signal = self.y

        moving_average = self.get_moving_average(signal=signal)

        # Use the top percentile values to find the Top to avoid noise interference
        high_region_values = moving_average[moving_average > np.percentile(moving_average, threshold)]

        if len(high_region_values) > 0:
            return np.max(moving_average)  # Fallback to max if no high region found
        else:
            return np.mean(high_region_values)  # Average of the high-stability region

    def get_base(self, signal="", threshold=0.10):
        """
            Calculate the moving average of a 1D array.

            Parameters:
                signal (numpy array): The input data array.
                threshold: Setting for stable definition

            Returns:
                numpy array: The array of moving average values, same length as input data.
        """
        if signal == "":
            signal = self.y

        moving_average = self.get_moving_average(signal=signal)

        # Use the top percentile values to find the Top to avoid noise interference
        low_region_values = moving_average[moving_average > np.percentile(moving_average, threshold)]

        if len(low_region_values) > 0:
            return np.min(moving_average)  # Fallback to min if low region found
        else:
            return np.mean(low_region_values)  # Average of the low-stability region

    def get_max(self, signal=""):
        """
            Calculate the moving average of a 1D array.

            Parameters:
                signal (numpy array): The input data array.

            Returns:
                max (float): The max value of the waveform.
        """
        if signal == "":
            signal = self.y

        return np.max(signal)

    def get_min(self, signal=""):
        """
            Calculate the moving average of a 1D array.

            Parameters:
                signal (numpy array): The input data array.

            Returns:
                min (float): The min value of the waveform.
        """
        if signal == "":
            signal = self.y

        return np.min(signal)

    def get_pk_to_pk(self, signal=""):
        """
            Calculate the moving average of a 1D array.

            Parameters:
                signal (numpy array): The input data array.

            Returns:
                pk2pk (float): The peak to peak value of the waveform.
        """
        if signal == "":
            signal = self.y

        return np.max(signal) - np.min(signal)

    def get_amplitude(self, signal=""):
        if signal == "":
            signal = self.y
        return self.get_top(signal) - self.get_base()

    def get_mean(self, signal=""):
        if signal == "":
            signal = self.y
        return np.mean(signal)

    def get_stdev(self, signal=""):
        if signal == "":
            signal = self.y
        return np.std(signal)

    def get_rms(self, signal=""):
        """
        Calculate the RMS value of a 1D array.

        Parameters:
            signal (numpy array): The input data array representing the waveform.

        Returns:
            float: The RMS value of the waveform.
        """
        if signal == "":
            signal = self.y
        return np.sqrt(np.mean(np.square(signal)))

    def get_period(self, time="", signal=""):
        """
        Calculate the Period of a 1D array.

        Parameters:
            time (numpy array): The input data array representing the waveform.
            signal (numpy array): The input data array representing the waveform.

        Returns:
            float: The period value of the waveform.
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Ensure that time and signal are numpy arrays
        time = np.asarray(time)
        signal = np.asarray(signal)

        # Find peaks
        peaks, _ = find_peaks(signal)

        # Calculate the period
        if len(peaks) > 1:
            peak_times = time[peaks]
            peak_distances = np.diff(peak_times)  # Time differences between successive peaks
            period = np.mean(peak_distances)
            return period
        else:
            raise ValueError('Not enough peaks to calculate period')

    def get_time_of_top(self, time="", signal="", threshold=0.9):
        """
        Calculate the Period of a 1D array.

        Parameters:
            time (numpy array): The input data array representing the waveform.
            signal (numpy array): The input data array representing the waveform.
            threshold: Setting for stable definition

        Returns:
            float: The time duration of top part of the waveform.
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Ensure that time and signal are numpy arrays
        time = np.asarray(time)
        signal = np.asarray(signal)

        # Find peaks in the signal
        peaks, _ = find_peaks(signal)

        # Calculate the duration of the top part for each peak
        durations = []
        for peak in peaks:
            # Find indices where the signal is above the threshold around each peak
            start_idx = peak
            while start_idx > 0 and signal[start_idx] >= threshold:
                start_idx -= 1
            start_idx += 1  # Adjust to include the correct start point

            end_idx = peak
            while end_idx < len(signal) - 1 and signal[end_idx] >= threshold:
                end_idx += 1
            end_idx -= 1  # Adjust to include the correct end point

            if start_idx < end_idx:
                duration = time[end_idx] - time[start_idx]
                durations.append(duration)

        # Calculate the average duration
        average_duration = np.mean(durations)
        return average_duration

    def get_time_of_base(self, time="", signal="", threshold=0.1):
        """
        Calculate the Period of a 1D array.

        Parameters:
            time (numpy array): The input data array representing the waveform.
            signal (numpy array): The input data array representing the waveform.
            threshold: Setting for stable definition

        Returns:
            float: The time duration of top part of the waveform.
        """
        if time == "":
            time = self.x
        if signal == "":
            signal = self.y

        # Ensure that time and signal are numpy arrays
        time = np.asarray(time)
        signal = np.asarray(signal)

        # Find negative peaks in the signal
        negative_peaks, _ = find_peaks(-signal)

        # Identify intervals below the threshold
        below_threshold = signal <= threshold
        start_idx = None
        base_intervals = []

        for i in range(len(signal)):
            if below_threshold[i] and start_idx is None:
                start_idx = i
            elif not below_threshold[i] and start_idx is not None:
                end_idx = i - 1
                if start_idx <= end_idx:
                    base_intervals.append((start_idx, end_idx))
                start_idx = None

        if start_idx is not None:  # Handle case where the signal ends below threshold
            base_intervals.append((start_idx, len(signal) - 1))

        # Calculate durations of base intervals
        durations = []
        for start_idx, end_idx in base_intervals:
            base_duration = time[end_idx] - time[start_idx]
            durations.append(base_duration)

        return np.mean(durations)


if __name__ == "__main__":
    import numpy as np
    from scipy import signal

    Time = np.linspace(start=-0.1, stop=0.1, num=1000, endpoint=False)
    FRQ = 50
    AMP = 5
    DUTY = 0.2

    #Test Waveform #1
    #Vertical = AMP - np.exp(-5 * Time)

    #Test Waveform #2
    Vertical = AMP * signal.square(2 * np.pi * FRQ * Time, duty=DUTY)

    #Test Waveform #3
    #Vertical = AMP * signal.sawtooth(2 * np.pi * FRQ * Time, width=0.2)

    wav = WaveformAnalysis(x=Time, y=Vertical)
    wav.plot(title="Sample Graph", xlabel="Time", ylabel="Voltage")

    print("""
    ---------------------------------------
    Measurement Function of Vertical part
    --------------------------------------- 
    """)
    print("Rise Time : {:.6f}s".format(wav.get_rise_time(thresh_low=0.1, thresh_high=0.9)))
    print("Fall Time : {:.6f}s".format(wav.get_fall_time(thresh_high=0.9, thresh_low=0.1)))
    print("Top : {:.6f}".format(wav.get_top()))
    print("Base : {:.6f}".format(wav.get_base()))
    print("Max : {:.6f}".format(wav.get_max()))
    print("Min : {:.6f}".format(wav.get_min()))
    print("Pk-Pk : {:.6f}".format(wav.get_pk_to_pk()))
    print("Amplitude : {:.6f}".format(wav.get_amplitude()))
    print("Mean : {:.6f}".format(wav.get_mean()))
    print("Stdev : {:.6f}".format(wav.get_stdev()))
    print("RMS : {:.6f}".format(wav.get_rms()))

    print("""
    ---------------------------------------
    Measurement Function of Horizontal part 
    ---------------------------------------
    """)

    print("Period : {:.6f}s".format(wav.get_period()))
    print("Frequency: {:.6f}Hz".format(wav.get_frequency()))
    print("+Duty : {:.6f}".format(wav.get_pulse_duty()))
    print("-Duty : {:.6f}".format(wav.get_minus_duty()))
    print(f"Pulse Count : {wav.get_pulse_count()}")
    print(f"Datapoint X-Axis: {wav.get_data_point()[0]}, Y-Axis: {wav.get_data_point()[1]}")
    print("Time of Top : {:.6f}s".format(wav.get_time_of_top()))
    print("Time of Base : {:.6f}s".format(wav.get_time_of_base()))

    plt.show()
