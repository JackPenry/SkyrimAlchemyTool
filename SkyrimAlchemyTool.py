import json
from tkinter import *
import tkinter.ttk as ttk


def main():
    alchemy_data = parse_json_file()
    root = Tk()
    app = SkyrimAlchemyTool(root, alchemy_data)
    root.mainloop()


def get_effect_name(data, ingredient_name=""):
    effect_name = []
    if ingredient_name:
        for ingredient in data["ingredient"]:
            if ingredient["name"] == ingredient_name:
                for index in range(0, 4):
                    effect_name.append(ingredient["effect"][index])
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


def parse_json_file():
    try:
        with open('data/alchemy_data.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("error: file 'alchemy_data.json' could not be found")
        exit(1)
    return data


class SkyrimAlchemyTool:
    def __init__(self, master, alchemy_data):
        self.master = master
        self.master.title("Skyrim Alchemy Tool")
        self.master.resizable(False, False)
        self.alchemy_data = alchemy_data

        ttk.Style().configure("TFrame", background="#dcdcdc")
        ttk.Style().configure("TRadiobutton", background="#dcdcdc")
        ttk.Style().configure("TLabel", background="#dcdcdc")
        ttk.Style().configure("TLabelframe", background="#dcdcdc")

        self.notebook = ttk.Notebook(master, height=500, width=550)
        self.notebook.pack()

        self.potion_creation = ttk.Frame(self.notebook)
        # self.notebook.add(self.framePotionCreation, text="Potion Creation Tool")

        self.encyclopedia = ttk.Frame(self.notebook)
        self.notebook.add(self.encyclopedia, text="Encyclopedia")

        self.effect_label = ttk.Label(self.encyclopedia, text="Effects:")
        self.effect_label.place(x=10, y=10)

        self.select_effect = ttk.Combobox(self.encyclopedia, height=10, width=25,
                                          values=get_effect_name(self.alchemy_data), textvariable="effect")
        self.select_effect.bind("<<ComboboxSelected>>", self.on_combobox_selection)
        self.select_effect.place(x=60, y=10)

        self.ingredient_label = ttk.Label(self.encyclopedia, text="Ingredients:")
        self.ingredient_label.place(x=250, y=10)

        self.select_ingredient = ttk.Combobox(self.encyclopedia, height=10, width=25,
                                              values=get_ingredient_name(self.alchemy_data), textvariable="ingredient")
        self.select_ingredient.bind("<<ComboboxSelected>>", self.on_combobox_selection)
        self.select_ingredient.place(x=330, y=10)

        self.selected_item = LabelFrame(self.encyclopedia, bg="#dcdcdc", height=400, width=500)

        self.button_list = []

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

    def on_combobox_selection(self, event):
        selected_combobox = event.widget
        selection = selected_combobox.get()
        selected_combobox.set("")
        self.master.focus()
        self.enumerate_button_list(selected_combobox.cget("textvariable"), selection)
        self.display_info(selection)


main()
