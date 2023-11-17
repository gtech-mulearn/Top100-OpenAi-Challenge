// create a medical report db to sotrre the report(in string format)

const reportSchema = new mongoose.Schema({
    report: {
        type: String,
        required: true,
    },
    });

const Report = mongoose.model("Report", reportSchema);

module.exports = Report;
