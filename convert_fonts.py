from fontTools.ttLib import TTFont
from fontTools.subset import main as subset
import os

def convert_font_to_woff2(input_path, output_directory=None):
    """
    Converts a TTF font to WOFF2 format and reduces it to Latin subset.
    
    Args:
        input_path (str): Path to the input TTF file
        output_directory (str, optional): Directory for output files. Defaults to same as input.
    """
    try:
        # Verify input file exists
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input font file not found: {input_path}")

        # Get absolute paths
        input_path = os.path.abspath(input_path)
        input_directory = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        base_name = os.path.splitext(filename)[0]
        
        # Use provided output directory or input directory
        output_directory = os.path.abspath(output_directory) if output_directory else input_directory
        
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        
        # Intermediate file path for subset
        subset_path = os.path.join(output_directory, f"{base_name}_subset.ttf")
        
        # Final WOFF2 output path
        woff2_path = os.path.join(output_directory, f"{base_name}.woff2")
        
        print(f"Processing font file: {input_path}")
        print(f"Output directory: {output_directory}")
        
        # Step 1: Create Latin subset
        subset_args = [
            input_path,
            '--output-file=' + subset_path,
            '--unicodes=U+0020-007F',  # Basic Latin only
            '--no-layout-closure',      # Don't close GSUB/GPOS lookups
            '--layout-features=""',     # Remove all layout features
            '--desubroutinize',         # Optimize for WOFF2 compression
            # '--no-hinting',             # Remove hinting
            # '--no-subset-tables+=DSIG', # Remove digital signature
            # '--glyphs=*',               # Keep only used glyphs
            # '--drop-tables+=FFTM'
        ]

        # Add commonly used punctuation and special characters
        additional_chars = [
            'U+00A0',  # NO-BREAK SPACE
            'U+00A9',  # COPYRIGHT SIGN
            'U+00AE',  # REGISTERED SIGN
            'U+2013',  # EN DASH
            'U+2014',  # EM DASH
            'U+2018',  # LEFT SINGLE QUOTATION MARK
            'U+2019',  # RIGHT SINGLE QUOTATION MARK
            'U+201C',  # LEFT DOUBLE QUOTATION MARK
            'U+201D',  # RIGHT DOUBLE QUOTATION MARK
            'U+2022',  # BULLET
            'U+2026',  # HORIZONTAL ELLIPSIS
        ]

        subset_args.extend([f'--unicodes={char}' for char in additional_chars])

        subset(subset_args)
        
        # Step 2: Convert to WOFF2
        font = TTFont(subset_path)

        # for table in ['GSUB', 'GPOS', 'kern', 'prep', 'gasp', 'fpgm', 'cvt ', 'OS/2']:
        #     if table in font:
        #         del font[table]

        font.flavor = 'woff2'
        font.save(woff2_path)
        
        # Clean up intermediate file
        os.remove(subset_path)
        
        # Get file sizes
        original_size = os.path.getsize(input_path)
        final_size = os.path.getsize(woff2_path)
        compression_ratio = (1 - (final_size / original_size)) * 100
        
        print("\nConversion completed successfully!")
        print(f"Original size: {original_size/1024:.2f}KB")
        print(f"Final size: {final_size/1024:.2f}KB")
        print(f"Compression ratio: {compression_ratio:.1f}%")
        print(f"Output saved to: {woff2_path}")
        
        return woff2_path
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with your font path
    convert_font_to_woff2('font1.otf')
    convert_font_to_woff2('font2.otf')

# def main():
#     """
#     Main function to handle command line usage
#     """
#     if len(sys.argv) < 2:
#         print("Usage:")
#         print("python script.py <path_to_font.ttf> [output_directory]")
#         print("\nExample:")
#         print("python script.py ./fonts/myfont.ttf ./converted_fonts")
#         return

#     input_font = sys.argv[1]
#     output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
#     convert_font_to_woff2(input_font, output_dir)

# if __name__ == "__main__":
#     main()
