# Imports
import tkinter as tk
from tkinter import ttk
import criteria as c
import beams as b

# Defines
STATE_DISABLED = "disabled"
STATE_ENABLED = "!disabled"
STATE_READONLY = "readonly"
NO_RESULT_MESSAGE = "No beams found that match the given criteria"

# Classes


class GUIWindow(tk.Frame):
    def __init__(self, beam_list, criteria, master=None):
        super().__init__(master)
        self.master = master
        self.evaluator = c.CriteriaEvaluator()
        self.criteria = c.Criteria()
        self.mainframe = ttk.Frame(self.master, padding="5 5 5 5")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), columnspan=4, rowspan=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainframe.pack(pady=10, padx=10)
        self.beams = beam_list
        self.criteria = criteria
        self.create_widgets()

    def create_widgets(self):
        condition_label_row = 0
        self.condition_label = ttk.Label(self.mainframe, text="Condition:")
        self.condition_label.grid(column=0, row=condition_label_row)

        condition_option_row = condition_label_row + 1
        self.column_frame = ttk.Frame(self.mainframe)
        self.column_frame.grid(row=condition_option_row, column=0)
        self.column_label = ttk.Label(self.column_frame, text="Column")
        self.column_label.grid(column=0, row=0)
        self.column_value = tk.StringVar()
        self.column_combobox = ttk.Combobox(self.column_frame, textvariable=self.column_value)
        self.column_combobox.grid(column=0, row=1)
        self.column_combobox['values'] = self.get_all_beam_columns()
        self.column_combobox["state"] = STATE_READONLY

        self.comparison_frame = ttk.Frame(self.mainframe)
        self.comparison_frame.grid(row=condition_option_row, column=1)
        self.comparison_label = ttk.Label(self.comparison_frame, text="Comparison")
        self.comparison_label.grid(column=0, row=0)
        self.comparison_value = tk.StringVar()
        self.comparison_combobox = ttk.Combobox(self.comparison_frame, textvariable=self.comparison_value)
        self.comparison_combobox.grid(column=0, row=1)
        self.comparison_combobox['values'] = ["=", "!=", "<", ">", "<=", ">="]
        self.comparison_combobox["state"] = STATE_READONLY

        self.condition_value_frame = ttk.Frame(self.mainframe)
        self.condition_value_frame.grid(row=condition_option_row, column=2)
        self.condition_value_label = ttk.Label(self.condition_value_frame, text="Value")
        self.condition_value_label.grid(column=0, row=0)
        self.condition_value = tk.StringVar()
        self.condition_value_entry = ttk.Entry(self.condition_value_frame, textvariable=self.condition_value)
        self.condition_value_entry.grid(column=0, row=1, sticky=(tk.S, tk.E))

        self.condition_add_button = ttk.Button(self.mainframe, text="Add", command=self.add_constraint)
        self.condition_add_button.grid(column=3, row=condition_option_row, sticky=tk.S)
        self.condition_remove_button = ttk.Button(self.mainframe,
                                                  text="Remove",
                                                  command=self.remove_constraint)
        self.condition_remove_button.grid(column=4, row=condition_option_row, sticky=tk.S)
        self.condition_remove_button["state"] = STATE_DISABLED

        condition_listbox_row = condition_option_row + 2
        self.conditions_listbox = tk.Listbox(self.mainframe, height=5)
        self.conditions_listbox.grid(column=0, row=condition_listbox_row, sticky=(tk.W, tk.E), columnspan=5)
        self.conditions_y_scrollbar = ttk.Scrollbar(self.mainframe,
                                                    orient=tk.VERTICAL,
                                                    command=self.conditions_listbox.yview)
        self.conditions_y_scrollbar.grid(column=5, row=condition_listbox_row, rowspan=4, sticky=(tk.N, tk.S, tk.E))
        self.conditions_listbox["yscrollcommand"] = self.conditions_y_scrollbar.set
        self.conditions_x_scrollbar = ttk.Scrollbar(self.mainframe,
                                                 orient=tk.HORIZONTAL,
                                                 command=self.conditions_listbox.xview)
        self.conditions_x_scrollbar.grid(column=0, row=condition_listbox_row+5, columnspan=5, sticky=(tk.S, tk.W, tk.E))
        self.conditions_listbox["xscrollcommand"] = self.conditions_x_scrollbar.set
        self.selected_condition_index = 0
        self.conditions_listbox.bind("<<ListboxSelect>>", self.update_selected_condition)
        self.conditions_listbox.bind("<Delete>", self.remove_constraint)

        types_row = condition_listbox_row + 6
        self.types_label = ttk.Label(self.mainframe, text="Types:")
        self.types_label.grid(column=0, row=types_row)
        self.types_frame = ttk.Frame(self.mainframe)
        self.types_frame.grid(column=0, row=types_row+1, columnspan=4, sticky=(tk.W, tk.E))

        self.wb_var = tk.IntVar()
        self.wb_var.set(1)
        self.type_wb_checkbox = ttk.Checkbutton(self.types_frame, text="Welded Beam", variable=self.wb_var)
        self.type_wb_checkbox.grid(column=0, row=0, sticky=(tk.N, tk.W))
        self.wc_var = tk.IntVar()
        self.wc_var.set(1)
        self.type_wc_checkbox = ttk.Checkbutton(self.types_frame, text="Welded Column", variable=self.wc_var)
        self.type_wc_checkbox.grid(column=0, row=1, sticky=(tk.N, tk.W))
        self.ub_var = tk.IntVar()
        self.ub_var.set(1)
        self.type_ub_checkbox = ttk.Checkbutton(self.types_frame, text="Universal Beam", variable=self.ub_var)
        self.type_ub_checkbox.grid(column=2, row=0, sticky=(tk.N, tk.W))
        self.uc_var = tk.IntVar()
        self.uc_var.set(1)
        self.type_uc_checkbox = ttk.Checkbutton(self.types_frame, text="Universal Column", variable=self.uc_var)
        self.type_uc_checkbox.grid(column=2, row=1, sticky=(tk.N, tk.W))

        evaluate_row = types_row + 3
        self.evaluate_button = ttk.Button(self.mainframe, text="Find beams", command=self.evaluate)
        self.evaluate_button.grid(column=0, row=evaluate_row, pady="10 0")

        results_listbox_row = evaluate_row + 1
        self.results_listbox = tk.Listbox(self.mainframe, height=5)
        self.results_listbox.grid(column=0, row=results_listbox_row, sticky=(tk.W, tk.E), columnspan=5)
        self.results_y_scrollbar = ttk.Scrollbar(self.mainframe,
                                                    orient=tk.VERTICAL,
                                                    command=self.results_listbox.yview)
        self.results_y_scrollbar.grid(column=5, row=results_listbox_row, rowspan=4, sticky=(tk.N, tk.S, tk.E))
        self.results_listbox["yscrollcommand"] = self.results_y_scrollbar.set
        self.results_x_scrollbar = ttk.Scrollbar(self.mainframe,
                                                 orient=tk.HORIZONTAL,
                                                 command=self.results_listbox.xview)
        self.results_x_scrollbar.grid(column=0, row=results_listbox_row+5, columnspan=5, sticky=(tk.S, tk.W, tk.E))
        self.results_listbox["xscrollcommand"] = self.results_x_scrollbar.set

    def add_constraint(self):
        comparison = self.get_comparison_value(self.comparison_value.get())
        new_condition = c.Condition(self.column_value.get(), comparison, self.condition_value.get())
        self.criteria.add_condition(new_condition)
        self.conditions_listbox.insert("end", str(new_condition))
        self.column_value.set("")
        self.comparison_value.set("")
        self.condition_value.set("")

    def remove_constraint(self, *args):
        for index in self.conditions_listbox.curselection():
            unwanted_condition_string = str(self.conditions_listbox.get(index))
            self.criteria.remove_condition_given_string(unwanted_condition_string)
            self.conditions_listbox.delete(index)

        self.condition_remove_button["state"] = STATE_DISABLED

    def get_comparison_value(self, comparison_value):
        if comparison_value == "=":
            comparison = c.EQUAL_TO
        elif comparison_value == "!=":
            comparison = c.NOT_EQUAL_TO
        elif comparison_value == "<":
            comparison = c.LESS_THAN
        elif comparison_value == ">":
            comparison = c.GREATER_THAN
        elif comparison_value == "<=":
            comparison = c.LESS_THAN + c.EQUAL_TO
        elif comparison_value == ">=":
            comparison = c.GREATER_THAN + c.EQUAL_TO
        else:
            comparison = c.TYPE

        return comparison

    def evaluate(self):
        type_condition = self.create_type_condition()
        type_criteria = c.Criteria()
        type_criteria.add_condition(type_condition)
        self.results_listbox.delete(0, "end")
        for beam in self.beams:
            if self.evaluator.evaluate_criteria(type_criteria, beam):
                if self.evaluator.evaluate_criteria(self.criteria, beam):
                    self.results_listbox.insert("end", str(beam))

        if self.results_listbox.size() < 1:
            self.results_listbox.insert("end", NO_RESULT_MESSAGE)

    def update_selected_condition(self, *args):
        if len(self.conditions_listbox.curselection()) < 1:
            self.condition_remove_button["state"] = STATE_DISABLED
        else:
            self.condition_remove_button["state"] = STATE_ENABLED

    def create_type_condition(self):
        types = []
        if self.wb_var.get() == 1:
            types.append(b.WELDED_BEAM)
        if self.wc_var.get() == 1:
            types.append(b.WELDED_COLUMN)
        if self.ub_var.get() == 1:
            types.append(b.UNIVERSAL_BEAM)
        if self.uc_var.get() == 1:
            types.append(b.UNIVERSAL_COLUMN)

        return c.Condition(b.TYPE, c.TYPE, types)

    def get_all_beam_columns(self):
        columns = []
        types = []
        for beam in self.beams:
            if not beam.get_type() in types:
                types.append(beam.get_type())
                for column in beam.columns:
                    if column not in columns:
                        columns.append(column)

        return tuple(columns)
