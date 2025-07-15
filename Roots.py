import tkinter as tk
from decimal import Decimal, getcontext
import time

# ---------- Precision Settings ----------
getcontext().prec = 200
NEWTON_STEPS = 200
TARGET_DECIMALS = 200

# ---------- My Custom Formula ----------
def custom_initial_guess(a: Decimal) -> Decimal:
    sqrt_floor = int(a.sqrt())
    b = Decimal(sqrt_floor ** 2) or Decimal(1)
    sqrt_b = b.sqrt()
    numerator = (a + b) / 4 + (a * b) / (a + b)
    return numerator / sqrt_b

# ---------- Hybrid Square Root Function ----------
def hybrid_sqrt(a_val: Decimal, max_steps: int = NEWTON_STEPS):
    steps = []
    true_val = a_val.sqrt()
    x = custom_initial_guess(a_val)

    for i in range(max_steps):
        error = abs(x - true_val)

        digits_correct = 0
        x_str = str(x)
        t_str = str(true_val)
        for d1, d2 in zip(x_str, t_str):
            if d1 == d2 and d1 != '.':
                digits_correct += 1
            elif d1 == d2:
                continue
            else:
                break

        steps.append((i + 1, str(x), str(error), digits_correct))

        if digits_correct >= TARGET_DECIMALS:
            break

        x = (x + a_val / x) / 2

    return x, steps

# ---------- GUI Setup ----------
def compute():
    try:
        a = Decimal(entry.get())
        start_time = time.perf_counter()
        result, logs = hybrid_sqrt(a)
        end_time = time.perf_counter()
        elapsed = format(end_time - start_time, '.16f')

        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, f"🌟 Final √{a} ≈ {result}\n")
        text_output.insert(tk.END, f"⏱️ Time taken: {elapsed} seconds\n\n")
        text_output.insert(tk.END, "🧪 Iteration Log:\n\n")
        for step, val, err, digits in logs:
            text_output.insert(
                tk.END,
                f"Step {step}: √ ≈ {val[:70]}...\n"
                f"  Error: {err}\n"
                f"  Correct Digits: {digits}\n\n"
            )
    except Exception as e:
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, f"❌ Error: {e}")

# ---------- GUI Window Design ----------
root = tk.Tk()
root.title("⚡ Pronoy's Hybrid √ Calculator ⚡")
root.configure(bg="#111111")

tk.Label(
    root,
    text="Enter a number (a):",
    bg="#111111",
    fg="#00ffcc",
    font=("Segoe UI", 11, "bold")
).pack(pady=(10, 0))

entry = tk.Entry(
    root,
    width=30,
    font=("Consolas", 12),
    bg="#222222",
    fg="#00ff88",
    insertbackground="white"
)
entry.pack(pady=5)
entry.focus_set()

tk.Button(
    root,
    text="Compute √a",
    command=compute,
    bg="#00bfff",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief=tk.RAISED
).pack(pady=6)

frame = tk.Frame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(
    frame,
    wrap=tk.WORD,
    height=22,
    width=80,
    bg="#0d0d0d",
    fg="#ffffff",
    font=("Courier New", 10),
    yscrollcommand=scrollbar.set
)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_output.yview)

root.mainloop()
