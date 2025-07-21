import os
from os.path import dirname, abspath
from dotenv import load_dotenv
from fpdf import FPDF, XPos, YPos
from src.config.logger import logger

load_dotenv()


def save_as_pdf(title: str, content: str) -> str:
    """
    Saves the given title and content as a PDF file.

    The PDF is saved to the path specified in the environment variable 'SAVE_PATH'.
    If 'SAVE_PATH' is not set, the PDF is saved to the project's root directory.
    The title is used as the filename for the PDF, with non-alphanumeric characters replaced by underscores.

    Args:
        title (str): The title of the PDF.
        content (str): The content of the PDF.
    Returns:
        str: A message indicating the path to which the PDF was saved.
    """

    save_path = os.getenv('SAVE_PATH')

    if (not save_path):
        save_path = dirname(dirname(abspath(__file__)))

    try:
        # Configurar PDF com fontes padrão do PDF (evitando substituição)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        pdf.set_font(size=16, style='B')
        pdf.cell(
            w=0, h=10,
            text=title,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align='C'
        )
        pdf.ln(10)

        pdf.set_font(size=12)
        pdf.multi_cell(
            w=0, h=10,
            text=content,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )

        safe_title = "".join(c if c.isalnum() else "_" for c in title)
        pdf_path = os.path.join(save_path, f"{safe_title}.pdf")
        pdf.output(pdf_path)

        return f"Saved to {pdf_path}"
    except Exception as e:
        err = f"Falha ao salvar em PDF. ERROR: {str(e)}"
        logger.exception(err, exc_info=e)
        return err
