import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

rowSet = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
columnSet = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
depthSet = ('1', '2')
orientationSet = ('vertical', 'horizontal')
myDestroyerPlace = {'row': 1, 'column': 1, 'depth': 1, 'orientation': 'vertical'}
mySubmarinePlace = {'row': 1, 'column': 1, 'depth': 1, 'orientation': 'vertical'}


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300+100+50")
        self.wm_title("Battle Ship")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (InputFrame, AttackFrame):  # 如果需要增加页面，新建class,并且在这里添加
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 只有最上面的可见

        self.show_frame(InputFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # 切换


# 第一页，输入玩家所在坐标
class InputFrame(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.root = root

        ttk.Label(self, text="Destroyer").grid(row=0, column=1)
        ttk.Label(self, text="Submarine").grid(row=0, column=2)

        ttk.Label(self, text="row:").grid(row=1)
        self.row1 = ttk.Combobox(self, state='readonly')
        self.row1['value'] = rowSet
        self.row1.grid(row=1, column=1)
        self.row2 = ttk.Combobox(self, state='readonly')
        self.row2.grid(row=1, column=2)
        self.row2['value'] = rowSet

        ttk.Label(self, text="column:").grid(row=2)
        self.column1 = ttk.Combobox(self, state='readonly')
        self.column1['value'] = columnSet
        self.column1.grid(row=2, column=1)
        self.column2 = ttk.Combobox(self, state='readonly')
        self.column2.grid(row=2, column=2)
        self.column2['value'] = columnSet

        ttk.Label(self, text="depth:").grid(row=3)
        self.depth1 = ttk.Combobox(self, state='readonly')
        # destroyer cannot be placed in the subsea layer, depth = 1
        self.depth1['value'] = ('1')
        self.depth1.grid(row=3, column=1)
        self.depth2 = ttk.Combobox(self, state='readonly')
        self.depth2.grid(row=3, column=2)
        # submarine can be placed on either of these two layers, depth = 1 or 2
        self.depth2['value'] = depthSet

        ttk.Label(self, text="orientation:").grid(row=4)
        self.orientation1 = ttk.Combobox(self, state='readonly')
        self.orientation1['value'] = orientationSet
        self.orientation1.grid(row=4, column=1)
        self.orientation2 = ttk.Combobox(self, state='readonly')
        self.orientation2.grid(row=4, column=2)
        self.orientation2['value'] = orientationSet
        ttk.Button(self, text="Enter", command=self.check_ship_place).grid(row=5, column=1)

    # check Destroyer or Submarine
    def check_single_ship(self, row, column, depth, orientation, ship_name):
        if rowSet.__contains__(row) is False:
            return ship_name + "'s row value is illegal:" + row

        if columnSet.__contains__(column) is False:
            return ship_name + "'s column value is illegal:" + column

        if depthSet.__contains__(depth) is False:
            return ship_name + "'s depth value is illegal:" + depth

        if orientationSet.__contains__(orientation) is False:
            return ship_name + "'s orientation value is illegal:" + orientation

        if orientation == 'vertical':
            if rowSet.__contains__(str(int(row) - 1)) is False or rowSet.__contains__(str(int(row) + 1)) is False:
                return ship_name + "'s row value is illegal when orientation value is vertical:" + row
        if orientation == 'horizontal':
            if columnSet.__contains__(str(int(column) - 1)) is False or columnSet.__contains__(
                    str(int(column) + 1)) is False:
                return ship_name + "'s column value is illegal when orientation value is horizontal:" + column
        return 'success'

    def check_ship_place(self):
        # check Destroyer first
        check_destroyer = self.check_single_ship(self.row1.get(), self.column1.get(), self.depth1.get(),
                                                 self.orientation1.get(), "Destroyer")
        if check_destroyer != "success":
            tk.messagebox.showerror('error', check_destroyer)
            return
        # check Submarine
        check_submarine = self.check_single_ship(self.row2.get(), self.column2.get(), self.depth2.get(),
                                                 self.orientation2.get(), "Submarine")
        if check_submarine != "success":
            tk.messagebox.showerror('error', check_submarine)
            return

        # the same layer, no overlapping coordinates
        if self.depth2.get() == '1':
            if self.orientation1.get() == 'vertical':
                for x in range(int(self.row1.get()) - 1, int(self.row1.get()) + 2):
                    if self.orientation2.get() == 'vertical':
                        for y in range(int(self.row2.get()) - 1, int(self.row2.get()) + 2):
                            if x == y and self.column1.get() == self.column2.get():
                                tk.messagebox.showerror('error', "overlapping coordinates")
                                return
                    else:
                        for y in range(int(self.column2.get()) - 1, int(self.column2.get()) + 2):
                            if x == int(self.row2.get()) and int(self.column1.get()) == y:
                                tk.messagebox.showerror('error', "overlapping coordinates")
                                return
            else:
                for x in range(int(self.column1.get()) - 1, int(self.column1.get()) + 2):
                    if self.orientation2.get() == 'vertical':
                        for y in range(int(self.row2.get()) - 1, int(self.row2.get()) + 2):
                            if int(self.row1.get()) == y and x == int(self.column2.get()):
                                tk.messagebox.showerror('error', "overlapping coordinates")
                                return
                    else:
                        for y in range(int(self.column2.get()) - 1, int(self.column2.get()) + 2):
                            if self.row1.get() == self.row2.get() and x == y:
                                tk.messagebox.showerror('error', "overlapping coordinates")
                                return

        # check pass, begin to attack
        self.begin_to_attack()

    def begin_to_attack(self):
        myDestroyerPlace['row'] = self.row1.get()
        myDestroyerPlace['column'] = self.column1.get()
        myDestroyerPlace['depth'] = self.depth1.get()
        myDestroyerPlace['orientation'] = self.orientation2.get()
        mySubmarinePlace['row'] = self.row2.get()
        mySubmarinePlace['column'] = self.column2.get()
        mySubmarinePlace['depth'] = self.depth2.get()
        mySubmarinePlace['orientation'] = self.orientation2.get()
        self.root.show_frame(AttackFrame)


# 第二页，输入攻击坐标
class AttackFrame(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.root = root

        ttk.Label(self, text="Begin to attack").grid(row=0, column=1)
        ttk.Label(self, text="row:").grid(row=1)
        self.row1 = ttk.Combobox(self, state='readonly')
        self.row1['value'] = rowSet
        self.row1.grid(row=1, column=1)

        ttk.Label(self, text="column:").grid(row=2)
        self.column1 = ttk.Combobox(self, state='readonly')
        self.column1['value'] = columnSet
        self.column1.grid(row=2, column=1)

        ttk.Label(self, text="depth:").grid(row=3)
        self.depth1 = ttk.Combobox(self, state='readonly')
        self.depth1['value'] = depthSet
        self.depth1.grid(row=3, column=1)

        ttk.Button(self, text="attack", command=self.attack).grid(row=4, column=1)
        self.attack_times = 0

    def attack(self):
        if self.row1.get().strip() == '':
            tk.messagebox.showerror('error', "please input row")
            return
        if self.column1.get().strip() == '':
            tk.messagebox.showerror('error', "please input column")
            return
        if self.depth1.get().strip() == '':
            tk.messagebox.showerror('error', "please input depth")
            return

        self.attack_times += 1
        ttk.Label(self, text="attack {}:row={}, column={}, depth={}".format(str(self.attack_times), self.row1.get(),
                                                                            self.column1.get(),
                                                                            self.depth1.get())).grid( row=4 + self.attack_times, columnspan = 2)
        #print(myDestroyerPlace)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
