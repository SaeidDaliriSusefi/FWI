import matplotlib.pyplot as plt
import numpy as np

# Base class for plot models
class PlotModel:
    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        self.data = data

    def is_data_valid(self):
        return self.data is not None and self.data.size > 0

# Subclass for True Model Plotting
class TrueModelPlot(PlotModel):
    def plot_model(self, title, cmap='viridis', save_as=None):
        """
        Plots the model data as a 2D heatmap.

        Parameters:
            title (str): The title of the plot.
            cmap (str): The colormap for the plot.
            save_as (str): Optional. The filename to save the plot.
        """
        if not self.is_data_valid():
            print("No data available to plot.")
            return

        plt.figure(figsize=(10, 6))
        plt.imshow(self.data, aspect='auto', cmap=cmap, origin='lower')
        plt.colorbar(label='Value')
        plt.title(title)
        plt.xlabel('Distance (km)')
        plt.ylabel('Depth (km)')
        
        if save_as:
            plt.savefig(save_as, dpi=300, bbox_inches='tight')
        
        plt.show()

# Additional subclasses for other model types
class VelocityModelPlot(PlotModel):
    def __init__(self, data=None):
        super().__init__(data)

class DensityModelPlot(PlotModel):
    def __init__(self, data=None):
        super().__init__(data)

class CustomModelPlot(PlotModel):
    def __init__(self, data=None):
        super().__init__(data)
