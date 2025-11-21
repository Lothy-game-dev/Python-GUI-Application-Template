import fitz  # PyMuPDF


def color_text_in_pdf(
    validate_file_content,
    validation_results,
    color_for_validation=(1, 0, 0),
    # yellow background
    fill=(1, 0.984, 0),
):
    # Load the PDF from bytes
    pdf_document = fitz.open(stream=validate_file_content, filetype="pdf")

    # Iterate through pages
    for result in validation_results:
        # Load the page (adjusting for 0-based index)
        page = pdf_document.load_page(result["page_number"] - 1)

        block = (
            result["x0"],
            page.rect.height - result["y1"],
            result["x1"],
            page.rect.height - result["y0"],
        )
        rect = fitz.Rect(block)

        # get the block and the span for the area of interest
        blocks = page.get_text("dict", clip=rect)["blocks"]
        if len(blocks) == 0:
            # If we can not find any block, then continue
            continue
        span = blocks[0]["lines"][0]["spans"][0]
        # span looks like this
        page.add_redact_annot(rect)
        page.apply_redactions()

        # Determine the font to use for the modified text
        font_to_use = "helv"
        for font in page.get_fonts():
            if font == span["font"]:
                font_to_use = span["font"]

        #  draw the yellow highlight bounding box
        page.draw_rect(span["bbox"], fill=fill, width=0)

        #        Write new text with modified properties using TextWriter
        tw = fitz.TextWriter(page.rect, color=color_for_validation)
        tw.append(
            span["origin"],
            span["text"],
            font=fitz.Font(font_to_use),
            fontsize=span["size"],
        )
        tw.write_text(page)

    return pdf_document
