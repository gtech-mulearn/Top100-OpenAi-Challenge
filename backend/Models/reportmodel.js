import mongoose from "mongoose";

const itemSchema = mongoose.Schema(
  {
    report: {
      type: String,
      required: true,
    }
})
export const Report = mongoose.model("reportSchema", reportSchema);