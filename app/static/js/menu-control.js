import ETAX_TABS from "../constants/tabs.constant.js"; // Adjust the path as necessary

document.addEventListener("DOMContentLoaded", function () {
  const dashboardDiv = document.querySelector(".dashboard");
  const sidebarDropdownDiv = document.querySelector(".sidebar-dropdown");

  ETAX_TABS.forEach((tab) => {
    const dashboardTitleDiv = document.createElement("div");
    dashboardTitleDiv.classList.add("dashboard-title", tab.class);
    dashboardTitleDiv.setAttribute(
      "onclick",
      `toggleDropdownSidebarForDashboard();switchTab(event, '${tab.class}'); event.stopPropagation();`
    );

    const tabTitleDiv = document.createElement("div");
    tabTitleDiv.classList.add("tab-title");

    const span = document.createElement("span");
    span.textContent = tab.tag;

    const svg = document.createElement("svg");
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.classList.add("ionicon");
    svg.setAttribute("viewBox", "0 0 512 512");
    svg.setAttribute("width", "30");
    svg.setAttribute("height", "30");
    svg.style.alignSelf = "end";
    svg.classList.add("dashboard-icon");

    const path1 = document.createElement("path");
    path1.classList.add("dashboard-icon-path");
    path1.setAttribute(
      "d",
      "M428 224H288a48 48 0 01-48-48V36a4 4 0 00-4-4h-92a64 64 0 00-64 64v320a64 64 0 0064 64h224a64 64 0 0064-64V228a4 4 0 00-4-4z"
    );

    const path2 = document.createElement("path");
    path2.classList.add("dashboard-icon-path");
    path2.setAttribute(
      "d",
      "M419.22 188.59L275.41 44.78a2 2 0 00-3.41 1.41V176a16 16 0 0016 16h129.81a2 2 0 001.41-3.41z"
    );

    const dropdownTabsDiv = document.createElement("div");
    dropdownTabsDiv.classList.add("tabs");

    const tabButton = document.createElement("button");
    tabButton.classList.add("tab", tab.class);
    tabButton.textContent = tab.name;
    tabButton.setAttribute(
      "onclick",
      `toggleDropdownSidebarForDashboard();switchTab(event, '${tab.class}'); event.stopPropagation();`
    );

    svg.appendChild(path1);
    svg.appendChild(path2);

    tabTitleDiv.appendChild(span);
    tabTitleDiv.appendChild(svg);

    dashboardTitleDiv.appendChild(tabTitleDiv);
    dashboardTitleDiv.appendChild(document.createTextNode(tab.name));

    dashboardDiv.appendChild(dashboardTitleDiv);
    dropdownTabsDiv.appendChild(tabButton);
    sidebarDropdownDiv.appendChild(dropdownTabsDiv);
  });
});
