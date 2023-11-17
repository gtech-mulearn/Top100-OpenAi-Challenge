// import React,{useState} from "react";
// // import AudioTimer from "./AudioTimer";
// import { ReactMic } from "react-mic";
// import axios from "axios";

// const ReactRecorder = () => {
//   // const [isRunning, setIsRunning] = React.useState(false);
//   // const [elapsedTime, setElapsedTime] = React.useState(0);
//   const [img, setImg]=useState("off.gif")
//   const [voice, setVoice] = React.useState(false);
//   const [recordBlobLink, setRecordBlobLink] = React.useState(null);


//   const onStop = async (recordedBlob) => {
//     setRecordBlobLink(recordedBlob.blobURL);
//     // setIsRunning(false);
//     const mediaBlob = await fetch(recordBlobLink)
//     .then(response => response.blob());

// const myFile = new File(
//     [mediaBlob],
//     "demo.mp4",
//     { type: 'video/mp4' }
// );
// const formData = new FormData();
// formData.append("file", myFile);

// await axios
//   .post("http://localhost/upload", formData, {
//     headers: { "Content-Type": "multipart/form-data" },
//   })
//   .then(() => {
//     console.log("success");
//   })
//   .catch((err) => {
//     console.log(err);
//   });
//   }
//   const startHandle = () => {
//     // setElapsedTime(0);
//     // setIsRunning(true);
//     setVoice(true);
//     setImg("loading.png")
//   };
//   const stopHandle = () => {
//     // setIsRunning(false);
//     setVoice(false);
//     setImg("off.gif")

//   };

//   const clearHandle = () => {
//     // setIsRunning(false);
//     setVoice(false);
//     setRecordBlobLink(false);
//     // setElapsedTime(0);
//   };

//   return (
//     <div className="micwave">
//       {/* <div className="micwave"> */}
//         {/* <h2>Audio Recorder</h2> */}
//         {/* <AudioTimer
//           isRunning={isRunning}
//           elapsedTime={elapsedTime}
//           setElapsedTime={setElapsedTime}
//         /> */}
//         <img src={`./images/${img}`} alt="" />

//         <ReactMic
//           record={voice}
//           className="wave"
//           onStop={onStop}
//           // strokeColor="#000000"
//           // backgroundColor="#FF4081"
//         />
//         <div className="btn-container">
//           {recordBlobLink ? (
//             <button 
//               onClick={clearHandle}
//               className="micbtn"
//             >
//               {" "}
//               Clear{" "}
//             </button>
//           ) : (
//             ""
//           )}
//         </div>
//         <div className="btn-container">
//           {!voice ? (
//             <button
//               onClick={startHandle}
//               className="micbtn"
//             >
//               Start
//             </button>
//           ) : (
//             <button
//               onClick={stopHandle}
//               className="micbtn"
//             >
//               Stop
//             </button>
//           )}
//         </div>
//         <div className="">
//           {/* {recordBlobLink ? (
//             <audio controls src={recordBlobLink} className="mt-6" />
//           ) : (
//             ""
//           )} */}
//         </div>
//       </div>
//     // </div>
//         );
  
//         }
// export default ReactRecorder;



import React, { useState, useRef } from 'react';
import MicRecorder from 'mic-recorder-to-mp3'; // Make sure to import the MicRecorder library
import axios from 'axios';

const Recorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const recorder = useRef(new MicRecorder({ bitRate: 128 }));
  const [audioFiles, setAudioFiles] = useState([]);

  const startRecording = () => {
    recorder.current.start().then(() => {
      setIsRecording(true);
    }).catch((e) => {
      console.error(e);
    });
  };

  const stopRecording = () => {
    recorder.current.stop().getMp3().then(([buffer, blob]) => {
      const file = new File(buffer, 'music.mp3', {
        type: blob.type,
        lastModified: Date.now()
      });

      const newAudioFiles = [...audioFiles, file];
      setAudioFiles(newAudioFiles);
      setIsRecording(false);
    }).catch((e) => {
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
    formData.append('file', audioFiles[audioFiles.length - 1]); // Assuming the latest file is to be sent

    axios.post('http://localhost:4000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((response) => {
      // Handle successful upload
      console.log('File uploaded:', response);
    })
    .catch((error) => {
      // Handle error
      console.error('Error uploading file:', error);
    });
  };

  return (
    <div>
      <button onClick={handleButtonClick} className='text-white'>
        {isRecording ? 'Stop recording' : 'Start recording'}
      </button>
      <ul id="playlist">
        {audioFiles.map((file, index) => (
          <li key={index}>
            <audio controls src={URL.createObjectURL(file)} />
          </li>
        ))}
      </ul>

      <button onClick={handleUpload} className='text-white m-5'>
        Upload Last Recording
      </button>
    </div>
  );
};

export default Recorder;
