import os
from os.path import join
from .fitting_form import Ui_FittingForm

import modules_qt.widget_methods.lineedit_methods as le
import modules_qt.widget_methods.listwidget_methods as lt
import modules_qt.widget_methods.combobox_methods as cb


DIRECTORY_FITTINGS = join(os.getcwd(), 'module_integrator', 'fitting_dictionaries')


class FittingForm(Ui_FittingForm):

    def __init__(self):
        super(FittingForm, self).__init__()
        self.setupUi(self)

        self.init_callbacks()

    def init_callbacks(self):
        """
            Activate the callbacks regarding the integration form
        """
        self.pushButton_add_fitting.clicked.connect(
            self.save_fitting_conditions
        )

        self.pushButton_startfit.clicked.connect(
            self.start_fitting
        )

        self.listWidget_fittings.clicked.connect(
            lambda: self.update_fitting_conditions(
                dict_fittings=self.get_dict_fitting()
            )
        )

        self.listWidget_files.clicked.connect(
            lambda: self.update_chart_fittings(
                list_files=lt.click_values(
                    listwidget=self.listWidget_files
                )
            )
        )


    def get_dict_fitting(self) -> dict:
        """
            Return the dictionary of integrations upon clicked fittings
        """
        pass

    def update_chart_fittings(self, list_files=[]):
        """
            Update the chart of fittings
        """
        pass

    def update_fitting_conditions(self, dict_fitting={}):
        """
            Update the lineedits with the dictionary with fittings conditions
        """
        pass

    def update_fitting_dictionaries(self, list_dicts=[]):
        """
            Updates the list of available fitting sets
        """
        pass

    def start_fitting(self):
        """
            Start all the fitting macro
        """
        pass

    def save_fitting_conditions(self, dict_fitting=dict()):
        """
            Save a json file with all the input fitting conditions
        """
        import json
        with open(join(DIRECTORY_FITTINGS, f"{dict_fitting['Name']}.json"), 'w+') as fp:
            json.dump(dict_fitting, fp)

        self.update_fitting_dictionaries(
            list_dicts=self.get_dict_fitting()
        )
