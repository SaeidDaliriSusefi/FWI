import numpy as np
import matplotlib.pyplot as plt

class PlotModel:
    def __init__(self, vp_data, max_distance_km, max_depth_km, plot_title="Selected Model Plot"):
        self.vp_data = vp_data
        self.max_distance_km = max_distance_km
        self.max_depth_km = max_depth_km
        self.plot_title = plot_title

    def plot_model_with_subplots(self, fig_size=(10, 8)):
        if self.vp_data is not None:
            # Check if data is velocity or density and adjust accordingly
            if 'density' in self.plot_title.lower():
                data = self.vp_data  # Assuming density data is already in kg/m³
                colorbar_label = 'Density (kg/m³)'
            else:
                data = self.vp_data / 1000  # Convert to km/s for velocity model (assuming input data is in m/s)
                colorbar_label = 'Velocity (km/s)'

            fig, axs = plt.subplots(2, 2, figsize=fig_size)

            # Plotting the selected model in the first subplot
            cax1 = axs[0, 0].imshow(data, cmap='jet', aspect='auto', origin='upper',
                                    extent=[0, self.max_distance_km, self.max_depth_km, 0])
            cbar1 = fig.colorbar(cax1, ax=axs[0, 0], orientation='vertical', pad=0.02)
            cbar1.set_label(colorbar_label, fontsize=10)
            cbar1.formatter.set_scientific(False)
            cbar1.update_ticks()

            axs[0, 0].set_title(self.plot_title, fontsize=14, loc='center', pad=10)
            axs[0, 0].set_xlabel('Distance (Km)', fontsize=12, labelpad=10)
            axs[0, 0].set_ylabel('Depth (Km)', fontsize=12, labelpad=10)

            # Leave the other subplots available for further customization or visualizations
            axs[0, 1].set_title('Subplot 2 (Empty)', fontsize=14)
            axs[1, 0].set_title('Subplot 3 (Empty)', fontsize=14)
            axs[1, 1].set_title('Subplot 4 (Empty)', fontsize=14)

            # Adjust layout and show plot
            plt.tight_layout()
            plt.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.1)
            plt.show()
