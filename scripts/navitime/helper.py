import time
import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.common.main import (
    find_and_click,
    find_and_click_by_class_name,
    is_on_application,
    set_driver,
)

if is_on_application():
    from scripts.navitime.main import (
        get_money_type,
        get_money,
        get_icon_features,
        get_icon_features_bus,
    )
else:
    from navitime.main import (
        get_money_type,
        get_money,
        get_icon_features,
        get_icon_features_bus,
    )


def get_commute_pass(driver_instance, start, end, transitions, type_pass):
    try:
        data_return = {
            "routes": [],
            "price1month": [],
            "price3month": [],
            "price6month": [],
        }

        set_driver(driver_instance)

        input_fields = [
            ('//*[@id="transfer_form"]/div[1]/dl[1]/dd/input[1]', start),
            ('//*[@id="transfer_form"]/div[1]/dl[2]/dd/input[1]', end),
        ]

        for xpath, value in input_fields:
            input_field = find_and_click(xpath)
            input_field.send_keys(value)
            driver_instance.implicitly_wait(2)

        transition_fields = [
            ('//*[@id="transfer_form"]/dl[1]/dd[1]/input[1]', transitions[0]),
            ('//*[@id="transfer_form"]/dl[1]/dd[2]/input[1]', transitions[1]),
            ('//*[@id="transfer_form"]/dl[1]/dd[3]/input[1]', transitions[2]),
        ]

        for i, (xpath, value) in enumerate(transition_fields):
            if value != "":
                if i > 0:
                    find_and_click('//*[@id="transfer_form"]/dl[1]/dd[4]/a', 1)
                transition_field = driver_instance.find_element(By.XPATH, xpath)
                transition_field.send_keys(value)
                time.sleep(2)

        select_type = driver_instance.find_element(
            By.XPATH, '//*[@id="transfer_form"]/dl[3]/dd/select'
        )
        select = Select(select_type)
        type_options = {"通勤": 1, "通学": 2, "通学（高校）": 3, "通学（中学）": 4}
        option_value = type_options.get(type_pass, 1)
        current_selected_option = select.first_selected_option
        if current_selected_option.get_attribute("value") != option_value:
            for option in select.options:
                if option.get_attribute("value") == option_value:
                    select.select_by_visible_text(option.text)
                    break

        driver_instance.implicitly_wait(2)
        find_and_click('//*[@id="submit_route_search"]')
        driver_instance.implicitly_wait(5)
        try:
            not_found_msg = driver_instance.find_element(By.CLASS_NAME, "error-message")
            data_return["routes"].append(not_found_msg.text)
            return data_return
        except Exception:
            count = 0
            i = 0
            while count < 3:
                try:
                    pass_data = driver_instance.find_element(By.ID, f"pass_{i + 1}")

                    route_array = [
                        div.find_element(By.CSS_SELECTOR, ".section__line__node").text
                        for div in pass_data.find_elements(
                            By.CLASS_NAME, "pass_contents__tr--section"
                        )
                        if div.find_element(
                            By.CSS_SELECTOR, ".section__line__node"
                        ).text
                        != ""
                    ]

                    route_string = "\n".join(route_array)
                    data_return["routes"].append(route_string)
                    driver_instance.implicitly_wait(1)

                    pass_money_data = pass_data.find_element(
                        By.XPATH, "./div[1]/table/tbody/tr[2]"
                    )
                    price_array = []
                    for pass_money in pass_money_data.find_elements(
                        By.CLASS_NAME, "cell-number"
                    ):
                        month_price_main = pass_money.find_element(
                            By.CLASS_NAME, "price__number"
                        ).text
                        month_price_lower = (
                            pass_money.find_element(By.CLASS_NAME, "lower").text
                            if pass_money.find_elements(By.CLASS_NAME, "lower")
                            else None
                        )
                        month_price = month_price_main + (
                            "\n" + month_price_lower if month_price_lower else ""
                        )
                        price_array.append(month_price)

                    data_return["price1month"].append(price_array[0])
                    data_return["price3month"].append(price_array[1])
                    data_return["price6month"].append(price_array[2])
                    count += 1
                    i += 1
                except Exception as e:
                    print(f"Error: {e}")
                    i += 1
                    continue
            return data_return
    except Exception as e:
        print(e)
        return {
            "routes": [
                "エラーが発生しました！データの取得に失敗しました。入力ファイルおよび/またはインターネット接続を再確認してください。"
            ],
            "price1month": [],
            "price3month": [],
            "price6month": [],
        }


# Function to get the best routes between start and end points using Selenium WebDriver
def get_best_routes(
    driver_instance, start, end, money, standard, index, length, transport
):

    try:
        set_driver(driver_instance)

        # Input start and end points
        element1 = driver_instance.find_element(
            By.XPATH,
            "//*[@id='body-top']/div[2]/div[1]/div/div/div[1]/div[1]/div[1]/div/label/input",
        )
        element1.send_keys(start)

        element2 = driver_instance.find_element(
            By.XPATH,
            "//*[@id='body-top']/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div/label/input",
        )
        element2.send_keys(end)
        driver_instance.implicitly_wait(2)

        # Return data, try-catch for each route to ignore if not exist
        data_return = {
            "routes": [],
            "cost": [],
            "transferTime": [],
            "time": [],
            "feature": [],
            "distance": [],
            "step": [],
            "calories": [],
            "flightName": [],
            "flightStartTime": [],
            "flightEndTime": [],
        }
        if start == end:
            data_return["routes"].append("出発地と目的地が同じです。")
            return data_return
        if transport == "train":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[2]')

            # Click search button
            find_and_click_by_class_name("route-search-contents__main__search-button")

            # Wait 2 seconds for output to show
            driver_instance.implicitly_wait(4)
            # Select language
            select_lang = driver_instance.find_element(
                By.XPATH, '//*[@id="selector_area"]/select'
            )
            select = Select(select_lang)
            option_id = "language_ja"
            current_selected_option = select.first_selected_option
            if current_selected_option.get_attribute("id") != option_id:
                for option in select.options:
                    if option.get_attribute("id") == option_id:
                        select.select_by_visible_text(option.text)
                        break
            driver_instance.implicitly_wait(1)
            if standard.replace(" ", "") == "早":
                find_and_click('//*[@id="left_pane"]/ul[3]/li[2]/a')
            elif standard.replace(" ", "") == "楽":
                find_and_click('//*[@id="left_pane"]/ul[3]/li[4]/a')
            elif standard.replace(" ", "") == "安":
                find_and_click('//*[@id="left_pane"]/ul[3]/li[3]/a')

            # Wait 2 seconds for output to show
            driver_instance.implicitly_wait(2)

            count = 0
            i = 0
            while count < 3:
                try:
                    # Try to find the first route by its ID
                    try:
                        route1 = driver_instance.find_element(
                            By.ID, "detail_route_" + str(i)
                        )
                    except Exception:
                        break
                    route1_array = []
                    # Iterate through each station in the route
                    for div in route1.find_elements(
                        By.CLASS_NAME, "section_station_frame"
                    ):
                        # Find the station name and append it to the route string
                        final = div.find_element(
                            By.CSS_SELECTOR, ".station_frame .left"
                        )
                        if len(route1_array) > 0:
                            if route1_array[len(route1_array) - 1] != final.text:
                                route1_array.append(final.text)
                        else:
                            route1_array.append(final.text)
                    # Remove the trailing arrow from the route string
                    route1_string = " -> ".join(route1_array)
                    driver_instance.implicitly_wait(1)
                    driver_instance.implicitly_wait(1)
                    if get_money_type(route1, i + 1) == 1:
                        # Get the normal fare cost
                        normal_cost = route1.find_element(
                            By.ID, "total-fare-text" + str(i + 1)
                        ).text
                        if float(normal_cost) >= float(money):
                            print("Overcost")
                            i += 1
                            continue
                        data_return["cost"].append(get_money(normal_cost, ""))
                    else:
                        # Get the normal fare cost
                        normal_cost = route1.find_element(
                            By.ID, "total-fare-text" + str(i + 1)
                        ).text
                        if float(normal_cost) >= float(money):
                            print("Overcost")
                            i += 1
                            continue
                        # Get the IC fare cost
                        ic_cost = route1.find_element(
                            By.ID, "total-ic-fare-text" + str(i + 1)
                        ).text
                        data_return["cost"].append(get_money(normal_cost, ic_cost))

                    # Append the route string to the data_return dictionary
                    driver_instance.implicitly_wait(1)
                    data_return["routes"].append(route1_string)

                    # Get the time and transfer time for the route
                    time_frame = route1.find_element(By.CLASS_NAME, "time_frame")
                    data = time_frame.find_elements(By.CSS_SELECTOR, "dd.left")
                    driver_instance.implicitly_wait(1)
                    data_return["time"].append(data[0].text)
                    data_return["transferTime"].append(
                        data[1].find_element(By.CLASS_NAME, "num").text
                    )
                    driver_instance.implicitly_wait(1)
                    # Get the features of the route and append to the data_return dictionary
                    data_return["feature"].append(get_icon_features(route1))
                    driver_instance.implicitly_wait(1)
                    driver_instance.implicitly_wait(1)
                    count += 1
                    i += 1
                except Exception as e:
                    # If the route is not found, print the error message
                    print(f"Error: {e}")
                    i += 1

            return data_return

        if transport == "car":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[3]')

            # Click search button
            find_and_click_by_class_name(
                "route-search-contents__main__search-button", 2
            )

            search_again = False
            hidden_value_input_start = driver_instance.find_element(
                By.XPATH, '//*[@id="route-search-start-box"]/div[1]/input[2]'
            )
            if hidden_value_input_start.get_attribute("value") == "":
                search_again = True
                results_container_start = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-start-box"]/div[2]/div[1]/section'
                )
                results_start = results_container_start.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                start_chosen = False
                for result in results_start:
                    if result.get_attribute("title") == start:
                        driver_instance.execute_script("arguments[0].click();", result)
                        start_chosen = True
                        break

                if start_chosen is False:
                    if results_start:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_start[0]
                        )

            _ = driver_instance.find_element(
                By.XPATH, '//*[@id="route-search-goal-box"]/div[1]/input[2]'
            )
            if hidden_value_input_start.get_attribute("value") == "":
                search_again = True
                results_container_end = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-goal-box"]/div[2]/div[1]/section'
                )
                results_end = results_container_end.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                end_chosen = False
                for result in results_end:
                    if result.get_attribute("title") == end:
                        driver_instance.execute_script("arguments[0].click();", result)
                        end_chosen = True
                        break

                if end_chosen is False:
                    if results_end:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_end[0]
                        )

            if search_again is True:
                find_and_click(
                    '//*[@id="route-search-condition-content"]/div/div[3]/button', 5
                )
            index = 1
            if standard.replace(" ", "") == "有料":
                index = 1
            elif standard.replace(" ", "") == "無料":
                index = 2
            elif standard.replace(" ", "") == "距離":
                index = 3
            elif standard.replace(" ", "") == "低燃費":
                index = 4
            elif standard.replace(" ", "") == "景観":
                index = 5

            if index != 1:
                find_and_click('//*[@id="ui-id-' + str(index + 1) + '"]', 5)
            route = driver_instance.find_element(
                By.XPATH, '//*[@id="route-' + str(index) + '"]'
            )
            route_data = route.find_element(By.XPATH, "./div[1]/ul/ul")
            route_array = []
            # Iterate through each station in the route
            for div in route_data.find_elements(By.CLASS_NAME, "name-area"):
                # Find the station name and append it to the route string
                final = div.find_element(By.CSS_SELECTOR, ".name")
                if len(route_array) > 0:
                    if route_array[len(route_array) - 1] != final.text:
                        route_array.append(final.text)

            # Remove the trailing arrow from the route string
            route_string = " -> ".join(route_array)
            data_return["routes"].append(route_string)

            driver_instance.implicitly_wait(1)
            time_span = route.find_element(By.XPATH, "./div[1]/div/div[1]/span")
            data_return["time"].append(time_span.text.replace("(", "").replace(")", ""))

            driver_instance.implicitly_wait(1)
            try:
                cost = route.find_element(By.CLASS_NAME, "value-car-fare").text
                etc_cost = route.find_element(By.CLASS_NAME, "value-etc-fare").text
                cost_number = "".join(filter(str.isdigit, cost))
                etc_cost_number = "".join(filter(str.isdigit, etc_cost))
                data_return["cost"].append(
                    cost_number + " 円\nETC: " + etc_cost_number + " 円"
                )
            except Exception:
                cost = route.find_element(By.CLASS_NAME, "value-normal-fare").text
                data_return["cost"].append(cost)

            driver_instance.implicitly_wait(1)
            data_return["feature"].append(standard.replace(" ", ""))
            driver_instance.implicitly_wait(1)

            return data_return

        if transport == "bus":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[4]')

            # Click search button
            find_and_click_by_class_name(
                "route-search-contents__main__search-button", 1
            )

            driver_instance.implicitly_wait(1)

            try:
                not_found = driver_instance.find_element(By.CLASS_NAME, "message-area")
                data_return["routes"].append(not_found.text)

                driver_instance.implicitly_wait(1)
                return data_return
            except Exception:
                driver_instance.implicitly_wait(1)
                if standard.replace(" ", "") == "楽":
                    find_and_click('//*[@id="summary-tab"]/li[3]/a')
                elif standard.replace(" ", "") == "安":
                    find_and_click('//*[@id="summary-tab"]/li[2]/a', 2)

                count = 0
                i = 0
                while count < 3:
                    try:
                        # Try to find the first route by its ID
                        try:
                            route1 = driver_instance.find_element(
                                By.ID, "route-" + str(i + 1)
                            )
                        except Exception:
                            break
                        route1_array = []
                        # Iterate through each station in the route
                        for div in route1.find_elements(
                            By.CLASS_NAME, "station-info-area"
                        ):
                            # Find the station name and append it to the route string
                            final = div.find_element(
                                By.CSS_SELECTOR, ".station-info .station-name a"
                            )
                            if len(route1_array) > 0:
                                if route1_array[len(route1_array) - 1] != final.text:
                                    route1_array.append(final.text)
                            else:
                                route1_array.append(final.text)
                        # Remove the trailing arrow from the route string
                        route1_string = " -> ".join(route1_array)
                        driver_instance.implicitly_wait(1)
                        # Check the type of fare (normal or IC) and get the corresponding cost

                        driver_instance.implicitly_wait(1)
                        normal_cost = route1.find_element(
                            By.CLASS_NAME, "normal-fare"
                        ).text.replace(",", "")
                        if float(normal_cost) >= float(money):
                            print("Overcost")
                            i += 1
                            continue
                        data_return["cost"].append(normal_cost + "円")

                        # Append the route string to the data_return dictionary
                        driver_instance.implicitly_wait(1)
                        data_return["routes"].append(route1_string)

                        # Get the time and transfer time for the route
                        time_frame = route1.find_element(By.XPATH, "./div[1]/div/dl/dd")
                        driver_instance.implicitly_wait(1)
                        data_return["time"].append(time_frame.text)
                        data_return["transferTime"].append(
                            route1.find_element(By.XPATH, "./div[1]/dl/dd/span[1]").text
                        )
                        driver_instance.implicitly_wait(1)
                        # Get the features of the route and append to the data_return dictionary
                        data_return["feature"].append(get_icon_features_bus(route1))
                        driver_instance.implicitly_wait(1)
                        driver_instance.implicitly_wait(1)
                        count += 1
                        i += 1
                    except Exception as e:
                        # If the route is not found, print the error message
                        print(f"Error: {e}")
                        i += 1

                return data_return

        if transport == "walk":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[5]')

            # Click search button
            find_and_click_by_class_name(
                "route-search-contents__main__search-button", 2
            )

            search_again = False
            try:
                _ = driver_instance.find_element(By.ID, "routeWalk")
            except Exception:
                search_again = True
                results_container_start = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-start-box"]/div[2]/div[1]/section'
                )
                results_start = results_container_start.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                start_chosen = False
                for result in results_start:
                    if result.get_attribute("title") == start:
                        driver_instance.execute_script("arguments[0].click();", result)
                        start_chosen = True
                        break

                if start_chosen is False:
                    if results_start:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_start[0]
                        )
                search_again = True
                results_container_end = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-goal-box"]/div[2]/div[1]/section'
                )
                results_end = results_container_end.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                end_chosen = False
                for result in results_end:
                    if result.get_attribute("title") == end:
                        driver_instance.execute_script("arguments[0].click();", result)
                        end_chosen = True
                        break

                if end_chosen is False:
                    if results_end:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_end[0]
                        )

            if search_again is True:
                find_and_click(
                    '//*[@id="route-search-condition-content"]/div/div[3]/button', 5
                )

            try:
                not_found = driver_instance.find_element(
                    By.CLASS_NAME, "route-search-error"
                )
                return_text = "検索条件に合致するルートを検索することができませんでした。\n考えられる理由は次のとおりです:"
                for div in not_found.find_elements(By.TAG_NAME, "div"):
                    return_text += "\n" + div.text
                data_return["routes"].append(return_text)

                driver_instance.implicitly_wait(1)
                return data_return
            except Exception:
                route = driver_instance.find_element(By.ID, "route-1")
                route_section = route.find_element(By.XPATH, "./div[1]/ul/ul")
                route_array = []
                for div in route_section.find_elements(By.CLASS_NAME, "poi-info-area"):
                    final = div.find_element(By.CSS_SELECTOR, ".poi-name-wrap .name")
                    if len(route_array) > 0:
                        if route_array[len(route_array) - 1] != final.text:
                            route_array.append(final.text)
                    else:
                        route_array.append(final.text)
                route_string = " -> ".join(route_array)
                data_return["routes"].append(route_string)
                driver_instance.implicitly_wait(1)
                summary = route.find_element(By.CLASS_NAME, "summary")
                time_data = (
                    summary.find_element(By.CLASS_NAME, "total-time")
                    .text.replace("(", "")
                    .replace(")", "")
                )
                data_return["time"].append(time_data)
                driver_instance.implicitly_wait(1)
                route_detail = summary.find_element(
                    By.CLASS_NAME, "route-summary-detail-info"
                )
                distance = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-distance .value div"
                )
                data_return["distance"].append(distance.text)
                driver_instance.implicitly_wait(1)
                step = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-step .value div"
                )
                data_return["step"].append(step.text)
                calories = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-calorie .value div"
                )
                data_return["calories"].append(calories.text)

                return data_return

        if transport == "bike":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[6]')

            # Click search button
            find_and_click_by_class_name(
                "route-search-contents__main__search-button", 2
            )

            driver_instance.implicitly_wait(2)

            search_again = False
            try:
                _ = driver_instance.find_element(By.ID, "routeBicycle")
            except Exception:
                search_again = True
                results_container_start = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-start-box"]/div[2]/div[1]/section'
                )
                results_start = results_container_start.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                start_chosen = False
                for result in results_start:
                    if result.get_attribute("title") == start:
                        driver_instance.execute_script("arguments[0].click();", result)
                        start_chosen = True
                        break

                if start_chosen is False:
                    if results_start:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_start[0]
                        )
                search_again = True
                results_container_end = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-goal-box"]/div[2]/div[1]/section'
                )
                results_end = results_container_end.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                end_chosen = False
                for result in results_end:
                    if result.get_attribute("title") == end:
                        driver_instance.execute_script("arguments[0].click();", result)
                        end_chosen = True
                        break

                if end_chosen is False:
                    if results_end:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_end[0]
                        )

            if search_again is True:
                find_and_click(
                    '//*[@id="route-search-condition-content"]/div/div[3]/button'
                )

            done = False
            while done is False:
                check = 0
                try:
                    route = driver_instance.find_element(By.ID, "route-1")
                except Exception:
                    check += 1

                try:
                    not_found = driver_instance.find_element(
                        By.CLASS_NAME, "route-search-error"
                    )
                except Exception:
                    check += 1

                if check == 2:
                    driver_instance.implicitly_wait(1)
                else:
                    done = True

            try:
                not_found = driver_instance.find_element(
                    By.CLASS_NAME, "route-search-error"
                )
                return_text = "検索条件に合致するルートを検索することができませんでした。\n考えられる理由は次のとおりです:"
                for div in not_found.find_elements(By.TAG_NAME, "div"):
                    return_text += "\n" + div.text
                data_return["routes"].append(return_text)

                driver_instance.implicitly_wait(1)
                return data_return
            except Exception:
                driver_instance.implicitly_wait(1)
                standard_no = 1
                if standard.replace(" ", "") == "距離が短い":
                    print("hahahahaha")
                elif standard.replace(" ", "") == "坂道が少ない":
                    standard_no = 2
                elif standard.replace(" ", "") == "坂道が多い":
                    standard_no = 3
                elif standard.replace(" ", "") == "大通り優先":
                    standard_no = 4
                elif standard.replace(" ", "") == "裏通り優先":
                    standard_no = 5

                if standard_no != 1:
                    find_and_click('//*[@id="ui-id-' + str(standard_no + 11) + '"]', 2)

                route = driver_instance.find_element(By.ID, "route-" + str(standard_no))
                route_section = route.find_element(By.XPATH, "./div[1]/ul/ul")
                route_array = []
                for div in route_section.find_elements(By.CLASS_NAME, "poi-info-area"):
                    final = div.find_element(By.CSS_SELECTOR, ".poi-name-wrap .name")
                    if len(route_array) > 0:
                        if route_array[len(route_array) - 1] != final.text:
                            route_array.append(final.text)
                    else:
                        route_array.append(final.text)

                route_string = " -> ".join(route_array)
                data_return["routes"].append(route_string)
                driver_instance.implicitly_wait(1)
                summary = route.find_element(By.CLASS_NAME, "summary")
                time_data = (
                    summary.find_element(By.CLASS_NAME, "total-time")
                    .text.replace("(", "")
                    .replace(")", "")
                )
                data_return["time"].append(time_data)
                driver_instance.implicitly_wait(1)
                route_detail = summary.find_element(
                    By.CLASS_NAME, "route-summary-detail-info"
                )
                distance = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-distance .value div"
                )
                data_return["distance"].append(distance.text)
                calories = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-calorie .value div"
                )
                data_return["calories"].append(calories.text)

                return data_return

        if transport == "plane":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[7]')

            # click for suggestion in start and end point
            find_and_click(
                '//*[@id="body-top"]/div[2]/div[1]/div/div/div[1]/div[1]/div/div/label/input',
                2,
            )
            start_input_suggest = driver_instance.find_element(
                By.XPATH,
                '//*[@id="body-top"]/div[2]/div[1]/div/div/div[1]/div[1]/div[3]/dl',
            )
            for suggest in start_input_suggest.find_elements(
                By.CLASS_NAME, "airport-suggest__list__item"
            ):
                if (
                    start.replace(" ", "").lower()
                    in suggest.text.replace(" ", "").lower()
                ):
                    driver_instance.execute_script("arguments[0].click();", suggest)
                    break

            find_and_click(
                '//*[@id="body-top"]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div/label/input',
                2,
            )
            end_input_suggest = driver_instance.find_element(
                By.XPATH,
                '//*[@id="body-top"]/div[2]/div[1]/div/div/div[1]/div[2]/div[3]/dl',
            )
            for suggest in end_input_suggest.find_elements(
                By.CLASS_NAME, "airport-suggest__list__item"
            ):
                if (
                    end.replace(" ", "").lower()
                    in suggest.text.replace(" ", "").lower()
                ):
                    driver_instance.execute_script("arguments[0].click();", suggest)
                    break

            find_and_click_by_class_name("picker__input", 1)
            if (
                standard.replace(" ", "") == ""
                or standard.replace(" ", "") == "すべて表示"
            ):
                pass
            elif standard.replace(" ", "") == "ANAのみ":
                find_and_click("./li[2]")
            elif standard.replace(" ", "") == "JALのみ":
                find_and_click("./li[3]")
            elif standard.replace(" ", "") == "LCC/その他":
                find_and_click("./li[4]")

            # Click search button
            find_and_click_by_class_name(
                "route-search-contents__main__search-button", 10
            )
            try:
                # Select language
                select_lang = driver_instance.find_element(
                    By.XPATH, '//*[@id="selector-area"]/select'
                )
                select = Select(select_lang)
                option_id = "language_ja"
                current_selected_option = select.first_selected_option
                if current_selected_option.get_attribute("id") != option_id:
                    for option in select.options:
                        if option.get_attribute("id") == option_id:
                            select.select_by_visible_text(option.text)
                            break

                driver_instance.implicitly_wait(1)
            except Exception:
                pass

            try:
                not_found = driver_instance.find_element(
                    By.CLASS_NAME, "not-match-line-frame"
                )
                return_text = "ご指定の条件での飛行機の運航はございません。"
                data_return["routes"].append(return_text)

                driver_instance.implicitly_wait(1)
                return data_return
            except Exception:
                content = driver_instance.find_element(
                    By.ID, "airplane-diagram-content"
                )
                date_str = driver_instance.find_element(
                    By.CLASS_NAME, "diagram-date"
                ).text
                count = 0
                i = 0
                while i < length:
                    try:
                        frame = content.find_elements(
                            By.CLASS_NAME, "diagram-result-frame"
                        )[i]
                    except Exception:
                        break
                    driver_instance.implicitly_wait(1)
                    flight_name = frame.find_element(
                        By.CSS_SELECTOR, ".flight .name"
                    ).text
                    data_return["flightName"].append(flight_name)
                    driver_instance.implicitly_wait(1)
                    start_time = frame.find_element(
                        By.CSS_SELECTOR, ".dep-time .time-str"
                    ).text
                    data_return["flightStartTime"].append(date_str + " " + start_time)
                    driver_instance.implicitly_wait(1)
                    end_time = frame.find_element(
                        By.CSS_SELECTOR, ".arv-time .time-str"
                    ).text
                    data_return["flightEndTime"].append(date_str + " " + end_time)
                    driver_instance.implicitly_wait(1)
                    diff_time = (
                        frame.find_element(By.CLASS_NAME, "diff-time")
                        .text.replace("(", "")
                        .replace(")", "")
                    )
                    data_return["time"].append(diff_time)
                    count += 1
                    i += 1
                    if count == 3:
                        break

                return data_return

        if transport == "truck":
            find_and_click('//*[@id="body-top"]/div[2]/div[1]/ul/li[8]')

            # Click search button
            find_and_click_by_class_name(
                "route-search-contents__main__search-button", 2
            )

            search_again = False
            try:
                _ = driver_instance.find_element(By.ID, "routeBicycle")
            except Exception:
                search_again = True
                results_container_start = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-start-box"]/div[2]/div[1]/section'
                )
                results_start = results_container_start.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                start_chosen = False
                for result in results_start:
                    if result.get_attribute("title") == start:
                        driver_instance.execute_script("arguments[0].click();", result)
                        start_chosen = True
                        break

                if start_chosen is False:
                    if results_start:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_start[0]
                        )
                search_again = True
                results_container_end = driver_instance.find_element(
                    By.XPATH, '//*[@id="route-search-goal-box"]/div[2]/div[1]/section'
                )
                results_end = results_container_end.find_elements(
                    By.CLASS_NAME, "kw-result-item"
                )
                end_chosen = False
                for result in results_end:
                    if result.get_attribute("title") == end:
                        driver_instance.execute_script("arguments[0].click();", result)
                        end_chosen = True
                        break

                if end_chosen is False:
                    if results_end:
                        driver_instance.execute_script(
                            "arguments[0].click();", results_end[0]
                        )

            if search_again is True:
                find_and_click(
                    '//*[@id="route-search-condition-content"]/div/div[3]/button'
                )

            done = False
            while done is False:
                check = 0
                try:
                    route = driver_instance.find_element(By.ID, "route-1")
                except Exception:
                    check += 1

                try:
                    not_found = driver_instance.find_element(
                        By.CLASS_NAME, "route-search-error"
                    )
                except Exception:
                    check += 1

                if check == 2:
                    driver_instance.implicitly_wait(1)
                else:
                    done = True

            try:
                not_found = driver_instance.find_element(
                    By.CLASS_NAME, "route-search-error"
                )
                return_text = "検索条件に合致するルートを検索することができませんでした。\n考えられる理由は次のとおりです:"
                for div in not_found.find_elements(By.TAG_NAME, "div"):
                    return_text += "\n" + div.text
                data_return["routes"].append(return_text)

                driver_instance.implicitly_wait(1)
                return data_return
            except Exception:
                driver_instance.implicitly_wait(1)
                standard_no = 1
                if standard.replace(" ", "") == "推奨ルート":
                    pass
                elif standard.replace(" ", "") == "無料優先":
                    standard_no = 2
                elif standard.replace(" ", "") == "高速優先":
                    standard_no = 3
                elif standard.replace(" ", "") == "道幅優先":
                    standard_no = 5

                if standard_no != 1:
                    try:
                        find_and_click(
                            '//*[@id="ui-id-' + str(standard_no + 1) + '"]', 2
                        )
                    except Exception:
                        find_and_click('//*[@id="ui-id-' + str(standard_no) + '"]', 2)

                try:
                    route = driver_instance.find_element(
                        By.ID, "route-" + str(standard_no)
                    )
                except Exception:
                    route = driver_instance.find_element(
                        By.ID, "route-" + str(standard_no - 1)
                    )
                route_section = route.find_element(By.XPATH, "./div[1]/ul/ul")
                route_array = []
                for div in route_section.find_elements(By.CLASS_NAME, "poi-info-area"):
                    final = div.find_element(By.CSS_SELECTOR, ".poi-name-wrap .name")
                    if len(route_array) > 0:
                        if route_array[len(route_array) - 1] != final.text:
                            route_array.append(final.text)
                    else:
                        if final.text == "":
                            route_array.append(start)
                        else:
                            route_array.append(final.text)

                route_string = " -> ".join(route_array)
                data_return["routes"].append(route_string)
                driver_instance.implicitly_wait(1)
                summary = route.find_element(By.CLASS_NAME, "summary")
                time_data = (
                    summary.find_element(By.CLASS_NAME, "total-time")
                    .text.replace("(", "")
                    .replace(")", "")
                )
                data_return["time"].append(time_data)
                driver_instance.implicitly_wait(1)
                route_detail = summary.find_element(
                    By.CLASS_NAME, "route-summary-detail-info"
                )
                distance = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-distance .value div"
                )
                data_return["distance"].append(distance.text)
                fare = route_detail.find_element(
                    By.CSS_SELECTOR, ".total-fare .value .fare-link"
                )
                data_return["cost"].append(fare.text.replace(" (", " (ETC:"))

            return data_return
        return None

    except Exception as e:
        err_string = ""
        if "Element not found" in str(e):
            err_string = "要素が見つかりませんでした。入力データを確認してください。"
        elif "TimeoutException" in str(e):
            err_string = "タイムアウトエラーが発生しました。インターネット接続を確認してください。"
        elif "WebDriverException" in str(e):
            err_string = (
                "WebDriverエラーが発生しました。ブラウザの設定を確認してください。"
            )
        else:
            err_string = "エラーが発生しました！データの取得に失敗しました。入力ファイルおよび/またはインターネット接続を再確認してください。"
        if transport == "plane":
            return {
                "routes": [],
                "cost": [],
                "transferTime": [],
                "time": [],
                "feature": [],
                "distance": [],
                "step": [],
                "calories": [],
                "flightName": [err_string],
                "flightStartTime": [],
                "flightEndTime": [],
            }
        return {
            "routes": [err_string],
            "cost": [],
            "transferTime": [],
            "time": [],
            "feature": [],
            "distance": [],
            "step": [],
            "calories": [],
            "flightName": [],
            "flightStartTime": [],
            "flightEndTime": [],
        }
