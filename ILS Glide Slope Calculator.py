import tkinter as tk
import math

#create a window
window = tk.Tk()

window.title('Glide Slope or Rate of Climb/Decent')  # window title
window.geometry('675x150')  # initial window size (width x height)
window.configure(bg='grey')

# the try statment tries to square the vaules, if they are not float it will return an error that will
# print a label on the program, if it does pass the program goes on and the label disappears
def combined():
    try:
     print(svar.get()**2)
     print(gvar.get()**2)
     ex_label.configure(text='')
    except tk.TclError:
        ex_label.configure(text='Please Enter Numbers ')

    click()
    solve()

L = []
start = 200
while int(start) < 1200:
    L.append(start)
    start += 50

# solve is the equations work out your GS and RoC and the equivalent 60M type
def solve():

    radAngle = math.radians(svar.get())
    gs = (gvar.get())
    rateOfDecent = (6069 * (math.tan(radAngle) * (gs / 60)))
    a1_label.configure(text='%.0f ft/min' % rateOfDecent)

    newrod = 0
    if rateOfDecent not in L:
        for i in L:
            if rateOfDecent < i:
                newrod = i
                break

        gsnew = ((newrod * 60) / (6069 * (math.tan(float(radAngle)))))
        a2_label.configure(text='60M Friendly Rate Of Climb, %.0f ft/min' % newrod)
        a3_label.configure(text='%.0f knots GS' % gsnew)


clicks = 0
def click():
    global clicks
    clicks += 1
    c_label.configure(text='Number of Calculations : {0}'.format(clicks))
    s1_label.configure(text='Rate of Climb / Decent at {0} degrees : '.format(svar.get()))


# creates a label that will update with each click of the calculate button
c_label = tk.Label(window, text='Number of Calculations : {0} '.format(clicks), bg='grey')
c_label.grid(row=6, column=3)

# creates a entry block that will allow the input of a number or text as a str value
svar = tk.DoubleVar()
slope = tk.Entry(window, textvariable=svar)
slope.grid(row=0, column=1)
# creates a label on the left side of the slope entry block
s_label = tk.Label(window, bg='grey', text='Enter the Glide Slope (degrees) : ')
s_label.grid(row=0, column=0)
# creates a label on the right side of the slope entry block
i_label = tk.Label(window, bg='grey', text='  Note: For Instrument departures 1/200nm = 1.879 degrees')
i_label.grid(row=0, column=3)

# creates a entry block that will allow the input of number or text as a str value
gvar = tk.DoubleVar()
gspeed = tk.Entry(window, textvariable=gvar)
gspeed.grid(row=1, column=1)
# creates a label on the left side of the entry block
g_label = tk.Label(window, bg='grey', text='Enter a ground speed in knots  : ')
g_label.grid(row=1, column=0)

# creates the button that is linked to the command combined and does all the work
calc_btn = tk.Button(window, text='Calculate', command=combined, bg='black', fg='white')  # command is how to link btns with function note: leave () off
calc_btn.grid(row=2, column=1)

# Create a solution label on the left side of the program
s1_label = tk.Label(window, text='Rate of Climb / Decent at 0.0 degrees : ', bg='grey')
s1_label.grid(row=4, column=0)
# creates an answer label that is modified by click() and solve()
a1_label = tk.Label(window, text='(Solution)', bg='grey')
a1_label.grid(row=4, column=1)

# creates the M model friendly answer and is then modified by solve()
a2_label = tk.Label(window, text='60M Friendly Rate Of Climb, 000 ft/min', bg='grey')
a2_label.grid(row=5, column=0)
# creates the M model friendly answer and is then modified by solve()
a3_label = tk.Label(window, text='(GS knots)', bg='grey')
a3_label.grid(row=5, column=1)

ex_label = tk.Label(window, text=' ', bg='grey')
ex_label.grid(row=7, column=3)


window.mainloop()
