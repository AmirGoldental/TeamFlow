const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true, // Allow Node.js integration
      contextIsolation: false, // For Electron 12+
    }
  });

  win.loadFile('index.html');
  win.webContents.openDevTools(); // Open DevTools

}

app.whenReady().then(createWindow);
