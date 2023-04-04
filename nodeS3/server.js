const aws = require('aws-sdk')
const express = require('express')
const multer = require('multer')
const multerS3 = require('multer-s3')
const app = express()
const bodyParser = require('body-parser');

app.use(bodyParser.json())

const s3 = new aws.S3({
    accessKeyId: "ASIAUIOYHLNDF6Y5XHJZ",
    secretAccessKey: "sFh2322C3Mfx/v6VnFzuEtJtP+GglSxguXY9/DYY",
    Bucket: "an516658-bucket"
})

const upload = multer({
    storage: multerS3({
        s3: s3,
        bucket: 'an516658-bucket',
        metadata: function (req, file, cb) {
            console.log(file);
            cb(null, { fieldName: file.originalname });
        },
        key: function (req, file, cb) {
            cb(null, file.originalname)
        }
    })
});

successResponse = (response, statusCode, message, data) => {
    response.status(statusCode || 200).json({
    code: statusCode || 200,
    message: message || "success",
    data: data || {},
  });
 };

module.exports = successResponse;

app.post('/storedata', function(request, response){
    console.log(request.body);      
    response.send(successResponse(request));
});

app.post('/appenddata', function(request, response){
    console.log(request.body);      
    response.send(successResponse(request));
});

app.post('/', function(request, response) {
    response.send('Hello world')
})

// app.post('/storedata', upload.single('photos'), function (req, res, next) {
//     res.send({
//         data: req.files, 
//         msg: 'Successfully uploaded' + req.files + 'files!'
//     })
// }); 

app.listen(3000, function() {console.log('express is up')});