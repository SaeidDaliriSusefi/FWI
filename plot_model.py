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
            # Convert to km/s for velocity model (assuming input data is in m/s)
            vp_km_s = self.vp_data / 1000

            fig, axs = plt.subplots(2, 2, figsize=fig_size)

            # Plotting the selected model in the first subplot
            cax1 = axs[0, 0].imshow(vp_km_s, cmap='jet', aspect='auto', origin='upper',
                                    extent=[0, self.max_distance_km, self.max_depth_km, 0])
            cbar1 = fig.colorbar(cax1, ax=axs[0, 0], orientation='vertical', pad=0.02)
            cbar1.set_label('Velocity/Density (km/s or kg/m³)', fontsize=10)
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
