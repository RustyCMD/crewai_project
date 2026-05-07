"""Dark theme palette + ttk style configuration for the dashboard."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class Palette:
    BG = "#1a1c20"
    SURFACE = "#22252b"
    SURFACE_HI = "#2c3036"
    TEXT = "#e6e6e6"
    MUTED = "#9aa0a6"
    ACCENT = "#4ea1ff"
    SUCCESS = "#5fcf80"
    WARN = "#f7c948"
    DANGER = "#ef4f4f"
    BORDER = "#3a3f46"


def apply_theme(root: tk.Misc) -> ttk.Style:
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".", background=Palette.BG, foreground=Palette.TEXT, fieldbackground=Palette.SURFACE)
    style.configure("TFrame", background=Palette.BG)
    style.configure("Surface.TFrame", background=Palette.SURFACE)
    style.configure("TLabel", background=Palette.BG, foreground=Palette.TEXT)
    style.configure("Surface.TLabel", background=Palette.SURFACE, foreground=Palette.TEXT)
    style.configure("Title.TLabel", background=Palette.BG, foreground=Palette.TEXT, font=("Segoe UI", 16, "bold"))
    style.configure("Header.TLabel", background=Palette.SURFACE, foreground=Palette.TEXT, font=("Segoe UI", 11, "bold"))
    style.configure("Muted.TLabel", background=Palette.BG, foreground=Palette.MUTED, font=("Segoe UI", 9))
    style.configure("Status.TLabel", background=Palette.BG, foreground=Palette.SUCCESS, font=("Consolas", 9))

    style.configure("TButton", background=Palette.SURFACE_HI, foreground=Palette.TEXT, padding=(10, 4))
    style.map("TButton", background=[("active", Palette.BORDER)])

    style.configure("Accent.TButton", background=Palette.ACCENT, foreground="#0a0a0a", padding=(10, 4), font=("Segoe UI", 9, "bold"))
    style.map("Accent.TButton", background=[("active", "#3287d8")])

    style.configure("Success.TButton", background=Palette.SUCCESS, foreground="#0a0a0a", padding=(10, 4), font=("Segoe UI", 9, "bold"))
    style.map("Success.TButton", background=[("active", "#48a868")])

    style.configure("Danger.TButton", background=Palette.DANGER, foreground="#ffffff", padding=(10, 4), font=("Segoe UI", 9, "bold"))
    style.map("Danger.TButton", background=[("active", "#c93b3b")])

    style.configure("TNotebook", background=Palette.BG, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=Palette.SURFACE,
        foreground=Palette.MUTED,
        padding=(14, 6),
        font=("Segoe UI", 9, "bold"),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", Palette.SURFACE_HI)],
        foreground=[("selected", Palette.TEXT)],
    )

    style.configure(
        "Treeview",
        background=Palette.SURFACE,
        fieldbackground=Palette.SURFACE,
        foreground=Palette.TEXT,
        rowheight=22,
        bordercolor=Palette.BORDER,
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=Palette.SURFACE_HI,
        foreground=Palette.TEXT,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
    )
    style.map("Treeview", background=[("selected", Palette.ACCENT)], foreground=[("selected", "#0a0a0a")])

    return style
