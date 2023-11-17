import React, { useState, useRef } from "react";
import MicRecorder from "mic-recorder-to-mp3"; // Make sure to import the MicRecorder library
import axios from "axios";

const Recorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const recorder = useRef(new MicRecorder({ bitRate: 128 }));
  const [audioFiles, setAudioFiles] = useState([]);

  const startRecording = () => {
    recorder.current
      .start()
      .then(() => {
        setIsRecording(true);
      })
      .catch((e) => {
        console.error(e);
      });
  };

  const stopRecording = () => {
    recorder.current
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const file = new File(buffer, "music.mp3", {
          type: blob.type,
          lastModified: Date.now(),
        });

        const newAudioFiles = [...audioFiles, file];
        setAudioFiles(newAudioFiles);
        setIsRecording(false);
      })
      .catch((e) => {
        console.error(e);
      });
  };

  const handleButtonClick = () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("file", audioFiles[audioFiles.length - 1]); // Assuming the latest file is to be sent

    axios
      .post("http://localhost:4002/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        // Handle successful upload
        console.log("File uploaded:", response);
      })
      .catch((error) => {
        // Handle error
        console.error("Error uploading file:", error);
      });
  };

  return (
    <div className="btn-container">
      <button onClick={handleButtonClick} className="text-white">
        {isRecording ? "Stop recording" : "Start recording"}
      </button>
      <ul id="playlist">
        {audioFiles.map((file, index) => (
          <li key={index}>
            <audio controls src={URL.createObjectURL(file)} />
          </li>
        ))}
      </ul>

      <button onClick={handleUpload} className="text-white m-5">
        Upload Last Recording
      </button>
    </div>
  );
};

export default Recorder;
