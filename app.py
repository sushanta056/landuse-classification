# app.py
import os
import tempfile
import numpy as np
import joblib
import rasterio
from flask import Flask, request, send_file, jsonify, render_template

MODEL_PATH = "xgb_model.joblib"  
OUT_FILENAME = "predicted_landuse.tif"

app = Flask(__name__)

# Load the model once at startup
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)
print("Loaded model:", MODEL_PATH)




def predict_geotiff(in_path, out_path):
    # Read the GeoTIFF and run prediction
    with rasterio.open(in_path) as src:
        meta = src.meta.copy()
        height, width = src.height, src.width
        band_count = src.count


        if band_count < 10:
            raise ValueError("10 bands of image (.tif file) is expected, band should be in the order B2, B3, B4, B5, B6, B7, B8A, B11, B12")


        feature_stack = src.read().astype("float32")

       

    valid_mask = np.any(np.isfinite(feature_stack) & (feature_stack != 0), axis=0)
    n_features = feature_stack.shape[0]
    flat = feature_stack.reshape(n_features, -1).T  # shape (H*W, 9)
    flat_preds = np.full((flat.shape[0],), fill_value=4, dtype=np.int32)
    valid_flat = valid_mask.reshape(-1)

    to_predict = flat[valid_flat]
    preds = model.predict(to_predict)
    flat_preds[valid_flat] = preds
    pred_map = flat_preds.reshape((height, width))

    out_meta = meta.copy()
    out_meta.update({
        "count": 1,
        "dtype": rasterio.uint8,
        "compress": "lzw"
    })
    with rasterio.open(out_path, "w", **out_meta) as dst:
        dst.write(pred_map.astype(rasterio.uint8), 1)


@app.route("/")
def index():
    # Serve the HTML upload form
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "tif" not in request.files:
        return jsonify({"error": "No 'tif' file sent"}), 400

    tif_file = request.files["tif"]
    if tif_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded file to temp file
    with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp_in:
        tmp_in_name = tmp_in.name
        tif_file.save(tmp_in_name)

    # ✅ Check file size (after saving to disk)
    file_size_mb = os.path.getsize(tmp_in_name) / (1024 * 1024)
    if file_size_mb > 100:
        os.remove(tmp_in_name)
        return jsonify({
            "error": f"File too large ({file_size_mb:.1f} MB). "
                     "Please upload raster smaller than 100 MB."
        }), 400

    tmp_out = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)
    tmp_out_name = tmp_out.name
    tmp_out.close()

    try:
        predict_geotiff(tmp_in_name, tmp_out_name)
        return send_file(tmp_out_name,
                         as_attachment=True,
                         download_name=OUT_FILENAME,
                         mimetype="image/tiff")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(tmp_in_name)
        except Exception:
            pass
        # keep tmp_out to let send_file complete



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
