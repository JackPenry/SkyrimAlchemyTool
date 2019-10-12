import json
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from os import path


def main():
    alchemy_data = parse_json_file("alchemy")
    if not path.exists("data/ingredient_data.json"):
        init_ingredient_data(alchemy_data)
    ingredient_data = parse_json_file("ingredient")
    root = Tk()
    app = SkyrimAlchemyTool(root, alchemy_data, ingredient_data)
    root.mainloop()


def get_effect_name(data, ingredient_name=""):
    effect_name = []
    if ingredient_name:
        for ingredient in data["ingredient"]:
            if ingredient["name"] == ingredient_name:
                for index in range(0, 4):
                    effect_name.append(ingredient["effect"][index])
                break
    else:
        for effect in data["effect"]:
            effect_name.append(effect["name"])
    return effect_name


def get_ingredient_name(data, effect_name=""):
    ingredient_name = []
    if effect_name:
        for effect in data["effect"]:
            if effect["name"] == effect_name:
                for ingredient in effect["ingredient"]:
                    ingredient_name.append(ingredient["name"])
                break
    else:
        for ingredient in data["ingredient"]:
            ingredient_name.append(ingredient["name"])
    return ingredient_name


def init_ingredient_data(alchemy_data):
    ingredient_data = {"ingredient": []}
    for ingredient_name in get_ingredient_name(alchemy_data):
        effect_list = get_effect_name(alchemy_data, ingredient_name)
        ingredient_data["ingredient"].append({
            "name": ingredient_name,
            "effect": [
                {
                    "name": effect_list[0],
                    "learned": "False"
                },
                {
                    "name": effect_list[1],
                    "learned": "False"
                },
                {
                    "name": effect_list[2],
                    "learned": "False"
                },
                {
                    "name": effect_list[3],
                    "learned": "False"
                }
            ],
            "quantity": 0
        })
        write_ingredient_data(ingredient_data)


def write_ingredient_data(ingredient_data):
    with open("data/ingredient_data.json", "w") as outfile:
        outfile.write(json.dumps(ingredient_data, indent=4))


def parse_json_file(file):
    try:
        with open("data/{0}_data.json".format(file)) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", "Could not find {0}_data.json".format(file))
        exit(1)
    return data


class SkyrimAlchemyTool:
    def __init__(self, master, alchemy_data, ingredient_data):
        self.master = master
        self.master.title("Skyrim Alchemy Tool")
        self.master.resizable(False, False)
        self.alchemy_data = alchemy_data
        self.ingredient_data = ingredient_data

        ttk.Style().configure("TFrame", background="#dcdcdc")
        ttk.Style().configure("TRadiobutton", background="#dcdcdc")
        ttk.Style().configure("TLabel", background="#dcdcdc")
        ttk.Style().configure("TLabelframe", background="#dcdcdc")

        self.notebook = ttk.Notebook(master, height=500, width=550)
        self.notebook.pack()

        self.potion_creation = ttk.Frame(self.notebook)
        # self.notebook.add(self.framePotionCreation, text="Potion Creation Tool")

        self.inventory = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory, text="Inventory")
        self.inventory_listbox = Listbox(self.inventory, activestyle="none", height=29, width=25)
        self.inventory_listbox.place(x=10, y=15)
        for index, ingredient in enumerate(get_ingredient_name(self.alchemy_data)):
            self.inventory_listbox.insert(index, ingredient)
        self.inventory_labelframe = LabelFrame(self.inventory, bg="#dcdcdc", height=300, width=350)
        self.inventory_listbox.bind("<<ListboxSelect>>", self.on_listbox_selected)
        self.unlearned_effect_listbox = Listbox(self.inventory_labelframe, activestyle="none", height=4, width=25)
        self.learned_effect_listbox = Listbox(self.inventory_labelframe, activestyle="none", height=4, width=25)
        self.unlearned_effect_label = ttk.Label(self.inventory_labelframe, text="Unlearned Effects")
        self.learned_effect_label = ttk.Label(self.inventory_labelframe, text="Learned Effects")
        self.status_button = ttk.Button(self.inventory_labelframe, command=self.change_effect_status,
                                        text="Change Status", width=25)
        self.quantity_label = ttk.Label(self.inventory_labelframe, text="Quantity:")
        self.quantity_entry = ttk.Entry(self.inventory_labelframe, justify="center", width=4)
        self.quantity_entry.bind("<FocusOut>", self.update_quantity)

        self.encyclopedia = ttk.Frame(self.notebook)
        self.notebook.add(self.encyclopedia, text="Encyclopedia")

        self.effect_label = ttk.Label(self.encyclopedia, text="Effects:")
        self.effect_label.place(x=10, y=10)

        self.select_effect = ttk.Combobox(self.encyclopedia, height=10, width=25,
                                          values=get_effect_name(self.alchemy_data), state="readonly",
                                          textvariable="effect")
        self.select_effect.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        self.select_effect.place(x=60, y=10)

        self.ingredient_label = ttk.Label(self.encyclopedia, text="Ingredients:")
        self.ingredient_label.place(x=250, y=10)

        self.select_ingredient = ttk.Combobox(self.encyclopedia, height=10, width=25,
                                              values=get_ingredient_name(self.alchemy_data),
                                              state="readonly", textvariable="ingredient")
        self.select_ingredient.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        self.select_ingredient.place(x=330, y=10)

        self.selected_item = LabelFrame(self.encyclopedia, bg="#dcdcdc", height=400, width=500)

        self.button_list = []
        self.selected_ingredient = {}

    def change_effect_status(self):
        selection = ""
        value = ""
        if self.unlearned_effect_listbox.curselection():
            index = self.unlearned_effect_listbox.curselection()
            selection = self.unlearned_effect_listbox.get(index)
            self.learned_effect_listbox.insert(END, selection)
            self.unlearned_effect_listbox.delete(index)
            value = "True"
        elif self.learned_effect_listbox.curselection():
            index = self.learned_effect_listbox.curselection()
            selection = self.learned_effect_listbox.get(index)
            self.unlearned_effect_listbox.insert(END, selection)
            self.learned_effect_listbox.delete(index)
            value = "False"
        else:
            messagebox.showerror("Error", "No effect selected!")
            return
        for effect in self.selected_ingredient["effect"]:
            if effect["name"] == selection:
                effect["learned"] = value
                break
        write_ingredient_data(self.ingredient_data)

    def destroy_buttons(self):
        for button in self.button_list:
            button.place_forget()
            del button
        self.button_list.clear()

    def display_info(self, name):
        self.selected_item.configure(text=name)
        self.selected_item.place(relwidth=.95, relx=.025, y=80)
        for index in range(0, len(self.button_list)):
            if 4 <= len(self.button_list) <= 5:
                self.button_list[index].place(relx=.5, rely=1 / len(self.button_list), x=-80,
                                              y=50 * index)
            elif len(self.button_list) == 6:
                self.button_list[index].place(relx=.5, rely=.15, x=-80, y=50 * index)
            elif 7 <= len(self.button_list) <= 8:
                if index < 4:
                    self.button_list[index].place(relx=.33, rely=.25, x=-90, y=50 * index)
                else:
                    self.button_list[index].place(relx=.66, rely=.25, x=-70, y=50 * (index - 4))
            elif 9 <= len(self.button_list) <= 10:
                if index < 5:
                    self.button_list[index].place(relx=.33, rely=.2, x=-90, y=50 * index)
                else:
                    self.button_list[index].place(relx=.66, rely=.2, x=-70, y=50 * (index - 5))
            elif 11 <= len(self.button_list) <= 12:
                if index < 6:
                    self.button_list[index].place(relx=.33, rely=.15, x=-90, y=50 * index)
                else:
                    self.button_list[index].place(relx=.66, rely=.15, x=-70, y=50 * (index - 6))
            elif 13 <= len(self.button_list) <= 15:
                if index < 5:
                    self.button_list[index].place(relx=.25, rely=.2, x=-120, y=50 * index)
                elif index < 10:
                    self.button_list[index].place(relx=.5, rely=.2, x=-80, y=50 * (index - 5))
                elif index < 15:
                    self.button_list[index].place(relx=.75, rely=.2, x=-40, y=50 * (index - 10))
            elif 17 <= len(self.button_list) <= 18:
                if index < 6:
                    self.button_list[index].place(relx=.25, rely=.15, x=-120, y=50 * index)
                elif index < 12:
                    self.button_list[index].place(relx=.5, rely=.15, x=-80, y=50 * (index - 6))
                else:
                    self.button_list[index].place(relx=.75, rely=.15, x=-40, y=50 * (index - 12))
            else:
                if index < 8:
                    self.button_list[index].place(relx=.25, rely=.08, x=-120, y=50 * index)
                elif index < 16:
                    self.button_list[index].place(relx=.5, rely=.08, x=-80, y=50 * (index - 8))
                else:
                    self.button_list[index].place(relx=.75, rely=.08, x=-40, y=50 * (index - 16))

    def enumerate_button_list(self, group, name):
        self.destroy_buttons()
        item_list = []
        if group == "effect":
            item_list = get_ingredient_name(self.alchemy_data, name)
            group = "ingredient"
        elif group == "ingredient":
            item_list = get_effect_name(self.alchemy_data, name)
            group = "effect"

        for index in range(0, len(item_list)):
            button = ttk.Button(self.selected_item, text=item_list[index], width=25)
            button.configure(command=lambda b=button: self.on_button_press(b, group))
            self.button_list.append(button)

    def on_button_press(self, button, group):
        self.enumerate_button_list(group, button.cget("text"))
        self.display_info(button.cget("text"))

    def on_combobox_selected(self, event):
        selected_combobox = event.widget
        selection = selected_combobox.get()
        selected_combobox.set("")
        self.master.focus()
        self.enumerate_button_list(selected_combobox.cget("textvariable"), selection)
        self.display_info(selection)

    def on_listbox_selected(self, event):
        selected_listbox = event.widget
        if not selected_listbox.curselection():
            return
        selection = selected_listbox.get(selected_listbox.curselection())
        self.show_inventory_item(selection)

    def show_inventory_item(self, ingredient_name):
        self.inventory_labelframe.configure(text=ingredient_name)
        self.inventory_labelframe.place(x=185, y=9)
        self.unlearned_effect_listbox.place(x=10, y=50)
        self.learned_effect_listbox.place(x=179, y=50)
        self.unlearned_effect_label.place(x=39, y=25)
        self.learned_effect_label.place(x=214, y=25)
        self.status_button.place(relx=.5, x=-80, y=130)
        self.unlearned_effect_listbox.delete(0, END)
        self.learned_effect_listbox.delete(0, END)
        for ingredient in self.ingredient_data["ingredient"]:
            if ingredient["name"] == ingredient_name:
                self.selected_ingredient = ingredient
                break
        for index in range(4):
            if self.selected_ingredient["effect"][index]["learned"] == "False":
                self.unlearned_effect_listbox.insert(END, ingredient["effect"][index]["name"])
            else:
                self.learned_effect_listbox.insert(END, ingredient["effect"][index]["name"])
        self.quantity_label.place(relx=.5, x=-45, y=180)
        self.quantity_entry.delete(0, END)
        self.quantity_entry.insert(0, self.selected_ingredient["quantity"])
        self.quantity_entry.place(relx=.5, x=15, y=180)

    def update_quantity(self, event):
        if int(self.quantity_entry.get()) != self.selected_ingredient["quantity"]:
            self.selected_ingredient["quantity"] = self.quantity_entry.get()
            write_ingredient_data(self.ingredient_data)


main()
