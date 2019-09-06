#import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

def out_plot(filename, outputdata, dt, rxnumber, rxcomponent):
    """Creates a plot (with matplotlib) of the B-scan.

    Args:
        filename (string): Filename (including path) of output file.
        outputdata (array): Array of A-scans, i.e. B-scan data.
        dt (float): Temporal resolution of the model.
        rxnumber (int): Receiver output number.
        rxcomponent (str): Receiver output field/current component.

    Returns:
        plt (object): matplotlib plot object.
    """
    
    (path, filename) = os.path.split(filename)
    
    fig = plt.figure(num=filename + ' - rx' + str(rxnumber), figsize=(20, 10), facecolor='w', edgecolor='w')
    plt.imshow(outputdata, extent=[0, outputdata.shape[1], outputdata.shape[0] * dt, 0], interpolation='nearest', aspect='auto', cmap='seismic', vmin=-np.amax(np.abs(outputdata)), vmax=np.amax(np.abs(outputdata)))
    plt.xlabel('Trace number')
    plt.ylabel('Time [s]')
    plt.grid()
    cb = plt.colorbar()
    if 'E' in rxcomponent:
        cb.set_label('Field strength [V/m]')
    elif 'H' in rxcomponent:
        cb.set_label('Field strength [A/m]')
    elif 'I' in rxcomponent:
        cb.set_label('Current [A]')
    fig.show()
#    return fig

