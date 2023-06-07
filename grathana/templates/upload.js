import 'FileUploader' from 'h5-fileuploader';

var up = new FileUploader({
    fileElement: document.getElementById('myfile'),
    fieldName: 'file'
    ,auto: false
    ,multiple: true
    ,accept: 'image/jpg, image/jpeg, image/png, application/pdf'
    ,fileSizeLimit: 1024 * 1024 * 500  // 5Mb
});

// upload server
up.configs.server = '/api/upload';

/**
 * other post params
 */
up.configs.postParams = {
    token: 'xxx',
    otherinfo: 'xxx'
};

/**
 * headers info
 */
up.configs.headers = {
    'csrf': 'xxx'
};

/**
 * called on a file added to queue
 */
up.fileQueuedHandler = function(file) {
     console.log('one file queued: ', file);
}

/**
 * called on all selected files queued
 */
up.filesQueuedCompleteHandler = function(obj) {
     // 非自动上传模式下，可以在这里调用上传方法手动上传
     console.log('all files queued: ', obj);
     
     // up.startUpload();
}

/**
 * upload progress
 */
up.uploadProgressHandler = function(file, percent) {
     console.log(percent);
}

/**
 * called on a file upload success
 */
up.uploadSuccessHandler = function(file, serverData) {
     console.log(serverData);
}

/**
 * called on all files upload success or fail
 */
up.uploadCompleteHandler = function() {
     console.log('upload complete');
}