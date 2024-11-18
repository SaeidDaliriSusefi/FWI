# -*- coding: utf-8 -*-
import os
import requests
import gzip
import obspy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

class TrueModel:
    """
    The base class for different types of true models.
    """

    class Marmousi1_Velocity:
        def __init__(self, vp_url='http://math.mit.edu/~rhewett/pysit/marmousi/velocity_rev1.segy.gz', output_filename='velocity_rev1.segy', max_depth_km=3.0, max_distance_km=16.0):
            self.vp_url = vp_url
            self.output_filename = output_filename
            self.max_depth_km = max_depth_km
            self.max_distance_km = max_distance_km
            self.vp_data = None

        def download_and_extract(self, verbose=True):
            if os.path.exists(self.output_filename):
                if verbose:
                    pass
                return

            try:
                response = requests.get(self.vp_url, stream=True)
                response.raise_for_status()
                with open(self.output_filename + '.gz', 'wb') as f:
                    f.write(response.content)
            except requests.RequestException as e:
                print(f'Failed to download {self.vp_url}: {e}')
                return

            try:
                with gzip.open(self.output_filename + '.gz', 'rb') as f_in:
                    with open(self.output_filename, 'wb') as f_out:
                        f_out.write(f_in.read())
            except OSError as e:
                print(f'Failed to extract {self.output_filename}.gz: {e}')
                return

            os.remove(self.output_filename + '.gz')

        def read_segy_file(self):
            try:
                segy = obspy.read(self.output_filename, format='SEGY')
                self.vp_data = np.array([tr.data for tr in segy.traces])
            except Exception as e:
                self.vp_data = None

        def process_data(self):
            if self.vp_data is not None:
                self.vp_data = self.vp_data * 1000

        def plot_model(self, fig_size=(6, 3)):
            if self.vp_data is not None:
                fig, ax = plt.subplots(figsize=fig_size)
                cax = ax.imshow(self.vp_data, cmap='jet', aspect='auto', origin='upper',
                                extent=[0, self.max_distance_km, self.max_depth_km, 0])
                cbar = fig.colorbar(cax, ax=ax, orientation='vertical', pad=0.02)
                cbar.set_label('P-wave Velocity (m/s)', fontsize=12)
                
                # Disable scientific notation on scale bar
                cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

                ax.set_title('Marmousi1 P-wave Velocity Model', fontsize=14, loc='center', pad=10)
                ax.set_xlabel('Distance (Km)', fontsize=12, labelpad=10)
                ax.set_ylabel('Depth (Km)', fontsize=12, labelpad=10)
                plt.tight_layout()
                plt.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.1)
                plt.show()

        def run(self, fig_size=(6, 3)):
            self.download_and_extract()
            self.read_segy_file()
            self.process_data()
            self.plot_model(fig_size=fig_size)

# Example usage:
if __name__ == "__main__":
    marmousi1_velocity = TrueModel.Marmousi1_Velocity()
    marmousi1_velocity.run(fig_size=(10, 5))
