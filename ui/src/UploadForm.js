import { useState, useRef } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap-icons/font/bootstrap-icons.css";
function UploadForm() {
    const [image, setImage] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);
    const [showEdges, setShowEdges] = useState(false);
    const imageSrc = showEdges
        ? "http://localhost:5000/edges"
        : "http://localhost:5000/processed";

    const [hsv, setHSV] = useState({
        h_min: 85,
        h_max: 135,
        s_min: 30,
        s_max: 255,
        v_min: 20,
        v_max: 255,
    });

    const debounceRef = useRef(null);

    const processImage = async (img = image, hsvVals = hsv) => {
        if (!img) return;
        const formData = new FormData();
        formData.append("image", img);
        Object.entries(hsvVals).forEach(([k, v]) => formData.append(k, v));
        const res = await axios.post(
            "http://localhost:5000/process",
            formData,
            { responseType: "blob" }
        );
        setProcessedImage(URL.createObjectURL(res.data));
    };

    const handleChange = (e) => {
        const newHSV = { ...hsv, [e.target.name]: e.target.value };
        setHSV(newHSV);
        if (debounceRef.current) clearTimeout(debounceRef.current);
        debounceRef.current = setTimeout(() => {
            processImage(image, newHSV);
        }, 0);
    };

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
        processImage(e.target.files[0], hsv);
    };

    const handleSubmit = () => {
        processImage();
    };

    return (
        <div className="container py-4">
            <h2 className="mb-4 display-1">Water Body Detection</h2>

            <div className="mb-3">
                <label className="form-label">Select Image</label>
                <input
                    type="file"
                    className="form-control"
                    onChange={handleImageChange}
                />
            </div>

            <div className="row">
                {Object.keys(hsv).map((key) => {
                    let label = key.includes("h")
                        ? "Hue"
                        : key.includes("s")
                        ? "Saturation"
                        : "Value";
                    let tooltip =
                        label === "Hue"
                            ? "Controls the color shade (0-179). Adjust to select the color range for water detection."
                            : label === "Saturation"
                            ? "Controls the intensity of the color (0-255). Lower values mean more gray, higher values mean more vivid color."
                            : "Controls the brightness (0-255). Lower values are darker, higher values are brighter.";
                    return (
                        <div className="col-md-6 mb-3" key={key}>
                            <label className="form-label d-flex align-items-center gap-2">
                                {label} ({hsv[key]})
                                <i
                                    className="bi bi-info-circle"
                                    style={{
                                        cursor: "pointer",
                                        color: "#0d6efd",
                                    }}
                                    title={tooltip}
                                ></i>
                            </label>
                            <input
                                type="range"
                                className="form-range"
                                name={key}
                                min={key.includes("h") ? 0 : 0}
                                max={key.includes("h") ? 179 : 255}
                                value={hsv[key]}
                                onChange={handleChange}
                            />
                        </div>
                    );
                })}
            </div>

            <div className="d-flex gap-3 mb-4">
                <button className="btn btn-primary" onClick={handleSubmit}>
                    Process Image
                </button>

                <a href="http://localhost:5000/download" download>
                    <button className="btn btn-success">
                        Download Processed Image
                    </button>
                </a>

                <button
                    className="btn btn-warning"
                    onClick={() => setShowEdges(!showEdges)}
                >
                    {showEdges ? "Show Normal View" : "Show Edge View"}
                </button>
            </div>

            <div className="row">
                {processedImage && (
                    <div className="col-md-6 mb-4">
                        <h5>Processed Image</h5>
                        <img
                            src={processedImage}
                            alt="Processed"
                            className="img-fluid rounded border"
                        />
                    </div>
                )}
                {processedImage && (
                    <div className="col-md-6 mb-4">
                        <h5>{showEdges ? "Edge View" : "Normal View"}</h5>
                        <img
                            src={imageSrc}
                            alt="Toggle View"
                            className="img-fluid rounded border"
                        />
                    </div>
                )}
            </div>
        </div>
    );
}

export default UploadForm;
