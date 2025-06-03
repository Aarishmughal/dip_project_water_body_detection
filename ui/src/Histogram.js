import { Bar } from "react-chartjs-2";

function Histogram({ data }) {
    const chartData = {
        labels: Array.from({ length: 256 }, (_, i) => i),
        datasets: [
            {
                label: "Pixel Intensity Frequency",
                data: data,
                backgroundColor: "rgba(54, 162, 235, 0.6)",
            },
        ],
    };

    return <Bar data={chartData} />;
}
export default Histogram;
