const express = require('express');
const { spawn } = require('child_process');
const app = express();
const multer = require('multer');
const fs = require("fs");
const path = require("path");

app.use(express.json());
app.use(express.static(path.join(__dirname, 'compressed_files')));

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, './uploads')
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
        cb(null, file.fieldname + '-' + uniqueSuffix + ".txt")
    }
});
  
const upload = multer({ storage: storage });

app.post('/compress', upload.single('file'), (req, res) => {
    console.log(req.file);
    const fileOriginalSize = Number(req.file.size);
    let fileName = req.file.filename;
    const fileDestination = req.file.destination;
    const fileData = fs.readFileSync(`${fileDestination}/${fileName}`, {encoding:'utf8'});
    pythonProcess = spawn('python', ['lzw_str.py',fileData]);

    pythonProcess.stdout.on('data', (data) => {
        console.log("stdout: " + data);
        fileName = fileName.split(".")[0].toString();
        fs.appendFileSync(`./compressed_files/${fileName}.lzm`, data, function (err) {
            if (err) throw err;
        }); 
        const fileStats = fs.statSync(`./compressed_files/${fileName}.lzm`);
        const ratio = (Number(fileStats.size) / Number(fileOriginalSize) * 100).toFixed(2);
        console.log(`Ratio of compression: ${ratio}%`);
        const fullUrl = req.protocol + '://' + req.get('host') + "/" + fileName + ".lzm";
        return res.status(200).send({ compressedFileLink: fullUrl, compressedData: data.toString(), ratio: ratio});
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        return res.status(500).send('An error occurred');
    });

    // Handle the Python process finishing
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

app.listen(3000, () => {
    console.log("Server listening on port 3000");
});