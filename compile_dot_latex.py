import argparse
import os
import shutil
import subprocess


def convert_dot_to_image(dot_file, output_format="png"):
    if output_format not in ["png", "svg"]:
        raise ValueError("Output format must be 'png' or 'svg'.")

    base_name = os.path.splitext(dot_file)[0]
    tex_file = f"{base_name}.tex"
    pdf_file = f"{base_name}.pdf"
    output_file = f"{base_name}.{output_format}"

    try:
        subprocess.run(
            ["dot2tex", "-ftikz", dot_file, "-o", tex_file],
            check=True,
        )

        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file], check=True)

        if output_format == "png":
            subprocess.run(
                [
                    "convert",
                    "-density",
                    "300",
                    "-background",
                    "white",
                    "-alpha",
                    "remove",
                    pdf_file,
                    "-quality",
                    "90",
                    output_file,
                ],
                check=True,
            )
        elif output_format == "svg":
            subprocess.run(["pdf2svg", pdf_file, output_file], check=True)
    finally:
        for ext in ["aux", "log", "tex", "pdf"]:
            file_to_remove = f"{base_name}.{ext}"
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

    print(f"Output saved as {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert DOT file to image.")
    parser.add_argument("dot_file", help="The input DOT file.")
    parser.add_argument(
        "output_format",
        default="png",
        choices=["png", "svg"],
        help="The output format (default: png).",
    )

    args = parser.parse_args()

    format = args.output_format

    required_commands = ["dot2tex", "pdflatex"]
    if format == "svg":
        required_commands.append("pdf2svg")

    if format == "png":
        required_commands.append("convert")

    for command in required_commands:
        if not shutil.which(command):
            raise EnvironmentError(f"Required command '{command}' is not available.")

    convert_dot_to_image(args.dot_file, args.output_format)
