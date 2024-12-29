import tkinter as tk
from tkinter import scrolledtext
from clipboard import ClipboardHandler
from config import TROLL_CONFIG
from utils import make_converter  # Ensure you create this function in a utility file
import converters as c
class HomestuckConverterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Homestuck Chinese Text Converter v0.9")
        self.font_size = tk.IntVar(value=12)
        self.prefix = ""
        self.converters = self.initialize_converters()
        self.clipboard_handler = ClipboardHandler()
        self.troll = "default" 
        self.create_widgets()        # Create UI
        self.last_prefix_type = 3  # Default to "Tag" initially
        self.chatlog_troll_mapping = []  # List of (troll, line_text) tuples
        self.background_color_index=0

    def initialize_converters(self):
        """Initialize troll converters using the make_converter utility."""
        converters = {
            "Karkat": make_converter("Karkat", "#626262", "CG", c.TextConverter),
            "Aradia": make_converter("Aradia", "#a10000", "AA", c.AradiaConverter),
            "Tavros": make_converter("Tavros", "#a15000", "AT", c.TavrosConverter),
            "Sollux": make_converter("Sollux", "#a1a100", "TA", c.SolluxConverter),
            "Nepeta": make_converter("Nepeta", "#416600", "AC", c.NepetaConverter),
            "Kanaya": make_converter("Kanaya", "#008141", "GA", c.TextConverter),
            "Terezi": make_converter("Terezi", "#008282", "GC", c.TereziConverter),
            "Vriska": make_converter("Vriska", "#005682", "AG", c.VriskaConverter),
            "Equius": make_converter("Equius", "#001582", "CT", c.EquiusConverter),
            "Gamzee": make_converter("Gamzee", "#2b0057", "TC", c.GamzeeConverter),
            "Eridan": make_converter("Eridan", "#6a006a", "CA", c.EridanConverter),
            "Feferi": make_converter("Feferi", "#77003c", "CC", c.FeferiConverter),
            "Kankri": make_converter("Kankri", "#ff0000", '??', c.KankriConverter),
            "Callie": make_converter("Callie", "#929292", "UU", c.CallieConverter),
            "John": make_converter("John", "#0715cd", "EB", c.TavrosConverter),
            "Dave": make_converter("Dave", "#e00707", "TG", c.DaveConverter),
            "Rose": make_converter("Rose", "#b536da", "TT", c.TextConverter),
            "Jade": make_converter("Jade", "#4ac925", "GG", c.TextConverter),
            "Dirk": make_converter("Dirk","#f2a400","TT",c.TextConverter),
            "Doc": make_converter("Doc","#ffffff","DocTag",c.TextConverter)
        }
        return converters
    
    def create_widgets(self):
        # Input Box
        tk.Label(self.root, text="Input Text:").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.input_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15)
        self.input_box.grid(row=1, column=0, padx=5, pady=5)


        # Troll Buttons and Prefix Buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=0, pady=5)
        for idx, troll in enumerate(self.converters.keys()):
            row = idx // 6
            column = idx % 6
            tk.Button(button_frame, text=troll, command=lambda t=troll: self.set_troll_and_prefix(t)).grid(row=row, column=column, padx=5, pady=5)

        tk.Button(button_frame, text="Tag", command=lambda: self.set_prefix_and_update(3)).grid(row=row+1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="NAME", command=lambda: self.set_prefix_and_update(2)).grid(row=row+1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Name", command=lambda: self.set_prefix_and_update(1)).grid(row=row+1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="None", command=lambda: self.set_prefix_and_update(0)).grid(row=row+1, column=3, padx=5, pady=5)
        self.slider = tk.Scale(button_frame, from_=6, to=20, orient='horizontal', variable=self.font_size, command=self.update_size)
        self.slider.grid(row=row+1, column=4, columnspan=2,padx=4, pady=5)
        # Output Box
        tk.Label(self.root, text="Output Text:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15)
        self.output_box.grid(row=4, column=0, padx=5, pady=5)

        # Chat Log Box
        tk.Label(self.root, text="Chat Log:").grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.chat_log = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=30, height=32)
        self.chat_log.grid(row=1, column=1, rowspan=4, padx=5, pady=5, sticky="nsew")

        # Bottom Buttons
        button_bottom_frame = tk.Frame(self.root)
        button_bottom_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(button_bottom_frame, text="Copy Output (RTF)", command=lambda: self.copy_rtf(font_size=self.slider.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_bottom_frame, text="Copy Output", command=self.copy_plain).pack(side=tk.LEFT, padx=5)
        tk.Button(button_bottom_frame, text="Clear Input", command=lambda: self.clear_output([self.input_box, self.output_box])).pack(side=tk.LEFT, padx=5)
        tk.Button(button_bottom_frame, text="Clear Chat Log", command=self.clear_chatlog).pack(side=tk.LEFT, padx=5)
        tk.Button(button_bottom_frame,text="Copy Chat Log",command=lambda: self.clipboard_handler.copy_chatlog(self.chatlog_troll_mapping,self.slider.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_bottom_frame, text="Change Background", command=self.change_background_color).pack(side=tk.LEFT, padx=5)
        
    def set_troll_and_prefix(self, troll):
        """Set troll and update prefix based on the last selected prefix type."""
        self.troll = troll
        
        # Get the troll's tag (for default or fallback)
        troll_tag = TROLL_CONFIG.get(troll, {}).get("tag", "")

        # Respect the last selected prefix type
        if self.last_prefix_type == 0:  # No prefix
            self.prefix = ""
        elif self.last_prefix_type == 1:  # Name
            self.prefix = f"{self.troll}:"
        elif self.last_prefix_type == 2:  # Uppercase Name
            self.prefix = f"{self.troll.upper()}:"
        elif self.last_prefix_type == 3:  # Tag
            self.prefix = f"{troll_tag}:"
        else:  # Fallback: Default to Tag if undefined
            self.prefix = f"{troll_tag}:"
        if troll_tag=="DocTag":
            self.prefix=''
        # Trigger text conversion with the new troll
        self.convert_text(troll, eventType=0)

    def set_prefix_and_update(self, prefix_type):
        """Set the prefix type and reapply conversion with the current troll."""
        # Save the selected prefix type
        self.last_prefix_type = prefix_type

        troll_tag = TROLL_CONFIG.get(self.troll, {}).get("tag", "")
        if prefix_type == 0:
            self.prefix = ""
        elif prefix_type == 1:
            self.prefix = f"{self.troll}:"
        elif prefix_type == 2:
            self.prefix = f"{self.troll.upper()}:"
        elif prefix_type == 3:
            self.prefix = f"{troll_tag}:"
        if troll_tag=="DocTag":
            self.prefix=''
        # Reapply conversion with the updated prefix
        self.convert_text(self.troll, eventType=1)

    def convert_text(self, troll,eventType):
        """Convert text using the selected troll's conversion function."""
        self.troll = troll
        converter = self.converters.get(troll)
        input_text = self.input_box.get("1.0", tk.END).strip()
        converted_text = converter.convert(input_text)

        # Clear output box
        self.output_box.delete("1.0", tk.END)

        # Apply prefix
        lines = converted_text.split("\n")
        prefixed_output = [self.prefix + line if line.strip() else "" for line in lines]

        # Update output box with formatted text
        self._insert_formatted_text(self.output_box, prefixed_output, troll)

        # Handle chat log updates
        if eventType == 0:  # Update due to troll switch
            self._append_to_chatlog(prefixed_output, troll)
        elif eventType == 1:  # Update due to Prefix switch
            self._replace_latest_chatlog(prefixed_output, troll)


    def _append_to_chatlog(self, lines, troll):
        """Append new lines to the chat log and track the start position."""
        # Store the starting position of the new input
        self.last_input_position = self.chat_log.index(tk.END + "-1c")
        # Insert the new lines
        self._insert_formatted_text(self.chat_log, lines, troll)
        self.chatlog_troll_mapping.append((troll, lines))

    def _replace_latest_chatlog(self, lines, troll):
        """Replace the latest input in the chat log with new lines."""
        if self.last_input_position:
            # Clear the last inserted input
            self.chat_log.delete(self.last_input_position, tk.END)

        # Ensure a newline is added before inserting new lines
        # Check if the chat log is empty before adding a newline
        if self.chat_log.get("1.0", tk.END).strip():
            self.chat_log.insert(tk.END, "\n")
        # Reinsert the updated lines and update the position
        self._append_to_chatlog(lines, troll)


    def _insert_formatted_text(self, text_widget, lines, troll):
        """Insert formatted text into a given text widget and record troll-line mapping."""
        text_widget.tag_configure(troll, foreground=TROLL_CONFIG[troll]["color"])
        font_size=self.font_size.get()
        if troll == "Gamzee":
            font_size_small=max(int(font_size*0.8),5)
            text_widget.tag_configure("Gamzee_large", foreground=TROLL_CONFIG[troll]["color"], font=("Arial", font_size))
            text_widget.tag_configure("Gamzee_small", foreground=TROLL_CONFIG[troll]["color"], font=("Arial", font_size_small))

            for line in lines:
                toggle_size = True
                for char in line:
                    tag = "Gamzee_large" if toggle_size and ('\u4e00' <= char <= '\u9fff' or char.isdigit() or '\uff01' <= char <= '\uff5e') else "Gamzee_small"
                    toggle_size = not toggle_size
                    text_widget.insert(tk.END, char, tag)
                text_widget.insert(tk.END, "\n")  # Add newline between lines

        elif troll == "Equius":
            text_widget.tag_configure("bold", font=("Arial", font_size, "bold"))
            text_widget.tag_configure(troll, foreground=TROLL_CONFIG[troll]["color"],font=("Arial", font_size))

            for line in lines:
                start_index = text_widget.index("end-1line")  # Start of the last inserted line
                text_widget.insert(tk.END, line + "\n", troll)

                for bold_char in ["强", "壮", "劲"]:
                    pos = line.find(bold_char)
                    while pos != -1:
                        bold_start = f"{start_index}+{pos}c"
                        bold_end = f"{bold_start}+1c"
                        text_widget.tag_add("bold", bold_start, bold_end)
                        pos = line.find(bold_char, pos + 1)
        elif troll=="Doc":
            text_widget.tag_configure(troll, foreground=TROLL_CONFIG[troll]["color"],background="#0e4603",font=("Arial", font_size))
            for line in lines:
                text_widget.insert(tk.END, line + "\n", troll)
        else:
            text_widget.tag_configure(troll, foreground=TROLL_CONFIG[troll]["color"],font=("Arial", font_size))
            for line in lines:
                text_widget.insert(tk.END, line + "\n", troll)


    
    def copy_plain(self):
        """Copy plain text to clipboard."""
        output_text = self.output_box.get("1.0", tk.END).strip()
        self.clipboard_handler.copy_plain(output_text)

    def copy_rtf(self,font_size):
        """Copy RTF text to clipboard."""
        output_text = self.output_box.get("1.0", tk.END).strip()
        if hasattr(self, "troll") and self.troll:  # Ensure troll is set
            self.clipboard_handler.copy_rtf(output_text, self.troll,font_size)
        else:
            print("Error: No troll selected for RTF copy.")

    

    def clear_output(self,boxes):
        """clear input and output"""
        for box in boxes:
            box.delete("1.0",tk.END)
    
    def clear_chatlog(self):
        """Clear the chat log and troll-line mapping."""
        self.chat_log.delete("1.0", tk.END)
        self.chatlog_troll_mapping.clear()

    def change_background_color(self):
        # Change the background color of the input box
        colors=["#ffffff","#0e4603"]
        n=len(colors)
        self.background_color_index = (self.background_color_index + 1) %n
        color=colors[self.background_color_index]
        self.input_box.config(bg=color)
        self.output_box.config(bg=color)
        self.chat_log.config(bg=color)

    def update_size(self, val):
        new_size = int(float(val))
        self.font_size.set(new_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomestuckConverterApp(root)
    root.mainloop()
