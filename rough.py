import tkinter as tk

def alu_4bit(x, y, sel):
    """
    Simulates 4-bit ALU based on control lines.
    x, y: 4-bit integers (0-15)
    sel: 3-bit selection string
    Returns: (result, zero_flag)
    """
    if sel == '000':      # AND
        res = x & y
    elif sel == '001':    # OR
        res = x | y
    elif sel == '010':    # ADD
        res = (x + y) & 0b1111
    elif sel == '011':    # SUBTRACT
        res = (x - y) & 0b1111
    elif sel == '100':    # NOR
        res = ~(x | y) & 0b1111
    elif sel == '101':    # SHIFT LEFT
        res = (x << y) & 0b1111
    elif sel == '111':    # SHIFT RIGHT
        res = (x >> y) & 0b1111
    else:
        res = 0

    zero = int(res == 0)
    return res, zero

def compute():
    try:
        x = int(entry_x.get(), 2)
        y = int(entry_y.get(), 2)
        sel = entry_sel.get()
        if len(sel) != 3 or not all(c in '01' for c in sel):
            raise ValueError("Selection must be 3-bit binary")
        res, zero = alu_4bit(x, y, sel)
        label_out.config(text=f"Output: {format(res, '04b')}")
        label_zero.config(text=f"Zero: {zero}")
    except:
        label_out.config(text="Invalid input")
        label_zero.config(text="")

# GUI
root = tk.Tk()
root.title("4-bit ALU Simulator")

tk.Label(root, text="X (4-bit binary):").grid(row=0, column=0)
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=1)

tk.Label(root, text="Y (4-bit binary):").grid(row=1, column=0)
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=1)

tk.Label(root, text="ALU Control (3-bit):").grid(row=2, column=0)
entry_sel = tk.Entry(root)
entry_sel.grid(row=2, column=1)

tk.Button(root, text="Compute", command=compute).grid(row=3, column=0, columnspan=2)

label_out = tk.Label(root, text="Output: ")
label_out.grid(row=4, column=0, columnspan=2)

label_zero = tk.Label(root, text="Zero: ")
label_zero.grid(row=5, column=0, columnspan=2)

root.mainloop()