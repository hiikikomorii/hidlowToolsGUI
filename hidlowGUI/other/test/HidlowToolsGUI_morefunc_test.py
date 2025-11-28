import tkinter as tk

root = tk.Tk()
root.title("test")
root.geometry("1270x720")


menu_frame = tk.Frame()
menu_frame.pack()

menu_frame1 = tk.Frame()
menu_frame1.pack()

button1 = tk.Button(menu_frame, text="Number", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button1.pack(side="left", padx=5)

button2 = tk.Button(menu_frame, text="IP", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button2.pack(side="left", padx=5)

button3 = tk.Button(menu_frame, text="Lat/Lon", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button3.pack(side="left", padx=5)

button4 = tk.Button(menu_frame, text="QRcode", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button4.pack(side="left", padx=5)

button5 = tk.Button(menu_frame, text="Troll", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button5.pack(side="left", padx=5)


button1 = tk.Button(menu_frame1, text="Number", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button1.pack(side="left", padx=5)

button2 = tk.Button(menu_frame1, text="IP", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button2.pack(side="left", padx=5)

button3 = tk.Button(menu_frame1, text="Lat/Lon", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button3.pack(side="left", padx=5)

button4 = tk.Button(menu_frame1, text="QRcode", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button4.pack(side="left", padx=5)

button5 = tk.Button(menu_frame1, text="Troll", bg="gray", fg="white", width=10, activeforeground="#9F9D9D")
button5.pack(side="left", padx=5)

root.mainloop()