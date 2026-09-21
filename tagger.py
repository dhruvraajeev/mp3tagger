#!/usr/bin/env python3
"""Minimal m4a tagger: title/artist/album/cover/explicit."""
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp4 import MP4, MP4Cover

F = {"title": "\xa9nam", "artist": "\xa9ART", "album": "\xa9alb"}
path = None
e = {}

def load():
    global path
    p = filedialog.askopenfilename(filetypes=[("Audio", "*.m4a *.mp4 *.m4b *.aac")])
    if not p:
        return
    path = p
    a = MP4(p)
    for k, tag in F.items():
        e[k].delete(0, "end")
        e[k].insert(0, a.tags.get(tag, [""])[0] if a.tags else "")
    explicit.set(1 if (a.tags or {}).get("rtng", [0])[0] == 1 else 0)
    art.set("")
    lbl.config(text=p.rsplit("/", 1)[-1])

def pick_art():
    p = filedialog.askopenfilename(filetypes=[("Image", "*.jpg *.jpeg *.png")])
    if p:
        art.set(p)

def save():
    if not path:
        return messagebox.showerror("nope", "open a file first")
    a = MP4(path)
    for k, tag in F.items():
        v = e[k].get()
        if v:
            a[tag] = [v]
        elif tag in a:
            del a[tag]
    # iTunes advisory: 1 = explicit, 2 = clean, 0 = none
    a["rtng"] = [1 if explicit.get() else 0]
    if art.get():
        data = open(art.get(), "rb").read()
        fmt = MP4Cover.FORMAT_PNG if art.get().lower().endswith(".png") else MP4Cover.FORMAT_JPEG
        a["covr"] = [MP4Cover(data, imageformat=fmt)]
    a.save()
    messagebox.showinfo("saved", "tags written")

r = tk.Tk()
r.title("m4a tagger")
tk.Button(r, text="Open file…", command=load).grid(row=0, column=0, sticky="we", padx=6, pady=6)
lbl = tk.Label(r, text="(no file)")
lbl.grid(row=0, column=1, sticky="w")
for i, k in enumerate(F, start=1):
    tk.Label(r, text=k).grid(row=i, column=0, sticky="e", padx=6)
    e[k] = tk.Entry(r, width=42)
    e[k].grid(row=i, column=1, padx=6, pady=3)
explicit = tk.IntVar()
tk.Checkbutton(r, text="Explicit (iTunes advisory)", variable=explicit).grid(row=4, column=1, sticky="w")
art = tk.StringVar()
tk.Button(r, text="Cover art…", command=pick_art).grid(row=5, column=0, padx=6, pady=6)
tk.Label(r, textvariable=art, wraplength=320, justify="left").grid(row=5, column=1, sticky="w")
tk.Button(r, text="Save", command=save).grid(row=6, column=1, sticky="e", padx=6, pady=8)
r.mainloop()
