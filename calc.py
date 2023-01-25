# https://www.blog.pythonlibrary.org/2019/02/12/creating-a-calculator-with-wxpython/
import wx

# creates a simple frame class
class Frame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Calculater", size=(350,375))
        panel = CalcPanel(self)
        self.SetSizeHints(350, 375, 350, 375)
        self.Show()

# A class for all of the panels
class CalcPanel(wx.Panel):

    # initalizes the panel and
    def __init__(self, parent):
        super().__init__(parent)
        self.last_button_pressed = None
        self.create_ui()

    # creats the basic GUI
    def create_ui(self):
        # sets the border and font
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)

        # sets the sultion box 
        self.solution = wx.TextCtrl(self, style=wx.TE_RIGHT)
        self.solution.SetFont(font)
        self.solution.Disable()
        main_sizer.Add(self.solution, 0, wx.EXPAND | wx.ALL, 5)
        self.running_total = wx.StaticText(self)
        main_sizer.Add(self.running_total, 0, wx.ALIGN_RIGHT)

        # creates a list for the button labels to be called from
        buttons = [['7', '8', '9', '/'],
               ['4', '5', '6', '*'],
               ['1', '2', '3', '-'],
               ['.', '0', '', '+']]
        
        # creates a button for each item in the array
        for label_list in buttons:
            btn_sizer = wx.BoxSizer()
            for label in label_list:
                button = wx.Button(self, label=label)
                btn_sizer.Add(button, 1, wx.ALIGN_CENTER, 0)
                button.Bind(wx.EVT_BUTTON, self.update_equation) # adds the label of the button to the equation
            main_sizer.Add(btn_sizer, 1, wx.ALIGN_CENTER)

        # creates the = button and sets it to display the total
        equals_btn = wx.Button(self, label='=')
        equals_btn.Bind(wx.EVT_BUTTON, self.on_total)
        main_sizer.Add(equals_btn, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        # creates the clear button and sets it to clear the equation
        clear_btn = wx.Button(self, label='Clear')
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        main_sizer.Add(clear_btn, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        # deisplays everything
        self.SetSizer(main_sizer)

    # adds to the existing equation
    def update_equation(self, event):
        # get the operators ready to be used in the equation
        operators = ['/', '*', '-', '+']
        btn = event.GetEventObject()
        label = btn.GetLabel()
        current_equation = self.solution.GetValue()

        # checks to see if the operator is in the list of operators
        if label not in operators:
            if self.last_button_pressed in operators:
                self.solution.SetValue(current_equation + ' ' + label)
            else:
                self.solution.SetValue(current_equation + label)
        elif label in operators and current_equation is not '' \
         and self.last_button_pressed not in operators:
            self.solution.SetValue(current_equation + ' ' + label)

        self.last_button_pressed = label

        # updates the solution
        for item in operators:
            if item in self.solution.GetValue():
                self.update_solution()
                break

    # updates the equation
    def update_solution(self):
        # tries to make the equation run
        try:
            current_solution = str(eval(self.solution.GetValue()))
            self.running_total.SetLabel(current_solution)
            self.Layout()
            return current_solution
        # checks for division by 0 and will display an error if it is
        except ZeroDivisionError:
            self.solution.SetValue('ZeroDivisionError')
        except:
            pass

    # clears the equation
    def on_clear(self, event):
        self.solution.Clear()
        self.running_total.SetLabel('')

    # gets the total and displays it uderneath the equation
    def on_total(self, event):
        solution = self.update_solution()
        if solution:
            self.running_total.SetLabel('')
            self.solution.SetValue(solution)

# not sure what this if statement does. may have to do with python being in main naturally
if __name__ == "__main__":
    app = wx.App(False) # creates an app
    frame = Frame()     # calls and creats the frame
    app.MainLoop()      # keeps the app in a loop
