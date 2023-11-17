import express from "express";
// import cors from "cors"
// import cors
//connnect to database

// const dotenv=require('dotenv');
import { createRequire } from "module";
import { config } from "dotenv";
import OpenAI from "openai";
import { createReadStream } from "fs";
import { log } from "console";


const require = createRequire(import.meta.url);
const cors = require("cors");
const multer = require("multer");
const mongoose = require("mongoose");
import Report from "./models/report.js";
config();
const model = "whisper-1";
const openai = new OpenAI({
  apiKey: process.env.OpenAI_API_KEY 
});

// dotenv.config();
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname + ".mp3");
  },
});

const upload = multer({ storage: storage, preservePath: true });

// upload mp3 file
let filename;
let data;
let answer;

//connect to database
const dbURI = process.env.MONGODB_URI;
mongoose
  .connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then((result) => app.listen(4002))
  .catch((err) => console.log(err));


app.post("/upload", upload.single("file"), async (req, res) => {
  console.log(req.file);
  res.send(`${req.file.path}`);

  filename = `./${req.file.path}`;

  data = await audioFn(filename);
  res.send(data);
});

// save report to database
app.post("/report", async(req, res) => {
  const report =  await new Report({
    report:  answer,
  });
  report
    .save()
    .then((result) => {
      console.log(result);
      res.send(result);
    })
    .catch((err) => console.log(err));
});

// get report from database
app.get("/report", (req, res) => {
  Report.find()
    .then((result) => {
      res.send(result);
    })
    .catch((err) => {
      console.log(err);
    });
});



app.listen(4003, () => {
  console.log("hi running");
});

// *********************************************************

// Whisper api
async function audioFn(filename) {
  const transcription = await openai.audio.transcriptions.create({
    file: createReadStream(filename),
    model: model,
    language: "en",
    temperature: 0.2,
  });

  console.log(transcription);

  //askQuestion returns a promise
  let answer = askQuestion(
    transcription.text +
      "imagine yourself as the best medical scriber in the world.Now you should creat a medical report with the following Sections. Objectives,introduction,patient history,assessment of current diagnosis(if provided only),treatment methadology,prognosis,closing.The above sections should be an object with key as section and values as respective section values"
  );
  //findAnswer take in a promise and resolve the promise
  findAnswer(answer);
}

function askQuestion(question) {
  // returns a promise
  let pr = openai.chat.completions.create({
    messages: [{ role: "user", content: question }],
    model: "gpt-3.5-turbo",
  });

  return pr;
}

function findAnswer(promise) {
  promise
    .then((data) => {
      let res = data.choices[0].message.content;
      answer = res;
      console.log(res);
      return res;
    })
    .catch((err) => {
      console.log("Oops Something went wrong");
      console.log(err);
    });
}
