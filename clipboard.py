import win32clipboard
from config import RTF_COLOR_DICT,TROLL_CONFIG

class ClipboardHandler:
    def copy_plain(self, text):
        """Copy plain text to clipboard."""
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

    @staticmethod
    def specialChar(char):
        """Determine if a character requires special handling (Chinese, digits, punctuation)."""
        punc = ['\u3002', '\uff1f', '\uff01', '\u3010', '\u3011', '\uff0c', '\u3001',    '\uff1b', '\uff1a',
                '\u300c', '\u300d', '\u300e', '\u300f', '\u2019', '\u201c', '\u201d', '\u2018', '\uff08',
                '\uff09', '\u3014', '\u3015', '\u2026', '\u2013', '\uff0e', '\u2014', '\u300a', '\u300b',
                '\u3008', '\u3009','\u00a0','\u3000','\u0020']
        return '\u4e00' <= char <= '\u9fff' or char.isdigit() or char in punc



    @staticmethod
    def to_rtf_styled_unicode(text, troll, i, font_size):
        """
        Convert text to RTF-styled Unicode based on troll-specific formatting and font size.

        Args:
            text (str): The text to convert.
            troll (str): The troll type to apply specific formatting.
            i (int): Color index for RTF formatting.
            font_size (int): The base font size for the text. 
        Returns:
            str: RTF-styled Unicode string.
        """
        rtf_unicode = ""
        toggle_size = True  # For Gamzee's size alternation

        for char in text:
            if troll == "Gamzee":
                if char == '\n':
                    rtf_unicode += "\\par "
                elif ClipboardHandler.specialChar(char):
                    # Alternate font size for Gamzee
                    current_size = font_size if toggle_size else max(int(font_size*0.8),5)
                    rtf_unicode += f"\\cf{i}\\fs{current_size * 2}\\u{ord(char)}?"
                    toggle_size = not toggle_size
                else:
                    rtf_unicode += f"\\cf{i}\\fs{font_size * 2}{char}"
            elif troll == "Equius":
                if char in ["强", "壮", "劲"]:
                    rtf_unicode += f"\\cf{i}\\b\\fs{font_size * 2}\\u{ord(char)}?\\b0"
                elif char == '\n':
                    rtf_unicode += "\\par "
                else:
                    if ClipboardHandler.specialChar(char):
                        rtf_unicode += f"\\cf{i}\\fs{font_size * 2}\\u{ord(char)}?"
                    else:
                        rtf_unicode += f"\\cf{i}\\fs{font_size * 2}{char}"
            else:
                if char == '\n':
                    rtf_unicode += "\\par "
                elif ClipboardHandler.specialChar(char):
                    rtf_unicode += f"\\cf{i}\\fs{font_size * 2}\\u{ord(char)}?"
                else:
                    rtf_unicode += f"\\cf{i}\\fs{font_size * 2}{char}"

        return rtf_unicode

    @staticmethod
    def copy_to_clipboard_rtf(text, troll,font_size):
        """
        Generic function to copy RTF text to the clipboard.
        
        Args:
            text (str): The text content to copy.
            troll (str): Troll-specific formatting settings.
        """
        # Fetch RTF color header
        rtf_header = RTF_COLOR_DICT.get(troll, RTF_COLOR_DICT["default"])

        # Build RTF content
        rtf_content = rtf_header + ClipboardHandler.to_rtf_styled_unicode(text, troll,1,font_size) + "}"

        # Encode as bytes and copy to clipboard
        rtf_bytes = rtf_content.encode("utf-8")
        print("SS")
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32clipboard.RegisterClipboardFormat("Rich Text Format"), rtf_bytes
        )
        win32clipboard.CloseClipboard()




    # Wrappers for clarity
    def copy_rtf(self, text, troll,font_size):
        """Copy output text with troll-specific RTF formatting."""
        ClipboardHandler.copy_to_clipboard_rtf(text, troll,font_size)



    def copy_chatlog(self, chatlog_troll_mapping, font_size):
        """
        Copy chat log to clipboard with individual troll formatting and dynamic font size.

        Args:
            chatlog_troll_mapping (list of tuples): List of (troll, line) tuples.
            font_size (int): Base font size for text.
        """
        # Initialize RTF content and color table
        rtf_content = r'{\rtf1\ansi\deff0'
        colortbl = r'{\colortbl;'  # Color table for trolls

        # Iterate through trolls and their conversations
        i = 1  # Color index starts at 1
        for troll, converse_list in chatlog_troll_mapping:
            # Join conversation lines into a single text block
            text = '\n'.join(converse_list)

            # Get color definition for the troll or use default
            troll_color = RTF_COLOR_DICT.get(troll, RTF_COLOR_DICT["default"])
            colortbl += troll_color[28:-2] + ';'  # Append troll's color to the table

            # Add RTF-styled text for this troll
            rtf_content += r'\pard' + ClipboardHandler.to_rtf_styled_unicode(text, troll, i, font_size) + r'\par'
            i += 1

        # Finalize the color table and append to RTF content
        colortbl += '}'
        rtf_content = rtf_content[:17] + colortbl + rtf_content[17:] + '}'

        # Encode the RTF content as bytes and copy to clipboard
        rtf_bytes = rtf_content.encode("utf-8")

        # Use win32clipboard to copy to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32clipboard.RegisterClipboardFormat("Rich Text Format"), rtf_bytes
        )
        win32clipboard.CloseClipboard()


