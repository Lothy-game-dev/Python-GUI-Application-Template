from selenium.webdriver.common.by import By


def get_money_type(route_element, count):
    try:
        _ = route_element.find_element(By.ID, "total-ic-fare-text" + str(count)).text
        return 2
    except Exception:
        return 1


def get_icon_features(route_element):
    try:
        icon_list = route_element.find_element(
            By.CSS_SELECTOR, ".section_header_contents .time_frame .icon_list"
        )
        icons = icon_list.find_elements(By.CLASS_NAME, "left")
        icon_string = ""
        for icon in icons:
            icon_alt = icon.find_element(By.CSS_SELECTOR, "img")
            icon_string += icon_alt.get_attribute("alt") + ", "
        return icon_string.rstrip(", ")
    except Exception:
        return ""


def get_icon_features_bus(route_element):
    try:
        icon_list = route_element.find_element(By.CSS_SELECTOR, ".route-feature")
        icons = icon_list.find_elements(By.CLASS_NAME, "rote-feature")
        icon_string = ""
        for icon in icons:
            if icon.get_attribute("alt") == "早い":
                icon_string += "早, "
            elif icon.get_attribute("alt") == "安い":
                icon_string += "安, "
            elif icon.get_attribute("alt") == "乗換が少ない":
                icon_string += "楽, "
        return icon_string.rstrip(", ")
    except Exception:
        return ""


def get_money(normal, ic):
    if ic == "":
        return "運賃: " + normal + "円"
    return "きっぷ運賃: " + normal + "円\nIC運賃: " + ic + "円"
