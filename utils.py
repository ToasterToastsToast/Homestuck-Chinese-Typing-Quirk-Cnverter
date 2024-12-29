from converters import TextConverter
from config import TROLL_CONFIG, RTF_COLOR_DICT

def make_converter(name, color, tag, converter_class=None):
    """
    Adds a new troll to the configuration and returns the converter instance.
    
    Args:
        name (str): Troll's name (e.g., "Terezi").
        color (str): Hex color code (e.g., "#008282").
        tag (str): Troll's shorthand tag (e.g., "GC").
        converter_class (TextConverter): Specific converter class for this troll.
    
    Returns:
        converter_instance: The created converter instance.
    """
    # Convert hex color to RTF color format
    hex_to_rtf = lambda hex_color: (
        r"{\rtf1\ansi\deff0{\colortbl;" +
        f"\\red{int(hex_color[1:3], 16)}" +
        f"\\green{int(hex_color[3:5], 16)}" +
        f"\\blue{int(hex_color[5:], 16)};}}"
    )
    

    # Add to TROLL_CONFIG
    TROLL_CONFIG[name] = {"color": color, "tag": tag}
    
    # Add to RTF_COLOR_DICT
    RTF_COLOR_DICT[name] = hex_to_rtf(color)
    
    # Create and return the converter instance
    return (converter_class or TextConverter)()
