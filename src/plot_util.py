import matplotlib.pyplot as plt

def plot_and_scatter(ax: plt.Axes, xdata, ydata, **kwargs):
    label = None
    if 'label' in kwargs.keys():
       label = kwargs['label']
       kwargs.pop('label')
       
    ax.plot(xdata, ydata, **kwargs)
    ax.scatter(xdata, ydata, label=label, **kwargs)
 