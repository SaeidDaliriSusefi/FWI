import os
import requests
import gzip
import obspy
import numpy as np

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
                self.vp_data = self.vp_data 

        def run(self):
            self.download_and_extract()
            self.read_segy_file()
            self.process_data()
            return self.vp_data

if __name__ == "__main__":
    # Example usage
    true_model = TrueModel.Marmousi1_Velocity()
    vp_data = true_model.run()
