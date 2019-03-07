# Imports
import pandas as pd
import numpy as np
import tkinter as tk
import beams as b
import criteria as c
import gui


# Defines
IX_HEADER = "i_x"
TYPE = "designation"
DATA_SPREADSHEET = "beam_dimensions_properties.xlsx"
RELEVANT_SHEETS = ["WB", "WC", "UB", "UC"]


# Functions
def load_beams_from_spreadsheet(spreadsheet):
    beams = []
    sheets = pd.read_excel(spreadsheet, sheet_name=RELEVANT_SHEETS, header=0)
    for sheet in sheets:
        columns = sheets[sheet].columns
        sheet_np = sheets[sheet].values
        for i in range(np.size(sheet_np, 0)):
            beams.append(b.Beam(columns, sheet_np[i, :]))

    return beams


def add_desired_beam_type(desired_beam_types, desired_beam_type):
    if desired_beam_type not in desired_beam_types:
        desired_beam_types.append(desired_beam_type)

    return desired_beam_types


def remove_undesired_beam_type(desired_beam_types, undesired_beam_type):
    if undesired_beam_type in desired_beam_types:
        desired_beam_types.remove(undesired_beam_type)

    return desired_beam_types


def main():
    # Read in from spreadsheet
    beams = load_beams_from_spreadsheet(DATA_SPREADSHEET)

    desired_criteria = c.Criteria()

    # Create GUI window
    root = tk.Tk()
    root.title("Beam Selection Tool")
    window = gui.GUIWindow(beams, desired_criteria, master=root)
    window.mainloop()


if __name__ == '__main__':
    main()
