const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let pyProc = null;
let win;

function createWindow() {
  win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
    },
  });

  win.loadURL("http://localhost:8501");

  win.on("closed", () => {
    win = null;
    if (pyProc) pyProc.kill();
  });
}

app.on("ready", () => {
  const pythonPath = "./python/python.exe"; 
  // let pythonPath;

  // if (process.env.NODE_ENV === "development") {
  //   // When running via npm start
  //   pythonPath = path.join(__dirname, "python", "python.exe");
  // } else {
  //   // When packaged
  //   pythonPath = path.join(process.resourcesPath, "python", "python.exe");
  // }
  
  pyProc = spawn(
    pythonPath,
    [ 
      "-m",
      "streamlit",
      "run",
      "app.py",
      "--server.port=8501",
      "--server.headless=true",
      "--server.address=localhost",
    ],
    { stdio: "inherit" }
  );

  setTimeout(createWindow, 12000); // wait longer
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
