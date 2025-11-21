function showLoading() {
  var activeTab = document.querySelector(".tab-content.active");
  activeTab.querySelector("#loading").style.display = "flex";
}
function handleSubmit(event) {
  event.preventDefault(); // Prevent default form submission
  showLoading(); // Show loading animation
  var socket = io("http://127.0.0.1:5002");
  var activeTab = document.querySelector(".tab-content.active");
  socket.on("connect", function () {
    console.log("Connected to server");
  });
  socket.on("progress", function (data) {
    activeTab.querySelector(".progress").style.width = data.progress + "%";
    activeTab.querySelector(".progress-text").innerText =
      Math.round(data.progress) + "%";
  });
  socket.on("text", function (data) {
    activeTab.querySelector("#text").innerText = data.text;
  });
  var formData = new FormData(activeTab.querySelector("form"));
  fetch("/", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.blob();
      } else {
        throw new Error("ファイルのダウンロードに失敗しました");
      }
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "results.xlsx"; // You may adjust this as necessary
      document.body.appendChild(a);
      a.click();
      a.remove();

      activeTab.querySelector(".progress").style.width = "100%";
      activeTab.querySelector("#loading p").innerText = "100%";
      setTimeout(function () {
        activeTab.querySelector("#loading").style.display = "none"; // Hide loading animation
        activeTab.querySelector(".progress").style.width = "0%";
        activeTab.querySelector("#loading p").innerText = "0%";
        alert(
          "ダウンロードが完了しました！ファイルは「Downloads」フォルダに保存されました。"
        );
      }, 1000); // Hide after 1 second
    })
    .catch((error) => {
      console.error(error);
      if (error.name === "AbortError") {
        displayError(
          { message: "インターネット接続を確認してください。" },
          "navi-error"
        );
      } else {
        displayError({ message: error.message }, "navi-error");
      }
      activeTab.querySelector(".progress").style.width = "0%";
      activeTab.querySelector("#loading p").innerText = "0%";
      activeTab.querySelector("#loading").style.display = "none"; // Hide loading animation on error
    });
}

function updateProgressBar() {
  var activeTab = document.querySelector(".tab-content.active");
  var progressText = activeTab.querySelector("#loading p").innerText;
  var progressValue = parseInt(progressText.replace("%", ""));

  var interval = setInterval(function () {
    var progressIncrease = Math.round((Math.random() * 3 + 1) * 10) / 10;
    if (progressValue + progressIncrease >= 100) {
      activeTab.querySelector(".progress").style.width = "99.9%";
      activeTab.querySelector("#loading p").innerText = "99.9%";
      clearInterval(interval);
    } else {
      progressValue += progressIncrease;
      activeTab.querySelector(".progress").style.width = progressValue + "%";
      activeTab.querySelector("#loading p").innerText =
        Math.round(progressValue * 10) / 10 + "%";
    }
  }, 3000); // Adjust the interval time as necessary
  return interval;
}

function switchTab(event, tabClass) {
  const allTabs = document.querySelectorAll(".dashboard-title");
  const mainContent = document.querySelector(".main-content");
  const tabContents = document.querySelectorAll(".tab-content");
  const sideTabs = document.querySelectorAll(".tab");

  // Check if the clicked tab is already active
  const isActive = document.querySelector(
    `.dashboard-title.${tabClass}.active`
  );

  if (isActive) {
    // If active, remove the active class to hide the content
    allTabs.forEach((tab) => tab.classList.remove("active"));
    tabContents.forEach((content) => {
      content.classList.remove("active");
      content.style.display = "none";
    });
    sideTabs.forEach((tab) => tab.classList.remove("active"));
    mainContent.classList.remove("active");
  } else {
    // Otherwise, activate the clicked tab and its content
    allTabs.forEach((tab) => tab.classList.remove("active"));
    tabContents.forEach((content) => {
      content.classList.remove("active");
      content.style.display = "none";
    });
    sideTabs.forEach((tab) => tab.classList.remove("active"));

    allTabs.forEach((tab) => {
      if (tab.classList.contains(tabClass)) {
        tab.classList.add("active");
      }
    });

    tabContents.forEach((content) => {
      if (content.classList.contains(tabClass)) {
        content.classList.add("active");
        content.style.display = "block";
      }
    });

    sideTabs.forEach((tab) => {
      if (tab.classList.contains(tabClass)) {
        tab.classList.add("active");
      }
    });

    // Activate main content if any tab is active
    if (document.querySelector(`.dashboard-title.${tabClass}.active`)) {
      mainContent.classList.add("active");
    } else {
      mainContent.classList.remove("active");
    }
  }
}

function switchTabNavitime(event, tabId) {
  var tabContents = document.querySelectorAll(".navitime-content");
  const naviTabs = document.querySelectorAll(".navi-tab");
  if (tabId == "tab2" && naviTabs[0].classList.contains("active")) {
    document.getElementById("mover").style.transform = "translateX(100%)";
    naviTabs[0].classList.remove("active");
    naviTabs[1].classList.add("active");
  } else {
    document.getElementById("mover").style.transform = "translateX(0%)";
    naviTabs[0].classList.add("active");
    naviTabs[1].classList.remove("active");
  }

  tabContents.forEach(function (content) {
    content.classList.remove("active");
  });

  document.getElementById(tabId).classList.add("active");
}

function downloadTemplateFile(event) {
  event.preventDefault();
  var transport = document.querySelector('input[name="transport"]:checked');
  if (!transport) {
    alert("交通手段を選択してください。");
  } else {
    var templateLink = document.getElementById("template-link");
    window.location.href = templateLink.href;
  }
}

function updateFileName() {
  var activeTab = document.querySelector(".tab-content.active");
  var fileInput = activeTab.querySelector(".file-input");
  var fileName = activeTab.querySelector(".file-name");
  fileName.textContent =
    fileInput.files.length > 0
      ? fileInput.files[0].name
      : "ファイルが選択されていません";
}

function handleFileDrop(event) {
  event.preventDefault();
  var activeTab = document.querySelector(".tab-content.active");
  var fileInput = activeTab.querySelector(".file-input");
  if (fileInput) {
    fileInput.files = event.dataTransfer.files;
    updateFileName();
  } else {
    console.error("File input element not found.");
  }
}

function handleDragOver(event) {
  event.preventDefault();
}

document.addEventListener("DOMContentLoaded", function () {
  var fileInputContainers = document.querySelectorAll(".file-input-container");
  fileInputContainers.forEach(function (container) {
    container.addEventListener("drop", handleFileDrop);
    container.addEventListener("dragover", handleDragOver);
  });
});

function toggleDropdown() {
  document.querySelector(".dropdown").classList.toggle("show");
}
// Add this function to handle clicks outside the dropdown
function handleClickOutside(event) {
  const dropdown = document.querySelector(".dropdown");
  if (!dropdown.contains(event.target)) {
    dropdown.classList.remove("show");
  }
}

// Add event listener to the document
document.addEventListener("click", handleClickOutside);
function toggleDropdownSidebar(event, tabClass) {
  document.querySelectorAll(".sidebar-dropdown").forEach(function (dropdown) {
    dropdown.classList.toggle("show");
  });
  switchTab(event, tabClass);
}

function toggleDropdownSidebarForDashboard(event, tabId) {
  document.querySelector(".sidebar-dropdown").classList.add("show");
}

function setDefaultFile(fileName) {
  document.getElementById("defaultFile").value = fileName;
  toggleDropdown();
  updateSelectedFile(fileName);
}

function updateSelectedFile(fileName) {
  const links = document.querySelectorAll(".dropdown-content a");
  links.forEach((link) => {
    if (link.textContent === fileName) {
      link.classList.add("selected");
    } else {
      link.classList.remove("selected");
    }
  });
}

// Initialize the selected file on page load
document.addEventListener("DOMContentLoaded", function () {
  const defaultFile = document.getElementById("defaultFile").value;
  updateSelectedFile(defaultFile);
});

function handleNewFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    setDefaultFile(file.name);
    document.getElementById("defaultFile").value = file.name;

    // Create a new option in the dropdown for the uploaded file
    const dropdownContent = document.querySelector(".dropdown-content");
    const newOption = document.createElement("div");
    newOption.style.display = "flex";
    newOption.style.alignItems = "center";
    newOption.style.justifyContent = "space-between";

    const fileLink = document.createElement("a");
    fileLink.href = "#";
    fileLink.textContent = file.name;
    fileLink.style.width = "100%";
    fileLink.onclick = function () {
      setDefaultFile(file.name);
    };

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "消去";
    deleteButton.style.whiteSpace = "nowrap";
    deleteButton.className = "delete-button";
    deleteButton.onclick = function () {
      deleteFileOption(newOption, file.name);
    };

    newOption.appendChild(fileLink);
    newOption.appendChild(deleteButton);

    // Insert the new option before the "Change file" label
    const changeFileLabel = document.querySelector(".file-upload-label");
    dropdownContent.insertBefore(newOption, changeFileLabel);

    // Automatically select the new file
    updateSelectedFile(file.name);
  }
}

function deleteFileOption(optionElement, fileName) {
  const dropdownContent = document.querySelector(".dropdown-content");
  dropdownContent.removeChild(optionElement);
  // Optionally, you can reset the default file if the deleted file was selected
  const defaultFileInput = document.getElementById("defaultFile");
  if (defaultFileInput.value === fileName) {
    defaultFileInput.value = "";
    updateSelectedFile(""); // Update the UI to reflect no file selected
  }
  // Reset the file input element to allow re-selection of the same file
  document.getElementById("newFileInput").value = "";
}
// ------------------------------------------------------------
// console.log("Internet connected");
// document.addEventListener("click", function (event) {
//   switchTab(null, "tab1");
// });
function disableSubmitButton(id, buttonId) {
  document.getElementById(id).style.display = "flex";
  document.getElementById(buttonId).disabled = true;
  //   document.getElementById("tab3").style.opacity = "70%";
  //   document.getElementById("tab3").style["pointer-events"] = "none";
}
function ableSubmitButton(id, buttonId) {
  document.getElementById(id).style.display = "none";
  document.getElementById(buttonId).disabled = false;
  //   document.getElementById("tab3").style.opacity = "100%";
  //   document.getElementById("tab3").style["pointer-events"] = "unset";
}
function displayError(error, id) {
  const errorDiv = document.getElementById(id);
  if (!error) {
    errorDiv.innerHTML = "";
    errorDiv.style.display = "none";
    return;
  }
  errorDiv.innerHTML = error.message || "Some thing went wrong";
  errorDiv.style.display = "block";
}
function displayUrl(url) {
  // console.log("displayUrl", url);
  const p = document.getElementById("url");
  if (!url) {
    p.innerHTML = "";
    p.style.display = "none";
    return;
  }
  p.innerHTML +=
    "ダウンロードフォルダーを確認してください。ファイル名は次のとおりです:<br>" +
    url.join("<br>");
  p.style.display = "block";
}

function handleResult(result) {
  const resultDiv = document.getElementById("result");
  if (!result) {
    resultDiv.innerHTML = "";
    resultDiv.style.display = "none";
    return;
  }
  // Check if result.summary is defined and has a length property
  if (result.summary && result.summary.length > 0) {
    // console.log(
    //   "handleResult ~ result.summary.length:",
    //   result.summary.length
    // );
    resultDiv.innerHTML = "文内にエラーは見つかりませんでした";
    resultDiv.style.display = "block";
  } else {
    resultDiv.innerHTML = "";
    resultDiv.style.display = "none";
  }
}

function handleUploadValidate(event) {
  const currentTarget = event.currentTarget;
  event.preventDefault(); // Prevent default form submission
  var formData = new FormData(currentTarget);
  const validateFile = formData.get("validateFile"); // Returns a File object
  disableSubmitButton("loadingValidate", "uploadButton-validate");
  displayError("", "error");
  displayUrl();
  handleResult();
  if (validateFile) {
    console.log("File Name:", validateFile.name); // File name
    console.log("File Type:", validateFile.type); // MIME type

    // Format file size
    let fileSize = validateFile.size;
    let formattedFileSize;
    if (fileSize >= 1024 * 1024) {
      formattedFileSize = (fileSize / (1024 * 1024)).toFixed(2) + " MB";
    } else if (fileSize >= 1024) {
      formattedFileSize = (fileSize / 1024).toFixed(2) + " KB";
    } else {
      formattedFileSize = fileSize + " bytes";
    }
    // console.log("File Size:", formattedFileSize); // Formatted file size

    if (validateFile.size > 15 * 1024 * 1024) {
      alert(
        "予期せぬエラーが発生しました。\\nファイルの内容、インターネット接続を確認し、もう一度お試しください。"
      );
      event.target.value = ""; // clear the file input
      ableSubmitButton("loadingValidate", "uploadButton-validate");
      return;
    }
  } else {
    console.log("");
  }

  // Create an AbortController to handle disconnection
  const controller = new AbortController();
  const signal = controller.signal;

  // Listen for the disconnect event
  window.addEventListener("offline", () => {
    console.log("Internet connection lost, aborting fetch.");
    controller.abort();
  });
  fetch("/validate/upload", {
    method: "POST",
    body: formData,
    signal: signal,
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data.error);
        });
      }
      return response.json();
    })
    .then((data) => {
      // console.log("data:", data);
      const { result, url } = data;
      sumLengthSum = 0;
      result.forEach((item) => {
        sumLengthSum += item.summary.length;
        // console.log(item.summary.length);
      });
      if (sumLengthSum > 0) {
        displayUrl(url);
      }
      // console.log(result);
      handleResult(result);
    })
    .catch((error) => {
      if (error.name === "AbortError") {
        displayError(
          { message: "インターネット接続を確認してください。" },
          "error"
        );
      } else {
        displayError({ message: error.message }, "error");
      }
      handleResult();
    })
    .finally(() => {
      ableSubmitButton("loadingValidate", "uploadButton-validate");
    });
}

function handleUploadCompareExcel(event) {
  event.preventDefault();
  const currentTarget = event.currentTarget;
  var formData = new FormData(currentTarget);
  const getDataFile = formData.get("getDataFile"); // Returns a File object
  disableSubmitButton("loadingCompare", "uploadButton-compare");
  displayError("", "compare-error");
  displayUrl();
  handleResult();
  if (getDataFile) {
    console.log("getDataFile:", getDataFile);
    let fileSize = getDataFile.size;
    let formattedFileSize;
    if (fileSize >= 1024 * 1024) {
      formattedFileSize = (fileSize / (1024 * 1024)).toFixed(2) + " MB";
    } else if (fileSize >= 1024) {
      formattedFileSize = (fileSize / 1024).toFixed(2) + " KB";
    } else {
      formattedFileSize = fileSize + " bytes";
    }
    if (fileSize > 15 * 1024 * 1024) {
      alert(
        "予期せぬエラーが発生しました。\\nファイルの内容、インターネット接続を確認し、もう一度お試しください。"
      );
      event.target.value = ""; // clear the file input
      ableSubmitButton("loadingCompare", "uploadButton-compare");
      return;
    }
  } else {
    console.log("");
  }

  const controller = new AbortController();
  const signal = controller.signal;

  window.addEventListener("offline", () => {
    console.log("Internet connection lost, aborting fetch.");
    controller.abort();
  });
  fetch("/excel-compare/upload", {
    method: "POST",
    body: formData,
    signal: signal,
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data.error);
        });
      }
      return response.json();
    })
    .then((data) => {
      console.log("Received data:", data.data_results[0]); // Log the data to check its structure
      if (data && data.compare_results && data.compare_results.length > 0) {
        renderComparisonResults(data.compare_results[0]);
      } else {
        console.error("Unexpected data structure:" + JSON.stringify(data));
      }

      // Display user data, status, and message
      //           <p>Employee ID: ${data.data_results.user_data.employee_id}</p>
      if (data.data_results.length > 0) {
        const userDataDiv = document.getElementById("compare-result");
        userDataDiv.innerHTML = data.data_results
          .map(
            (result) => `
          <p>The user with Employee ID: ${
            result.user_data.employee_id
          } and Name: ${result.user_data.name} is ${
              result.status === "exists"
                ? "already exists"
                : "<span style='color: #b60005; font-weight: 500;'>added to database</span>"
            }</p>
        `
          )
          .join("");
        userDataDiv.style.display = "block";
      }
    })
    .catch((error) => {
      if (error.name === "AbortError") {
        displayError(
          { message: "インターネット接続を確認してください。" },
          "compare-error"
        );
      } else {
        displayError({ message: error.message }, "compare-error");
      }
      handleResult();
    })
    .finally(() => {
      ableSubmitButton("loadingCompare", "uploadButton-compare");
    });
}

function updateFileNameForValidateRoute(fileName, event) {
  const file = event.target.files[0];

  if (file.size > 15 * 1024 * 1024) {
    alert(
      "予期せぬエラーが発生しました。\\nファイルの内容、インターネット接続を確認し、もう一度お試しください。"
    );
    event.target.value = ""; // clear the file input
  }
  var fileInput = event.target;
  var activeLabel = document.getElementById(fileName);
  activeLabel.innerHTML =
    fileInput.files.length > 0
      ? Array.from(fileInput.files)
          .map(
            (file) =>
              `${file.name} (${
                file.size > 1024 * 1024
                  ? (file.size / 1024 / 1024).toFixed(2) + " MB"
                  : (file.size / 1024).toFixed(2) + " KB"
              })`
          )
          .join("<br>")
      : "ファイルが選択されていません";
  fileInput.files.length > 0
    ? Array.from(fileInput.files)
        .map((file) => file.name)
        .join("<br>")
    : "ファイルが選択されていません";
}

// Initialize the selected file on page load
document.addEventListener("DOMContentLoaded", function () {
  const defaultFile = document.getElementById("defaultFile").value;
  updateSelectedFile(defaultFile);
});

window.addEventListener("offline", (event) => {
  console.log("Internet connection lost");
  displayError({ message: "インターネット接続を確認してください。" });
  ableSubmitButton();
  // document.getElementById("tab3").style["pointer-events"] = "none";
});
window.addEventListener("online", (event) => {
  console.log("Internet connected");
  ableSubmitButton();
});
// function updateTemplateLink() {
//   var transport = document.querySelector(
//     'input[name="transport"]:checked'
//   ).value;
//   var templateLink = document.getElementById("template-link");
//   if (transport === "train") {
//     templateLink.href = "/download-template-navi-train";
//   } else if (transport == "car") {
//     templateLink.href = "/download-template-navi-car";
//   } else if (transport == "bus") {
//     templateLink.href = "/download-template-navi-bus";
//   } else if (transport == "walk") {
//     templateLink.href = "/download-template-navi-walk";
//   } else if (transport == "bike") {
//     templateLink.href = "/download-template-navi-bike";
//   } else if (transport == "plane") {
//     templateLink.href = "/download-template-navi-plane";
//   } else if (transport == "truck") {
//     templateLink.href = "/download-template-navi-truck";
//   }
// }
function renderComparisonResults(data) {
  // const excelUsersDiv = document.getElementById("excel-users");
  const usersNotFoundDiv = document.getElementById("users-not-found");
  const usersNotInExcelDiv = document.getElementById("users-not-in-excel");
  // const closestMatchesDiv = document.getElementById("closest-matches");

  // Clear previous content
  // excelUsersDiv.innerHTML = "";
  // usersNotFoundDiv.innerHTML = "";
  // usersNotInExcelDiv.innerHTML = "";
  // closestMatchesDiv.innerHTML = "";

  const jsonOutputDiv = document.getElementById("json-output");
  jsonOutputDiv.style.display = "block";

  // Render Excel Users
  // excelUsersDiv.innerHTML = "<h3>Excel Users</h3>";
  (data.excel_users || []).forEach((user) => {
    excelUsersDiv.innerHTML += `<p>Employee ID: ${user.employee_id}, Name: ${user.name}</p>`;
  });

  // Render Users Not Found in DB with Closest Matches
  // usersNotFoundDiv.innerHTML = "<h3>Users Not Found in DB</h3>";
  (data.users_not_found_in_db || []).forEach((user) => {
    usersNotFoundDiv.innerHTML += `<p><span style="color: #b60005; font-weight: 500;">申請者に社員番号: ${user.employee_id}、ユーザ名: ${user.name}</span>が見つかりません。 行: ${user.custom_row}</p>`;

    // Find and display the closest match for each user
    const closestMatch = (data.closest_matches || []).find(
      (match) => match.employee_id === user.employee_id
    );
    if (closestMatch && closestMatch.status === undefined) {
      usersNotFoundDiv.innerHTML += `
        <p class="closest-match">
          Did you mean: Employee ID: 
          <button 
            type="button" 
            title="Copy Employee ID" 
            onclick="addCopyButtonListeners()" 
            class="copy-btn" 
            data-clipboard-text="${closestMatch.employee_id}">
              ${closestMatch.employee_id}
              <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-copy">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
              <svg style="display: none;" xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-check">
                <path d="M20 6L9 17l-5-5" />
              </svg>
          </button> | 
          Name: 
          <button 
            type="button" 
            title="Copy Name" 
            onclick="addCopyButtonListeners()" 
            class="copy-btn" 
            data-clipboard-text="${closestMatch.name}">
              ${closestMatch.name} 
              <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-copy">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
              <svg style="display: none;" xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-check">
                <path d="M20 6L9 17l-5-5" />
              </svg>
          </button>
        </p>
        <br>
      `;
    } else if (closestMatch.status === "no_similar_user") {
      usersNotFoundDiv.innerHTML += `<p class="no-similar-user">No similar user found in database.</p><br>`;
    }
  });

  // Render Users Not in Excel
  // usersNotInExcelDiv.innerHTML = "<h3>Users Not in Excel</h3>";
  (data.users_not_in_excel || []).forEach((user) => {
    usersNotInExcelDiv.innerHTML += `<p class="not-in-excel">申請者リストに社員番号: ${user.employee_id}、ユーザ名: ${user.name}が見つかりません。</p>`;
  });
}
function addCopyButtonListeners() {
  const copyButtons = document.querySelectorAll(".copy-btn");

  copyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const textToCopy = this.getAttribute("data-clipboard-text");
      console.log("textToCopy:", textToCopy);
      navigator.clipboard
        .writeText(textToCopy)
        .then(() => {
          // Provide feedback to the user
          this.querySelector(".feather-check").style.display = "block";
          this.querySelector(".feather-copy").style.display = "none";
          setTimeout(() => {
            this.querySelector(".feather-check").style.display = "none";
            this.querySelector(".feather-copy").style.display = "block";
          }, 2000);
        })
        .catch((err) => {
          console.error("Failed to copy: ", err);
        });
    });
  });
}
