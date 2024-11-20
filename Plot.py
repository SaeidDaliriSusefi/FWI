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

# Subclass for plotting each model type separately
class TrueModelPlot(PlotModel):
    
    def plot_marmousi1_velocity(self, cmap='viridis', save_as=None):
        """
        Plots the Marmousi1 Velocity Model as a 2D heatmap.

        Parameters:
            cmap (str): The colormap for the plot.
            save_as (str): Optional. The filename to save the plot.
        """
        self._plot_model(title="Marmousi1 Velocity Model", cmap=cmap, save_as=save_as)

    def plot_marmousi1_density(self, cmap='plasma', save_as=None):
        """
        Plots the Marmousi1 Density Model as a 2D heatmap.

        Parameters:
            cmap (str): The colormap for the plot.
            save_as (str): Optional. The filename to save the plot.
        """
        self._plot_model(title="Marmousi1 Density Model", cmap=cmap, save_as=save_as)

    def plot_marmousi2_velocity(self, cmap='inferno', save_as=None):
        """
        Plots the Marmousi2 Velocity Model as a 2D heatmap.

        Parameters:
            cmap (str): The colormap for the plot.
            save_as (str): Optional. The filename to save the plot.
        """
        self._plot_model(title="Marmousi2 Velocity Model", cmap=cmap, save_as=save_as)

    def plot_marmousi2_density(self, cmap='magma', save_as=None):
        """
        Plots the Marmousi2 Density Model as a 2D heatmap.

        Parameters:
            cmap (str): The colormap for the plot.
            save_as (str): Optional. The filename to save the plot.
        """
        self._plot_model(title="Marmousi2 Density Model", cmap=cmap, save_as=save_as)

    def _plot_model(self, title, cmap='viridis', save_as=None):
        """
        Generic method to plot model data.

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

    def plot_model_with_subplots(self, other_data=None):
        """
        Creates a 2x2 subplot with the true model plotted in the first subplot.

        Parameters:
            other_data (list of numpy.ndarray): List containing data for the other subplots.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plotting the True Model in the first subplot
        if self.is_data_valid():
            ax = axes[0, 0]
            im = ax.imshow(self.data, aspect='auto', cmap='viridis', origin='lower')
            fig.colorbar(im, ax=ax, label='Value')
            ax.set_title("True Model")
            ax.set_xlabel('Distance (km)')
            ax.set_ylabel('Depth (km)')
        else:
            print("No data available to plot for the True Model.")

        # Plotting additional data in other subplots (if provided)
        if other_data:
            for idx, data in enumerate(other_data):
                if idx >= 3:  # We only have space for 3 additional subplots
                    break
                
                row, col = (idx + 1) // 2, (idx + 1) % 2
                ax = axes[row, col]
                
                if data is not None and data.size > 0:
                    im = ax.imshow(data, aspect='auto', cmap='plasma', origin='lower')
                    fig.colorbar(im, ax=ax, label='Value')
                    ax.set_title(f"Additional Data {idx + 1}")
                    ax.set_xlabel('Distance (km)')
                    ax.set_ylabel('Depth (km)')
                else:
                    ax.set_title(f"Additional Data {idx + 1}")
                    ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', fontsize=12)

        # Hide unused subplots if less than 3 additional datasets are provided
        if not other_data or len(other_data) < 3:
            for idx in range(len(other_data) if other_data else 0, 3):
                row, col = (idx + 1) // 2, (idx + 1) % 2
                axes[row, col].axis('off')

        plt.tight_layout()
        plt.show()
