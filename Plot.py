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

# Usage example
if __name__ == "__main__":
    # Dummy data for demonstration
    data = np.random.rand(100, 200)

    # TrueModelPlot instance
    true_model_plot = TrueModelPlot(data)
    
    # Plotting the True Model as a standalone plot
    true_model_plot.plot_model(title="True Model Plot", cmap='seismic')

    # Plotting with subplots (2x2 layout)
    additional_data = [np.random.rand(100, 200), np.random.rand(100, 200), None]  # Adding dummy data
    true_model_plot.plot_model_with_subplots(other_data=additional_data)
