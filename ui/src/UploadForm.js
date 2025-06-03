import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
    const [image, setImage] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);
    const [hsv, setHSV] = useState({
        h_min: 85,
        h_max: 135,
        s_min: 30,
        s_max: 255,
        v_min: 20,
        v_max: 255,
    });

    const handleChange = (e) => {
        setHSV({ ...hsv, [e.target.name]: e.target.value });
    };

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append("image", image);
        Object.entries(hsv).forEach(([k, v]) => formData.append(k, v));

        const res = await axios.post(
            "http://localhost:5000/process",
            formData,
            {
                responseType: "blob",
            }
        );

        setProcessedImage(URL.createObjectURL(res.data));
    };

    return (
        <div>
            <input type="file" onChange={handleImageChange} />
            {Object.keys(hsv).map((key) => (
                <div key={key}>
                    <label>{key}</label>
                    <input
                        type="range"
                        name={key}
                        min={key.includes("h") ? 0 : 0}
                        max={key.includes("h") ? 179 : 255}
                        value={hsv[key]}
                        onChange={handleChange}
                    />
                </div>
            ))}
            <button onClick={handleSubmit}>Process Image</button>

            {processedImage && <img src={processedImage} alt="Result" />}
            <a href="http://localhost:5000/download" download>
                <button className="btn btn-success">
                    Download Processed Image
                </button>
            </a>
            <Histogram image={processedImage} />
        </div>
    );
}

export default UploadForm;
