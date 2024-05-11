const fs = require("fs");
const path = require("path");

// Function to escape double curly braces in a string
function escapeCurlyBraces(str) {
  return str.replace(/{{/g, "\\{{").replace(/}}/g, "\\}}");
}

// Function to process a single file
function processFile(filePath) {
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error(`Error reading file: ${filePath}`);
      return;
    }
    const escapedData = escapeCurlyBraces(data);
    fs.writeFile(filePath, escapedData, "utf8", (err) => {
      if (err) {
        console.error(`Error writing file: ${filePath}`);
        return;
      }
      console.log(`Processed file: ${filePath}`);
    });
  });
}

// Function to process all markdown files in a directory
function processDirectory(dirPath) {
  fs.readdir(dirPath, (err, files) => {
    if (err) {
      console.error(`Error reading directory: ${dirPath}`);
      return;
    }
    files.forEach((file) => {
      const filePath = path.join(dirPath, file);
      fs.stat(filePath, (err, stats) => {
        if (err) {
          console.error(`Error reading file stats: ${filePath}`);
          return;
        }
        if (stats.isDirectory()) {
          processDirectory(filePath);
        } else if (file.endsWith(".md")) {
          processFile(filePath);
        }
      });
    });
  });
}

// Start processing from the root directory
const rootDir = "./";
processDirectory(rootDir);
