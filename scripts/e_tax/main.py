import os
import multiprocessing
from flask import Response, json
from scripts.e_tax import helper
from scripts.e_tax import color_pdf_file


def worker_function(
    part, collected_invalid_chars, main_process_result_dict, part_order
):
    result = {}
    result["invalid_characters"] = []
    result["worker_process"] = os.getpid()
    for char in part:
        content = char["text"]
        if content in collected_invalid_chars:
            returned_data = {}
            returned_data["text"] = char["text"]
            returned_data["page_number"] = char["page_number"]
            returned_data["x0"] = char["x0"]
            returned_data["x1"] = char["x1"]
            returned_data["y0"] = char["y0"]
            returned_data["y1"] = char["y1"]
            returned_data["fontname"] = char["fontname"]
            returned_data["size"] = char["size"]
            returned_data["width"] = char["width"]
            returned_data["height"] = char["height"]
            returned_data["top"] = char["top"]
            returned_data["bottom"] = char["bottom"]
            result["invalid_characters"].append(returned_data)
    main_process_result_dict[f"{part_order}"] = result


def parallel_process_files(standard_file, pdf_files, xlsx_files):
    # bytes streams of files
    standard_file_content = standard_file.read()
    collected_invalid_chars = helper.collect_invalid_chars_from_standard_doc(
        standard_file_content
    )

    processes = []
    manager = multiprocessing.Manager()
    total_result_dict = manager.dict()

    # Process PDF files
    pdf_result = []
    pdf_validate_file_contents = []
    parts_of_pdf_arr = []
    if len(pdf_files) > 0:
        # Create a dict to collect results

        for validate_file in pdf_files:
            validate_file_content = validate_file.read()
            pdf_validate_file_contents.append(validate_file_content)

            parts_of_pdf = helper.read_and_divide_pdf(
                validate_file_content, 3.6
            )  # 4 workers

            parts_of_pdf_arr.append(
                {"fileName": validate_file.filename, "parts": parts_of_pdf}
            )
            for order, part in enumerate(parts_of_pdf):
                p = multiprocessing.Process(
                    target=worker_function,
                    args=(part, collected_invalid_chars, total_result_dict, order),
                )
                processes.append(p)
                p.start()

    # Process XLSX files
    queue = multiprocessing.Queue()
    for validate_file in xlsx_files:
        validate_file_content = validate_file.read()
        p = multiprocessing.Process(
            target=helper.parallel_processing_xlsx_file_manager,
            args=(
                standard_file_content,
                validate_file_content,
                queue,
                2,
                validate_file.filename,
            ),
        )
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # config the result for FE.
    for parts_of_pdf in parts_of_pdf_arr:
        results_to_client = []
        for order, part in enumerate(parts_of_pdf["parts"]):
            if len(total_result_dict[f"{order}"]["invalid_characters"]) > 0:
                results_to_client.extend(
                    total_result_dict[f"{order}"]["invalid_characters"]
                )
        # handle the db saving async here in the main process, this is the main process!!!!!!!

        # color the mistakes in pdf
        pdf_file_handle = color_pdf_file.color_text_in_pdf(
            validate_file_content=pdf_validate_file_contents[
                parts_of_pdf_arr.index(parts_of_pdf)
            ],
            validation_results=results_to_client,
        )
        pdf_result.append(
            helper.config_result_to_front_end(
                summary=results_to_client,
                file_handle=pdf_file_handle,
                file_name=parts_of_pdf["file_name"],
            )
        )

    # Process XLSX results
    xlsx_result = []
    while not queue.empty():
        xlsx_result.append(queue.get())

    if xlsx_result and pdf_result:
        final_response = combine_responses(pdf_result, xlsx_result)
    elif xlsx_result:
        final_response = combine_responses(xlsx_result, [])
    elif pdf_result:
        final_response = combine_responses([], pdf_result)
    else:
        final_response = [helper.config_result_to_front_end(summary=results_to_client)]

    return helper.config_final_result_to_fe(final_response)


def combine_responses(response1, response2):
    # Extract and decode the response data
    data1 = []
    data2 = []
    for response in response1:
        data1.append(json.loads((response).get_data(as_text=True)))
    for response in response2:
        data2.append(json.loads((response).get_data(as_text=True)))

    # Combine the data (assuming both are lists)
    combined_data = data1 + data2
    # Create a new Response object with the combined data
    combined_response = Response(
        response=json.dumps(combined_data), status=200, mimetype="application/json"
    )
    return combined_response
