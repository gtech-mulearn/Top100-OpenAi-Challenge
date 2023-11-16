
const express=require('express');
const dotenv=require('dotenv');

dotenv.config();
const app=express();

app.use(express.json());
app.use(express.urlencoded({extended:true}));

const multer = require('multer');
const upload = multer({dest:'uploads/'});

// upload mp3 file
app.post('/upload',upload.single('file'),(req,res)=>{
    console.log(req.file);
    res.send('Single file upload');
});

app.listen(3000,()=>console.log('Server started at port:3000'));
