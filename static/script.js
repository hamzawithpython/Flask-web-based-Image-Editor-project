const fileInput = document.querySelector(".file-input"),
  filterOptions = document.querySelectorAll(".filter button"),
  editOptions = document.querySelectorAll(".edit button"),  // New selector for edit buttons
  filterName = document.querySelector(".filter-info .name"),
  filterValue = document.querySelector(".filter-info .value"),
  filterSlider = document.querySelector(".slider input"),
  rotateOptions = document.querySelectorAll(".rotate button"),
  previewImg = document.querySelector(".preview-img img"),
  resetFilterBtn = document.querySelector(".reset-filter"),
  chooseImgBtn = document.querySelector(".choose-img"),
  saveImgBtn = document.querySelector(".save-img");

let brightness = "100", saturation = "100", inversion = "0", grayscale = "0";
let rotate = 0, flipHorizontal = 1, flipVertical = 1;
let currentFilter = "";  // Track the current filter applied
let processedImageURL = "";  // Save the processed image URL after filter is applied

// Helper function to disable/enable buttons
const toggleControls = (state) => {
  filterOptions.forEach(option => option.disabled = !state);  // Disable filter buttons during processing
  editOptions.forEach(option => option.disabled = state);  // Enable edit buttons after filter is applied
  rotateOptions.forEach(option => option.disabled = false);  // Rotate & flip are always enabled
  saveImgBtn.disabled = state;  // Enable save button after filter
  resetFilterBtn.disabled = state;  // Enable reset button after filter
  chooseImgBtn.disabled = !state;  // Enable choose image button
}

// Load image from file input and display in preview
const loadImage = () => {
  let file = fileInput.files[0];
  if (!file) return;
  previewImg.src = URL.createObjectURL(file);  // Load the image for preview
  previewImg.addEventListener("load", () => {
    resetFilterBtn.click();  // Reset all filters and edits
    document.querySelector(".container").classList.remove("disable");
    currentFilter = "";  // Clear current filter
    processedImageURL = previewImg.src;  // Save original image URL
    toggleControls(true);  // Re-enable controls after image is loaded
  });
}

// Apply filters using backend processing
const applyFilterBackend = (filterName) => {
  const formData = new FormData();
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload an image first!");
    return;
  }

  formData.append("file", file);
  formData.append("operation", filterName);  // The filter to be applied

  // Show a loading spinner and disable controls
  previewImg.src = "path_to_loading_spinner.gif";  // Replace with your loading spinner image
  toggleControls(false);  // Disable all controls except choosing a new image

  // Send the AJAX request to the Flask backend
  fetch("/edit", {
    method: "POST",
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      if (data.processed_image_url) {
        processedImageURL = data.processed_image_url;  // Save the processed image URL
        previewImg.src = processedImageURL;  // Update the preview image with the processed one
        currentFilter = filterName;  // Set the current filter
        applyEdits();  // Apply existing brightness, saturation, etc., to the processed image
      } else {
        alert("Failed to apply filter.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Error applying filter.");
    })
    .finally(() => {
      toggleControls(true);  // Re-enable controls after the image is processed
    });
}

// Filter button click event listeners
filterOptions.forEach(option => {
  option.addEventListener("click", () => {
    if (currentFilter) {
      alert("You can only apply one filter. Reset or upload a new image to apply a different filter.");
      return;
    }

    document.querySelector(".filter .active").classList.remove("active");
    option.classList.add("active");

    // Apply the filter via the backend
    applyFilterBackend(option.value);  // Use the filter value, e.g., "mnc", "crd", "anm", "rtr"
  });
});

// Apply current edit settings (brightness, saturation, etc.) and transformations (rotate, flip)
const applyEdits = () => {
  // Apply transformations and filters on top of the current processed image
  previewImg.style.transform = `rotate(${rotate}deg) scale(${flipHorizontal}, ${flipVertical})`;
  previewImg.style.filter = `brightness(${brightness}%) saturate(${saturation}%) invert(${inversion}%) grayscale(${grayscale}%)`;
}

// Slider only for edit buttons (brightness, saturation, etc.)
editOptions.forEach(option => {
  option.addEventListener("click", () => {
    document.querySelector(".edit .active").classList.remove("active");
    option.classList.add("active");
    filterName.innerText = option.innerText;

    // Set slider max value and current value based on selected edit
    if (option.id === "brightness") {
      filterSlider.max = "200";
      filterSlider.value = brightness;
      filterValue.innerText = `${brightness}%`;
    } else if (option.id === "saturation") {
      filterSlider.max = "200";
      filterSlider.value = saturation;
      filterValue.innerText = `${saturation}%`
    } else if (option.id === "inversion") {
      filterSlider.max = "100";
      filterSlider.value = inversion;
      filterValue.innerText = `${inversion}%`;
    } else {
      filterSlider.max = "100";
      filterSlider.value = grayscale;
      filterValue.innerText = `${grayscale}%`;
    }
  });
});

// Update edit values and apply changes when slider input changes
const updateEdits = () => {
  filterValue.innerText = `${filterSlider.value}%`;
  const selectedEdit = document.querySelector(".edit .active");
  if (selectedEdit.id === "brightness") {
    brightness = filterSlider.value;
  } else if (selectedEdit.id === "saturation") {
    saturation = filterSlider.value;
  } else if (selectedEdit.id === "inversion") {
    inversion = filterSlider.value;
  } else {
    grayscale = filterSlider.value;
  }
  applyEdits();  // Apply updated edit settings
}

// Set up event listeners for slider (only for edit options)
filterSlider.addEventListener("input", updateEdits);

// Set up rotation and flip buttons
rotateOptions.forEach(option => {
  option.addEventListener("click", () => {
    if (option.id === "left") {
      rotate -= 90;
    } else if (option.id === "right") {
      rotate += 90;
    } else if (option.id === "horizontal") {
      flipHorizontal = flipHorizontal === 1 ? -1 : 1;
    } else {
      flipVertical = flipVertical === 1 ? -1 : 1;
    }
    applyEdits();  // Apply the updated rotation/flip
  });
});

// Reset all filters and transformations to default values
const resetFilter = () => {
  brightness = "100"; saturation = "100"; inversion = "0"; grayscale = "0";
  rotate = 0; flipHorizontal = 1; flipVertical = 1;
  editOptions[0].click();  // Reset to default edit option
  currentFilter = "";  // Allow applying filters again
  previewImg.src = processedImageURL || fileInput.src;  // Reset to the last filtered image or original image
  applyEdits();  // Apply default settings
}

// Save the current image with applied edits and transformations
const saveImage = () => {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = previewImg.naturalWidth;
  canvas.height = previewImg.naturalHeight;
  ctx.filter = `brightness(${brightness}%) saturate(${saturation}%) invert(${inversion}%) grayscale(${grayscale}%)`;
  ctx.translate(canvas.width / 2, canvas.height / 2);
  if (rotate !== 0) {
    ctx.rotate(rotate * Math.PI / 180);
  }
  ctx.scale(flipHorizontal, flipVertical);
  ctx.drawImage(previewImg, -canvas.width / 2, -canvas.height / 2, canvas.width, canvas.height);
  const link = document.createElement("a");
  link.download = "image.jpg";
  link.href = canvas.toDataURL();
  link.click();
}

// Set up event listeners
resetFilterBtn.addEventListener("click", resetFilter);
saveImgBtn.addEventListener("click", saveImage);
fileInput.addEventListener("change", loadImage);
chooseImgBtn.addEventListener("click", () => fileInput.click());
