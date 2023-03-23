import os
from os.path import join
# from .integration_form import Ui_IntegrationForm
from modules_qt.gui_widget_integration import GUIPyX_Widget_integrationform
import modules_qt.widget_methods.lineedit_methods as le
import modules_qt.widget_methods.listwidget_methods as lt
import modules_qt.widget_methods.combobox_methods as cb
from integration.integrator_methods import DIRECTORY_INTEGRATIONS




class IntegrationForm(GUIPyX_Widget_integrationform):

    def __init__(self):
        super(IntegrationForm, self).__init__()
        self.integrator = None
        self.init_callbacks()
        self.update_integration_dictionaries(
            list_dicts=self.get_dictionaries_integration()
        )
        
    def init_callbacks(self):
        """
            Activate the callbacks regarding the integration form
        """
        self.list_azrad.clicked.connect(
            lambda: self.activate_integration_form(
                name_dict=lt.click_values(
                    listwidget=self.list_azrad
                )[0]
            )
        )

        self.list_proj.clicked.connect(
            lambda: self.activate_integration_form(
                name_dict=lt.click_values(
                    listwidget=self.list_proj
                )[0]
            )
        )

        self.button_azrad_check.clicked.connect(
            lambda : (
            self.check_integration_azrad(),
            )
        )

        # Callback for add a new integration rad/azimut
        self.button_azrad_add.clicked.connect(
            lambda: self.add_new_integration(
                dict_setup=self.get_radaz_attributes()
            )           
        )
        
        # Callback for add a new integration projection
        self.button_proj_add.clicked.connect(
            lambda: self.add_new_integration(
                dict_setup=self.get_projection_attributes()
            )           
        )

        self.button_proj_check.clicked.connect(
            lambda : (
                self.check_integration_projs(),
            )
        )


    def get_radaz_attributes(self) -> dict:
        """
            Return a dictinary with all the attributes for the creation of a new setup
        """
        return {
            'Name':le.text(
                lineedit=self.lineedit_name_azrad
            ),
            'Type':cb.value(
                combobox=self.combobox_type_azrad
            ),
            'Suffix':le.text(
                lineedit=self.lineedit_suffix_azrad
            ),
            'Azimuth_range':[
                le.text(
                    lineedit=self.lineedit_minaz
                ),
                le.text(
                    lineedit=self.lineedit_maxaz
                ),
            ],
            'Radial_range':[
                le.text(
                    lineedit=self.lineedit_minrad
                ),
                le.text(
                    lineedit=self.lineedit_maxrad
                ),
            ],
            'Unit':cb.value(
                combobox=self.combobox_units_azrad
            ),

            'Bins_azimut':le.text(
                    lineedit=self.lineedit_azimuthal_bins
            ),
        }


    def get_projection_attributes(self) -> dict:
        """
            Return a dictinary with all the attributes for the creation of a new setup
        """
        return {
            'Name':le.text(
                lineedit=self.lineedit_name_proj,
            ),
            'Type':cb.value(
                combobox=self.combobox_direction_proj,
            ),
            'Suffix':le.text(
                lineedit=self.lineedit_suffix_proj,
            ),
            'Unit_input':cb.value(
                combobox=self.combobox_input_units,
            ),
            'Ip_range':[
                le.text(
                    lineedit=self.lineedit_minip,
                ),
                le.text(
                    lineedit=self.lineedit_maxip,
                ),
            ],
            'Oop_range':[
                le.text(
                    lineedit=self.lineedit_minoop,
                ),
                le.text(
                    lineedit=self.lineedit_maxoop,
                ),
            ],
            'Unit':cb.value(
                combobox=self.combobox_output_units,
            ),
        }

    def add_new_integration(self, dict_setup=dict()):
        """
            Introduce a new integration dictionary
        """
        import json
        with open(join(DIRECTORY_INTEGRATIONS, f"{dict_setup['Name']}.json"), 'w+') as fp:
            json.dump(dict_setup, fp)

        self.update_integration_dictionaries(
            list_dicts=self.get_dictionaries_integration()
        )


    def get_dictionaries_integration(self) -> list:
        """
            Return a list with the dictionaries of all the available integrations
        """
        import json
        list_dicts = []
        for file in os.listdir(DIRECTORY_INTEGRATIONS):
            if file.endswith('json'):
                with open(join(DIRECTORY_INTEGRATIONS, file), 'r') as fp:
                    list_dicts.append(
                        json.load(fp)
                    )
        return list_dicts

    def get_dict_integration(self, name=str()) -> dict:
        """
            Return a dictionary of integration giving a name
        """
        for d in self.get_dictionaries_integration():
            if name == d['Name']:
                return d
        return

    def update_integration_dictionaries(self, list_dicts=[]):
        """
            Feed the list_widget of the integration form with all the available dictionaries
        """

        # Feed each combobox with their respective dictionaries
        lt.insert_list(
            listwidget=self.list_azrad,
            item_list=[
                d['Name'] for d in list_dicts if d['Type'] in ('Azimuthal', 'Radial')
            ],
            reset=True,
        )

        lt.insert_list(
            listwidget=self.list_proj,
            item_list=[
                d['Name'] for d in list_dicts if d['Type'] in ('Horizontal', 'Vertical')
            ],
            reset=True,
        ),

    def activate_integration_form(self, name_dict=str()):
        """
            Updates the integration form with a dictionary
        """
        import json
        try:
            with open(join(DIRECTORY_INTEGRATIONS, f"{name_dict}.json"), 'r') as fp:
                dict_integration = json.load(fp)
        except:
            return

        if dict_integration['Type'] in ('Azimuthal', 'Radial'):
            le.substitute(
                lineedit=self.lineedit_name_azrad,
                new_text=dict_integration['Name'],
            )

            le.substitute(
                lineedit=self.lineedit_suffix_azrad,
                new_text=dict_integration['Suffix'],
            )

            le.substitute(
                lineedit=self.lineedit_minaz,
                new_text=dict_integration['Azimuth_range'][0],
            )

            le.substitute(
                lineedit=self.lineedit_maxaz,
                new_text=dict_integration['Azimuth_range'][1],
            )

            le.substitute(
                lineedit=self.lineedit_minrad,
                new_text=dict_integration['Radial_range'][0],
            )

            le.substitute(
                lineedit=self.lineedit_maxrad,
                new_text=dict_integration['Radial_range'][1],
            )

            cb.set_text(
                combobox=self.combobox_type_azrad,
                text=dict_integration['Type']
            )

            cb.set_text(
                combobox=self.combobox_units_azrad,
                text=dict_integration['Unit']
            )

            try:
                le.substitute(
                    lineedit=self.lineedit_azimuthal_bins,
                    new_text=dict_integration['Bins_azimut'],
                )
            except:
                pass
    
        elif dict_integration['Type'] in ('Horizontal', 'Vertical'):
            le.substitute(
                lineedit=self.lineedit_name_proj,
                new_text=dict_integration['Name'],
            )

            le.substitute(
                lineedit=self.lineedit_suffix_proj,
                new_text=dict_integration['Suffix'],
            )

            cb.set_text(
                combobox=self.combobox_direction_proj,
                text=dict_integration['Type']
            )

            cb.set_text(
                combobox=self.combobox_input_units,
                text=dict_integration['Unit_input']
            )

            le.substitute(
                lineedit=self.lineedit_minip,
                new_text=dict_integration['Ip_range'][0],
            )

            le.substitute(
                lineedit=self.lineedit_maxip,
                new_text=dict_integration['Ip_range'][1],
            )

            le.substitute(
                lineedit=self.lineedit_minoop,
                new_text=dict_integration['Oop_range'][0],
            )

            le.substitute(
                lineedit=self.lineedit_maxoop,
                new_text=dict_integration['Oop_range'][1],
            )

            cb.set_text(
                combobox=self.combobox_output_units,
                text=dict_integration['Unit'],
            )

        else:
            return

    def check_integration_azrad(self):
        """
            Updates the graph to check the shape of the integration (radial or azimuthal)
        """
        if self.integrator:
            try:
                self.integrator.check_integration(
                    dict_integration=self.get_dict_integration(
                        name=lt.click_values(
                            listwidget=self.list_azrad
                        )[0]
                    ),
                )
            except:
                return
        else:
            return

    def check_integration_projs(self):
        """
            Updates the graph to check the shape of the integration (projection)
        """
        if self.integrator:
            try:
                self.integrator.check_integration(
                    dict_integration=self.get_dict_integration(
                        name=lt.click_values(
                            listwidget=self.list_proj
                        )[0]
                    ),
                )
            except:
                return
        else:
            return