# Imports
import numpy as np

# Defines
WELDED_BEAM = "wb"
WELDED_COLUMN = "wc"
UNIVERSAL_BEAM = "ub"
UNIVERSAL_COLUMN = "uc"
TAPERED_FLANGE_BEAM = "tfb"
PARALLEL_FLANGE_CHANNEL = "pfc"
UNIVERSAL_BEARING_PILE = "ubp"
EQUAL_ANGLE = "ea"
UNSPECIFIED = "unspecified"

TYPE = "designation"


class ColumnValueLengthMismatchError(Exception):
    """Raised when the number of column headers do not match the number of values for a given beam"""
    pass


class Beam:
    def __init__(self, columns, values):
        self.columns = columns
        self.value_dictionary = {}
        self.populate_dictionary(values)

    def populate_dictionary(self, values):
        if len(self.columns) != np.size(values):
            raise ColumnValueLengthMismatchError

        for i in range(len(self.columns)):
            self.value_dictionary[self.columns[i]] = "%s" % (values[i])

    def get_value(self, column_header):
        return self.value_dictionary[column_header]

    def get_type(self):
        designation = self.value_dictionary[TYPE].lower()
        if WELDED_BEAM in designation:
            return WELDED_BEAM
        elif WELDED_COLUMN in designation:
            return WELDED_COLUMN
        elif UNIVERSAL_BEAM in designation:
            return UNIVERSAL_BEAM
        elif UNIVERSAL_COLUMN in designation:
            return UNIVERSAL_COLUMN
        elif TAPERED_FLANGE_BEAM in designation:
            return TAPERED_FLANGE_BEAM
        elif PARALLEL_FLANGE_CHANNEL in designation:
            return PARALLEL_FLANGE_CHANNEL
        elif UNIVERSAL_BEARING_PILE in designation:
            return UNIVERSAL_BEARING_PILE
        elif EQUAL_ANGLE in designation:
            return EQUAL_ANGLE
        else:
            return UNSPECIFIED

    def __str__(self):
        string = "| "
        for column in self.columns:
            string += ("%s: %s | " % (column.upper(), self.get_value(column)))

        return string.rstrip()


class DesiredBeamTypes:
    def __init__(self):
        self.desired_beam_types = []

    def add_desired_beam_type(self, desired_beam_type):
        self.desired_beam_types.append(desired_beam_type)

    def remove_undesired_beam_type(self, undesired_beam_type):
        self.desired_beam_types.remove(undesired_beam_type)

    def __str__(self):
        return str(self.desired_beam_types)
