import os
import requests
import gzip
import obspy
import numpy as np

class TrueModel:
    """
    The base class for different types of true models.
    """

    def __init__(self, url, output_filename, max_depth_km=3.0, max_distance_km=16.0):
        self.url = url
        self.output_filename = output_filename
        self.max_depth_km = max_depth_km
        self.max_distance_km = max_distance_km
        self.data = None

    def download_and_extract(self, verbose=True):
        if os.path.exists(self.output_filename):
            if verbose:
                print(f"{self.output_filename} already exists.")
            return

        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            with open(self.output_filename + '.gz', 'wb') as f:
                f.write(response.content)
        except requests.RequestException as e:
            if verbose:
                print(f'Failed to download {self.url}: {e}')
            return

        try:
            with gzip.open(self.output_filename + '.gz', 'rb') as f_in:
                with open(self.output_filename, 'wb') as f_out:
                    f_out.write(f_in.read())
        except OSError as e:
            if verbose:
                print(f'Failed to extract {self.output_filename}.gz: {e}')
            return

        os.remove(self.output_filename + '.gz')

    def read_segy_file(self):
        try:
            segy = obspy.read(self.output_filename, format='SEGY')
            self.data = np.array([tr.data for tr in segy.traces])
        except Exception as e:
            print(f"Failed to read SEGY file {self.output_filename}: {e}")
            self.data = None

    def process_data(self):
        if self.data is not None:
            self.data = np.flipud(self.data)
            self.data = np.rot90(self.data, k=3)
            self.data = self.data * 1000

    def run(self, verbose=True):
        self.download_and_extract(verbose=verbose)
        self.read_segy_file()
        self.process_data()

# Marmousi1 Velocity Model
class Marmousi1_Velocity(TrueModel):
    def __init__(self):
        super().__init__(
            url='http://math.mit.edu/~rhewett/pysit/marmousi/velocity_rev1.segy.gz',
            output_filename='velocity_rev1.segy'
        )

# Marmousi1 Density Model
class Marmousi1_Density(TrueModel):
    def __init__(self):
        super().__init__(
            url='http://math.mit.edu/~rhewett/pysit/marmousi/density_rev1.segy.gz',
            output_filename='density_rev1.segy'
        )

# Marmousi2 Velocity Model
class Marmousi2_Velocity(TrueModel):
    def __init__(self):
        super().__init__(
            url='http://www.agl.uh.edu/downloads/vp_marmousi-ii.segy.gz',
            output_filename='vp_marmousi-ii.segy'
        )

# Marmousi2 Density Model
class Marmousi2_Density(TrueModel):
    def __init__(self):
        super().__init__(
            url='http://www.agl.uh.edu/downloads/density_marmousi-ii.segy.gz',
            output_filename='density_marmousi-ii.segy'
        )
