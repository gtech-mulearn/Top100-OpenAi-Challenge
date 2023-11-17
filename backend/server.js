
import express from "express"
// import cors from "cors"
// import cors


// const dotenv=require('dotenv');
import { createRequire } from "module";
import {config} from "dotenv";
import OpenAI from 'openai';
import {createReadStream} from "fs"

const require = createRequire(import.meta.url);
const cors = require('cors')
const multer = require('multer')

config()
const model = "whisper-1"
const openai = new OpenAI({
  apiKey: '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',
});


// dotenv.config();
const app=express();

app.use(express.json());
app.use(express.urlencoded({extended:true}));
app.use(cors())



const upload = multer({dest:'uploads/'});

// upload mp3 file
app.post('/upload',upload.single('file'),(req,res)=>{
    console.log(req.file);
    res.send('Single file upload');  
})
app.listen(4000,()=>console.log('Server started at port:3000'));

// *********************************************************






audioFn();



// Whisper api
async function audioFn(){
    const transcription = await openai.audio.transcriptions.create({
    file : createReadStream("./audio.m4a"),
    model : model,
    language:"en",
    temperature:0.2
  })
 
  
  
  //askQuestion returns a promise
  let answer = askQuestion(transcription.text + "imagine yourself as the best medical scriber in the world.Now you should creat a medical report with the following Sections. Objectives,introduction,patient history,assessment of current diagnosis(if provided only),treatment methadology,prognosis,closing.The above sections should be an object with key as section and values as respective section values");
  //findAnswer take in a promise and resolve the promise
  findAnswer(answer);
  
  }

function askQuestion(question){
     // returns a promise
    let pr = openai.chat.completions.create({
        messages: [{ role: 'user', content: question }],
        model: 'gpt-3.5-turbo',
    })

    return pr 
  }

  function findAnswer(promise){
    
    promise.then((data)=>{
       
      let res =  data.choices[0].message.content;
      console.log(res);
      
          
      })
      .catch((err) =>{
        console.log("Oops Something went wrong");
        console.log(err);
      })
  }

 
