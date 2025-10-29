document.addEventListener("DOMContentLoaded", () => {
    const tifInput = document.getElementById("tifInput");
    const predictBtn = document.getElementById("predictBtn");
    const fileNameDisplay = document.getElementById("fileName");
    const status = document.getElementById("status");

    // Enable predict button when file is selected
    tifInput.addEventListener("change", () => {
        if (tifInput.files.length > 0) {
            predictBtn.disabled = false;
            fileNameDisplay.textContent = tifInput.files[0].name;
        } else {
            predictBtn.disabled = true;
            fileNameDisplay.textContent = "No file selected";
        }
        status.textContent = "";
    });

    // Handle Predict button click
    predictBtn.addEventListener("click", () => {
        if (tifInput.files.length === 0) return;

        const file = tifInput.files[0];
        const formData = new FormData();
        formData.append("tif", file);

        status.textContent = "⏳ Uploading and predicting... please wait";
        predictBtn.disabled = true;

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(res => {
            if (!res.ok) {
                // Server returned an error
                return res.json().then(err => { throw new Error(err.error) });
            }
            return res.blob();
        })
        .then(blob => {
            // Download the predicted GeoTIFF
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "predicted_landuse.tif";
            document.body.appendChild(a);
            a.click();
            a.remove();
            status.textContent = "✅ Prediction completed! File downloaded.";
        })
        .catch(err => {
            console.error(err);
            status.textContent = "❌ Error: " + err.message;
        })
        .finally(() => {
            predictBtn.disabled = false;
        });
    });
});
