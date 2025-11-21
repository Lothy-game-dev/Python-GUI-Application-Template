from openpyxl.styles import PatternFill
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText


def color_text_in_xlsx(
    workbook,
    validation_results,
    color_for_validation="FF0000",
    # yellow background color
    fill="FFFF00",
):
    text_color = InlineFont(b=True, color=color_for_validation)
    background_color = PatternFill(start_color=fill, end_color=fill, fill_type="solid")

    # Iterate through results
    for cell in validation_results:
        sheet = workbook[f'{cell["sheet_name"]}']
        original_cell = sheet[f'{cell["cell_coordinate"]}']

        # cell.value could be a CellRichText of text blocks, a string, or a number
        if isinstance(original_cell.value, CellRichText):
            collections_of_text_blocks = []
            for block in original_cell.value:
                if isinstance(block, TextBlock):
                    if block.text in cell["invalid_chars"]:
                        collections_of_text_blocks.append(
                            TextBlock(text_color, block.text)
                        )
                    else:
                        collections_of_text_blocks.append(block)
                else:
                    if block in cell["invalid_chars"]:
                        collections_of_text_blocks.append(TextBlock(text_color, block))
                    else:
                        collections_of_text_blocks.append(block)

        else:

            collections_of_text_blocks = [
                TextBlock(text_color, char) if char in cell["invalid_chars"] else char
                for char in str(original_cell.value)
            ]
        rich_text = CellRichText(collections_of_text_blocks)
        sheet[f'{cell["cell_coordinate"]}'] = rich_text
        sheet[f'{cell["cell_coordinate"]}'].fill = background_color

    return workbook
