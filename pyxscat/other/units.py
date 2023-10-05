from numpy import pi

UNITS_Q = ('q_nm^-1', 'q_A^-1')
UNITS_THETA = ('2th_deg', '2th_rad')
QNM_ALIAS = ('q_nm^-1', 'q_nm^-1', 'nm', 'nm-1', 'qnm', 'q_nm')
QA_ALIAS = ('q_A^-1', 'q_A', 'q_a^-1', 'q_a^-1', 'a', 'a-1', 'qa', 'q_a')
RAD_ALIAS = ('2th_rad', 'rad', '2thrad', 'thrad', 'tth_rad', 'tthrad')
DEG_ALIAS = ('2th_deg', 'deg', '2thdeg', 'thdeg', 'tth_deg', 'tthdeg')

DICT_UNIT_ALIAS = {
    QNM_ALIAS : 'q_nm^-1',
    QA_ALIAS : 'q_A^-1',
    RAD_ALIAS : '2th_rad',
    DEG_ALIAS : '2th_deg',
}

CAKE_INTEGRATIONS = ("azimuthal", "radial")
BOX_INTEGRATIONS = ("horizontal", "vertical")

def get_pyfai_unit(unit='nm'):
    """
        Identify the correct unit for pyFAI from alias
    """
    unit = unit.lower()
    for alias, correct_unit in DICT_UNIT_ALIAS.items():
        if unit in alias:
            return correct_unit


# DEFAULT VALUES FOR PLOTTING
DICT_UNIT_PLOTS = {
    'q_nm^-1' : {
        'X_LABEL' : r'$q_{r}$ $(nm^{-1})$',
        'Y_LABEL' : r'$q_{z}$ $(nm^{-1})$',
        'X_LIMS' : [-20,20],
        'Y_LIMS' : [-20,20],
        'X_TICKS' : [-20,-10,0,10,20],
        'Y_TICKS' : [-20,-10,0,10,20],
        'SCALE' : 100,
    },

    'q_A^-1' : {
        'X_LABEL' : '$q_{r}$ $(\u212b^{-1})$',
        'Y_LABEL' : '$q_{z}$ $(\u212b^{-1})$',
        'X_LIMS' : [-2,2],
        'Y_LIMS' : [-2,2],
        'X_TICKS' : [-2,-1,0,1,2],
        'Y_TICKS' : [-2,-1,0,1,2],
        'SCALE' : 10,
    },

    '2th_deg' : {
        'X_LABEL' : '2\u03b8 (\u00b0)',
        'Y_LABEL' : '\u03b1 (\u00b0)',
        'X_LIMS' : [-20,20],
        'Y_LIMS' : [-20,20],
        'X_TICKS' : [-20,-10,0,10,20],
        'Y_TICKS' : [-20,-10,0,10,20],
        'SCALE' : 180/pi,
    },

    '2th_rad' : {
        'X_LABEL' : '2\u03b8 (rad)',
        'Y_LABEL' : '\u03b1 (rad)',
        'X_LIMS' : [round(-pi / 10, 2), round(pi / 10, 2)],
        'Y_LIMS' : [round(-pi / 10, 2), round(pi / 10, 2)],
        'X_TICKS' : [round(-2*pi / 10, 2), round(-pi / 2, 2) , 0 , round(pi / 10, 2) , round(2*pi / 10, 2)],
        'Y_TICKS' : [round(-2*pi / 10, 2), round(-pi / 2, 2) , 0 , round(pi / 10, 2) , round(2*pi / 10, 2)],
        'SCALE' : 1,
    },
}
DICT_PLOT_DEFAULT = DICT_UNIT_PLOTS['q_nm^-1']