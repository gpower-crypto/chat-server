const express = require("express");
const { spawn } = require("child_process");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;

// Middleware to parse JSON requests
app.use(bodyParser.json());

app.post("/message", (req, res) => {
  const userMessage = req.body.message;

  // Log the user's command text in the console
  console.log(`User command received: ${userMessage}`);

  // Spawn a child process to execute the Python script
  const pythonProcess = spawn("py", ["chat.py", userMessage]);

  // Capture the output of the Python script
  let pythonOutput = "";
  pythonProcess.stdout.on("data", (data) => {
    pythonOutput += data.toString();
  });

  // Handle the end of the Python process
  pythonProcess.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);

    // Send the Python script's output back to the C++ application
    res.json({
      response: `Python Output: ${pythonOutput}`,
    });
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
