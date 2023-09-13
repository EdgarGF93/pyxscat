

import numpy as np



# @log_info
def raw_integration_azimuthal(
    self, 
    data=None,
    norm_factor=1.0,
    dict_integration=dict(),
) -> np.array:
    """
    Performs an azimuthal integration using the pygix-pyFAI engine

    Parameters:
    data(np.array) : data to be integrated
    norm_factor(float) : this value will be used by the pygix-pyFAI integration engine
    dict_integration(dict) : dictionary with key-values that will be read by the pygix-pyFAI integration engine
    
    Returns:
    np.array : result of the integration
    """
    # Take the array of intensity
    if (data is None) or (not dict_integration):
        return
    p0_range=dict_integration['Radial_range']
    p1_range=dict_integration['Azimuth_range']
    unit=dict_integration['Unit']
    npt=self.calculate_bins(
                radial_range=p0_range,
                unit=unit,
    )

    # Do the integration with pygix/pyFAI
    try:
        # logger.info(f"Trying azimuthal integration with: bins={npt}, p0_range={p0_range}, p1_range={p1_range}, unit={unit}")
        y_vector, x_vector = self.integrate_1d(
            process='sector',
            data=data,
            npt=npt,
            p0_range=p0_range,
            p1_range=p1_range,
            unit=unit,
            normalization_factor=float(norm_factor),
            polarization_factor=POLARIZATION_FACTOR,
        )
        # logger.info("Integration performed.")
    except:
        pass
        # logger.info("Error during azimuthal integration.")

    return np.array([x_vector, y_vector])