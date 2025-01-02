import React, {useEffect, useState} from "react";
import "../App.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import TimePicker from "../components/TimePicker.tsx";
import "./CameraHistory.css"
import Header from "../components/Header.tsx";
import ImageWithSpinner from "../components/ImageWithSpinner.tsx";

function CameraHistory() {
    const [imageFiles, setImageFiles] = useState<string[]>([]);
    const [selectedFile, setSelectedFile] = useState<string>("");
    const [date, setDate] = useState(new Date());
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let url = "/api/webcam/todays_images";
        if ("localhost" === window.location.hostname) {
            url = "http://localhost:5040/api/webcam/todays_images";
        }
        fetch(url).then(response => response.json()).then((data) => {
            console.log("todays images", data.todays_images);
            setImageFiles(data.todays_images);
            setLoading(false);
        })
    }, [date]);

    let imageFileLinks = [];
    for (let file of imageFiles) {
        const filename = file.split("/").pop();
        let datetimeStr = filename?.split("_")[0].replace(".jpg", "");
        if (datetimeStr) {
            let parts = datetimeStr.split("T");
            datetimeStr = parts[0] + " " + parts[1].replace(/-/g, ":");

        }

        let url = "/api/webcam/key/" + filename;
        if ("localhost" === window.location.hostname) {
            url = "http://localhost:5040/api/webcam/key/" + filename;
        }

        imageFileLinks.push(<li key={file}>
            <a href={url}>
                {datetimeStr}
            </a>
        </li>)
    }

    let timestamps = []
    for (let file of imageFiles) {
        const filename = file.split("/").pop();
        let datetimeStr = filename?.split("_")[0].replace(".jpg", "");
        if (datetimeStr) {
            let parts = datetimeStr.split("T");
            datetimeStr = parts[0] + " " + parts[1].replace(/-/g, ":");
        }
        timestamps.push(datetimeStr)
    }

    function onTimeChange(index: number) {
        setSelectedFile(imageFiles[index]);
    }

    if(loading){
        return <h1>Loading...</h1>
    }

    const isMobile = window.innerWidth < 800;

    console.log(imageFiles)
    let filename: string | undefined = "";
    if (selectedFile === undefined || selectedFile === "") {
        filename = imageFiles[0].split("/").pop();
    } else {
        filename = selectedFile.split("/").pop();
    }
    let src = "/api/webcam/key/" + filename;
    console.log(src)
    if ("localhost" === window.location.hostname) {
        src = "http://localhost:5040/api/webcam/key/" + filename;
    }

    return (
        <>
            <Header/>
            <div id="image-picker" className={isMobile ? "mobile" : ""}>
                <div id="image-picker-dp">
                    <DatePicker
                        selected={date}
                        onChange={(date) => {
                            if (date === null) return;
                            setDate(date);
                        }}
                    />
                </div>

                <TimePicker timestamps={timestamps} onChange={onTimeChange}/>
            </div>
            <ImageWithSpinner key={src} src={src} alt="webcam image" />
        </>
    );
}

export default CameraHistory;
