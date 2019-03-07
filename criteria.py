# Imports

# Defines
EQUAL_TO = "1"
GREATER_THAN = "2"
LESS_THAN = "4"
NOT_EQUAL_TO = "6"
IN = "8"
TYPE = "9"


class Criteria:
    def __init__(self):
        self.conditions = []

    def add_condition(self, condition):
        self.conditions.append(condition)

    def remove_condition(self, condition):
        unwanted_condition_string = str(condition)
        self.remove_condition_given_string(unwanted_condition_string)

    def remove_condition_given_string(self, unwanted_condition_string):
        i = 0
        while i < len(self.conditions):
            if str(self.conditions[i]) == unwanted_condition_string:
                del self.conditions[i]
                break
            i += 1


    def __str__(self):
        string = "This criteria has the following conditions:\n"
        for condition in self.conditions:
            string += "  - " + str(condition) + "\n"

        return string


class Condition:
    def __init__(self, column, condition, value):
        self.column = column
        self.condition = condition
        self.value = value

    def __str__(self):
        string = self.column + " "
        if self.condition == GREATER_THAN:
            string += ">"
        elif self.condition == LESS_THAN:
            string += "<"
        elif self.condition == GREATER_THAN + EQUAL_TO:
            string += ">="
        elif self.condition == LESS_THAN + EQUAL_TO:
            string += "<="
        elif self.condition == EQUAL_TO:
            string += "="
        elif self.condition == NOT_EQUAL_TO:
            string += "!="
        elif self.condition == IN:
            string += "in"
        elif self.condition == TYPE:
            string += "has type in"
        string += " "
        string += str(self.value)

        return string


class CriteriaEvaluator:
    def __init__(self):
        pass

    def evaluate_criteria(self, criteria, beam):
        check = False
        for condition in criteria.conditions:
            if condition.column in beam.columns:
                beam_value = beam.get_value(condition.column)
                if condition.condition == EQUAL_TO:
                    check = (beam_value == condition.value)
                elif condition.condition == NOT_EQUAL_TO:
                    check = (beam_value != condition.value)
                elif condition.condition == GREATER_THAN:
                    check = float(beam_value) > float(condition.value)
                elif condition.condition == LESS_THAN:
                    check = float(beam_value) < float(condition.value)
                elif condition.condition == (GREATER_THAN + EQUAL_TO):
                    check = float(beam_value) >= float(condition.value)
                elif condition.condition == (LESS_THAN + EQUAL_TO):
                    check = float(beam_value) <= float(condition.value)
                elif condition.condition == IN:
                    check = beam_value in condition.value
                elif condition.condition == TYPE:
                    check = beam.get_type() in condition.value
            else:
                print("Beam: %s\ndoes not specify a value for %s" % (beam, condition.column))

            if not check:
                return False

        return True
