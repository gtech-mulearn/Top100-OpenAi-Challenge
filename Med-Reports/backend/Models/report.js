// create a medical report db to sotrre the report(in string format)

import mongoose from "mongoose";

const reportSchema = new mongoose.Schema({
    report: {
        type: String,
        required: true,
    },
    });

const Report = mongoose.model("Report", reportSchema);

export default Report;