#-----------------------LIBRARIES--------------------------------
from matplotlib import pyplot as plt
plt.style.use('seaborn-v0_8-poster')

#----------------------------------------------------------------
#--------------------------PLOTTING------------------------------
def plot_peaks(data, x=(200,1100), y=(0,1)):
    """
    Plots the spectrum as a function of its intensity and the wavelength. If the
    peak finder and the half peak finder were already run, plots them with the
    "scatter" function.

    Parameters
    ----------
    data : pandas.core.frame.DataFrame
        The dataframe that contains the information about spectrum, peaks and
        half peaks.
    x : tuple, optional
        Limits the X-Axis to this interval, given in nanometers. The default
        is (200,1100).
    y : tuple, optional
        Limits the Y-Axis to this interval, given in intensity scale. The
        default is (0,1).
    """
    fig = plt.figure()
    ax1 = fig.subplots()
    ax1.plot(data["Wavelength"], data['Spectrum'], linewidth=1, color = 'blue', label='Spectrum')
    if "Halfpeaks" in data.columns:
        mask = data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
        ax1.scatter(data.loc[mask, "Wavelength"], data.loc[mask, "Halfpeaks"], s=60, marker='d', color = 'red', label='Half peaks' if mask.any() else '_nolegend_')
    if "Peaks" in data.columns:
        mask = data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        ax1.scatter(data.loc[mask, "Wavelength"], data.loc[mask, "Peaks"], s=60, marker='d', color = 'black', label='Peaks' if mask.any() else '_nolegend_')
    ax1.set_xlim(x[0],x[1])
    ax1.set_ylim(y[0],y[1])
    ax1.set_xlabel('Wavelength (nm)')
    ax1.set_ylabel('Intensity')
    ax1.legend()
    return plt.show()

def plot_derivatives(data, derivative1st, x=(200,1100), y=(0,1), ylim_deriv=0.3):
    """
    Plots the data and the first derivative in two subplots, which share the X-Axis.
    In the first subplot, the half peaks are scattered in three different formats,
    that represent "big", "small" and "noise" half peaks. In the second subplot, the
    position of the half peaks is represented with a vertical line.
    
    If the peak finder was already run, the peaks are also represented with black
    dots at the first subplot.

    Parameters
    ----------
    data : pandas.core.frame.DataFrame
        The dataframe that contains the information about spectrum, peaks and
        half peaks.
    derivative1st : np.ndarray shape (N-1, 2)
        Columns: [midpoint_wavelength, normalized_derivative].
        It is the first derivative, obtained with the halfpeak_finder function.
    x : tuple, optional
        Limits the X-Axis to this interval, given in nanometers. The default
        is (200,1100).
    y : tuple, optional
        Limits the Y-Axis of the first subplot to this interval, at the spectrum,
        given in intensity scale. The default is (0,1).
    ylim_deriv : tuple, optional
        Limits the Y-Axis of the second subplot, at the first derivative, between
        (-ylim_deriv, +ylim_deriv). The default is 0.3.
    """
    fig, axes = plt.subplots(2, 1, figsize=(16, 12), sharex=True)
    ax1 = axes[0]
    ax2 = axes[1]
    # -----
    ax1.plot(data["Wavelength"], data['Spectrum'], linewidth=1, color = 'blue', label='Spectrum')
    ax1.scatter(data["Wavelength"], data['Spectrum'], s=5, marker='d', color = 'blue')
    if "Halfpeaks" in data.columns:
        mask1 = (data["Category"] == 'big') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
        mask2 = (data["Category"] == 'small') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1]) 
        mask3 = (data["Category"] == 'noise') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1]) 
        count1 = mask1.sum()
        count2 = mask2.sum()
        count3 = mask3.sum()
        ax1.scatter(data.loc[mask1, "Wavelength"], data.loc[mask1, "Halfpeaks"], s=80, marker='d', color = 'm', label=f'Big Half Peaks ({count1})' if mask1.any() else '_nolegend_')
        ax1.scatter(data.loc[mask2, "Wavelength"], data.loc[mask2, "Halfpeaks"], s=80, marker='d', color = 'darkorange', label=f'Small Half Peaks ({count2})' if mask2.any() else '_nolegend_')
        ax1.scatter(data.loc[mask3, "Wavelength"], data.loc[mask3, "Halfpeaks"], s=60, marker='X', color = 'black', label=f'Noise Half Peaks ({count3})' if mask3.any() else '_nolegend_')
    if "Peaks" in data.columns:
        mask4 = data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        count4 = mask4.sum()
        ax1.scatter(data.loc[mask4, "Wavelength"], data.loc[mask4, "Peaks"], s=80, marker='d', color = 'black', label=f'Peaks ({count4})' if mask3.any() else '_nolegend_')
    ax1.set_ylim(y[0],y[1])
    ax1.set_xlim(x[0],x[1])
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=20)
    ax1.grid(axis="x")
    # -----
    ax2.hlines(0,x[0],x[1], linewidth=1, color='black')
    ax2.plot(derivative1st[:, 0], derivative1st[:, 1], linewidth=1, color='green', label="1st Derivative")
    if "Halfpeaks" in data.columns:
        mask5 = (data["Category"] == 'big') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1])
        mask6 = (data["Category"] == 'small') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1])
        mask7 = (data["Category"] == 'noise') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1])
        ax2.vlines(data.loc[mask5, "Wavelength"], -ylim_deriv, +ylim_deriv, linewidth=2, color = 'm', label='Half Peaks (big)' if mask5.any() else '_nolegend_')
        ax2.vlines(data.loc[mask6, "Wavelength"], -ylim_deriv, +ylim_deriv, linewidth=2, color = 'darkorange', label='Half Peaks (small)' if mask6.any() else '_nolegend_')
        ax2.vlines(data.loc[mask7, "Wavelength"], -ylim_deriv, +ylim_deriv, linewidth=2, color = 'black', label='Half Peaks (noise)' if mask7.any() else '_nolegend_')
    ax2.set_xlabel('Wavelength (nm)')
    ax2.set_ylim(-ylim_deriv,ylim_deriv)
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=20)
    ax2.grid(axis="x")
    # -----
    return plt.show()

def plot_peaks_per_category(data, category= 'all', x=(200,1100), y=(0,1)):
    """
    Plots the spectrum as a function of its intensity and the wavelength, and each
    peak and half peak as a function of its category. When specifying the category
    to 'halfpeaks', it is not a requirement to run the Peak Finder previously. Also,
    when specifying any peak category different from 'halfpeaks' (including 'all'),
    it is not needed to run the Half Peak Finder before.
    
    Raises
    ------
    NameError
        The category must be one of the following ones: 'all', 'clearly_visible',
        'visible', 'small', 'noise', 'halfpeaks'.

    Parameters
    ----------
    data : pandas.core.frame.DataFrame
        The dataframe that contains the information about spectrum, peaks and
        half peaks.
    category : str, optional
        It is the category that the user wants to plot. If 'all', every peak and
        half peak will be represented in different colors. The default is 'all'.
    x : tuple, optional
        Limits the X-Axis to this interval, given in nanometers. The default
        is (200,1100).
    y : tuple, optional
        Limits the Y-Axis to this interval, given in intensity scale. The
        default is (0,1).
    """
    if category not in ["all", "clearly_visible", "visible", "small", "noise", "halfpeaks"]:
        raise NameError("The category must be one of the following ones: 'all', 'clearly_visible', 'visible', 'small', 'noise', 'halfpeaks'")
    farbes={'clearly_visible':"red",
            'visible':"blue",
            'small':"green",
            'noise':"grey",
            'big_halfpeak':"m",
            'small_halfpeak':"darkorange",
            'noise_halfpeak':"grey"}
    fig = plt.figure()
    ax1 = fig.subplots()
    ax1.plot(data["Wavelength"], data['Spectrum'], linewidth=1, color = 'black', label='Spectrum')
    if category!='all' and category!='halfpeaks':
        mask = (data["Category"] == category) & data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        count = mask.sum()
        ax1.scatter(data.loc[mask, "Wavelength"], data.loc[mask, "Peaks"], s=60, marker='d',
                    color=farbes[category], label=f"{category.replace('_', ' ').title()} ({count})" if mask.any() else '_nolegend_')
    elif category=='halfpeaks':
        mask = (data["Category"] == 'big') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
        count = mask.sum()
        ax1.scatter(data.loc[mask, "Wavelength"], data.loc[mask, "Halfpeaks"],s=60, marker='d',
                    color = farbes['big_halfpeak'], label=f'Big Half peaks ({count})' if mask.any() else '_nolegend_')
        mask = (data["Category"] == 'small') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
        count = mask.sum()
        ax1.scatter(data.loc[mask, "Wavelength"], data.loc[mask, "Halfpeaks"],s=60, marker='d',
                    color = farbes['small_halfpeak'], label=f'Small Half Peaks ({count})' if mask.any() else '_nolegend_')
        mask = (data["Category"] == 'noise') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
        count = mask.sum()
        ax1.scatter(data.loc[mask, "Wavelength"], data.loc[mask, "Halfpeaks"],s=20, marker='d',
                    color = farbes['noise_halfpeak'], label=f'Noise HP ({count})' if mask.any() else '_nolegend_')
    else:
        mask1 = (data["Category"] == 'clearly_visible') & data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        mask2 = (data["Category"] == 'visible') & data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        mask3 = (data["Category"] == 'small') & data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        mask4 = (data["Category"] == 'noise') & data["Peaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Peaks"].between(y[0], y[1])
        count1 = mask1.sum()
        count2 = mask2.sum()
        count3 = mask3.sum()
        count4 = mask4.sum()
        ax1.scatter(data.loc[mask4, "Wavelength"], data.loc[mask4, "Peaks"], s=20, marker='d', color=farbes['noise'], label=f"Noise ({count4})" if mask4.any() else '_nolegend_')
        ax1.scatter(data.loc[mask3, "Wavelength"], data.loc[mask3, "Peaks"], s=60, marker='d', color=farbes['small'], label=f"Small ({count3})" if mask3.any() else '_nolegend_')
        ax1.scatter(data.loc[mask2, "Wavelength"], data.loc[mask2, "Peaks"], s=60, marker='d', color=farbes['visible'], label=f"Visible ({count2})" if mask2.any() else '_nolegend_')
        ax1.scatter(data.loc[mask1, "Wavelength"], data.loc[mask1, "Peaks"], s=60, marker='d', color=farbes['clearly_visible'], label=f"Clearly Visible ({count1})" if mask1.any() else '_nolegend_')
        if "Halfpeaks" in data.columns:
            mask5 = (data["Category"] == 'big') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
            mask6 = (data["Category"] == 'small') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
            mask7 = (data["Category"] == 'noise') & data["Halfpeaks"].notna() & data["Wavelength"].between(x[0], x[1]) & data["Halfpeaks"].between(y[0], y[1])
            count5 = mask5.sum()
            count6 = mask6.sum()
            count7 = mask7.sum()
            ax1.scatter(data.loc[mask7, "Wavelength"], data.loc[mask7, "Halfpeaks"], s=20, marker='d', color = farbes['noise_halfpeak'], label=f'Noise HP ({count7})' if mask7.any() else '_nolegend_')
            ax1.scatter(data.loc[mask5, "Wavelength"], data.loc[mask5, "Halfpeaks"], s=60, marker='d', color = farbes['big_halfpeak'], label=f'Big Half Peaks ({count5})' if mask5.any() else '_nolegend_')
            ax1.scatter(data.loc[mask6, "Wavelength"], data.loc[mask6, "Halfpeaks"], s=60, marker='d', color = farbes['small_halfpeak'], label=f'Small Half Peaks ({count6})' if mask6.any() else '_nolegend_')
    ax1.set_xlim(x[0],x[1])
    ax1.set_ylim(y[0],y[1])
    ax1.set_xlabel('Wavelength (nm)')
    ax1.set_ylabel('Intensity')
    ax1.legend()
    return plt.show()

def plot_troughpoints(data, x=(200,1100), y=(0,1)):
    """
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    x : TYPE, optional
        DESCRIPTION. The default is (200,1100).
    y : TYPE, optional
        DESCRIPTION. The default is (0,1).
    """
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(data["Wavelength"], data['Spectrum'], linewidth=1, color = 'blue', label='Spectrum')
    ax.plot(data["Wavelength"], data['Continuum'], linestyle='--', linewidth=2, color = 'green', label='Continuum')
    ax.scatter(data["Wavelength"], data['trough'], s = 30, marker = 'd', color = 'black', label='Trough Points')
    ax.scatter(data["Wavelength"], data['trough_filtered'], s = 60, marker = 'd', color = 'red', label='Non-Filtered Troughs')
    plt.xlim(x[0],x[1])
    plt.ylim(y[0],y[1])
    plt.xlabel('Wavelength')
    plt.ylabel('Intensity')
    plt.legend()
    return plt.show()

def plot_continuum(data, x=(200,1100), y=(0,1)):
    """
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    x : TYPE, optional
        DESCRIPTION. The default is (200,1100).
    y : TYPE, optional
        DESCRIPTION. The default is (0,1).
    """
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(data["Wavelength"], data['Spectrum2'], linewidth=1, color = 'blue', label='New Spectrum')
    ax.plot(data["Wavelength"], data['Continuum'], linestyle='--', linewidth=2, color = 'red', label='Continuum')
    plt.xlim(x[0],x[1])
    plt.ylim(y[0],y[1])
    plt.xlabel('Wavelength')
    plt.ylabel('Intensity')
    plt.legend()
    return plt.show()