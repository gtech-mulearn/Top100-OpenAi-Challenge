import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import { useTypewriter } from 'react-simple-typewriter';
import '../styles/Upload.css'; // Import your CSS file
import TextField from '@mui/material/TextField';
import { Input } from 'semantic-ui-react'

interface UploadProps {}

const Upload: React.FC<UploadProps> = () => {
  const navigate = useNavigate();

  const inputStyle = {
    "&::placeholder": {
      color: '#yourPlaceholderColor', // Set the color of the placeholder text
    },
  };

  const [text] = useTypewriter({
    words: ['Auto', 'Simple', 'Easy', 'Anytime', 'Generate...'],
    loop: true,
    delaySpeed: 2500,
  });

  return (
    <>
      <div className="upload-container">
      <img src={logo} alt="Logo" className="logo" />
        <div>
          <span className='typing'>
            Excel {text}
          </span>
        </div>
        <div>
          {/* Add any other elements or content as needed */}
        </div>
        <input className="link" type="text" placeholder="Enter your excel sheet link...."/>
        <button className='btn1' onClick={() => navigate('/chat')}>Submit</button>
      </div>
    </>
  );
};

export default Upload;
