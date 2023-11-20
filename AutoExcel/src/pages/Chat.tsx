import  { useState } from 'react'
import Industry from '../components/Industry'
import '../styles/Chat.css'
import Fab from '@mui/material/Fab';
import MicIcon from '@mui/icons-material/Mic';
import '../styles/Chat.css'
import axios from 'axios';






export default function Chat() {

    const [prompt,setPrompt] = useState('')

    const [industry, setIndustry] = useState(() => {
        const storedIndustry = localStorage.getItem('industry');
        return storedIndustry || ''; // Set default value if 'industry' is not in local storage
      });

    function postData() {
      console.log("hit")
        const data = {context: industry,columns:'yourColumn' ,data: prompt}
        axios.post('http://localhost:8000/openai',  data )
          .then(response => {
            // Handle the response if needed
            console.log(response.data);
          })
          .catch(error => {
            // Handle errors
            console.error('Error sending POST request:', error);
          }).then(()=>{setPrompt("")}) ;
         
    

    const [industryPage, setIndustryPage] = useState(true);
  return (
    <div className='chat-base'>
      {industryPage&&<Industry onClose={()=>{setIndustryPage(false)}}/>}
      <div className='text-area-container'>
        <textarea className='text-area'  placeholder="Type your prompt here." onChange={(e)=>{setPrompt(e.target.value)}} value={prompt}/>
       <button onClick={postData} >send</button>
        <Fab color="primary" aria-label="voice-recognition" className='voice-icon'>
          <MicIcon />
        </Fab>
      </div>
    </div>
  )
}
}