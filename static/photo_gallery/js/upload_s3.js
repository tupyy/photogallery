/*
     Function to carry out the actual POST request to S3 using the signed request from the Python app.
   */
function uploadFile(file, s3Data, url) {
    const xhr = new XMLHttpRequest();
    const postData = new FormData();
    for (key in s3Data.fields) {
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 204) {
                alert('upload ok');
            } else {
                alert('Could not upload file.');
            }
        }
    };
    xhr.open('PUT', url, true);
    xhr.setRequestHeader('x-amz-acl', 'public-read');
    // xhr.setRequestHeader('Access-Control-Allow-Origin','*');
    xhr.send(postData);
}

/*
  Function to get the temporary signed request from the Python app.
  If request successful, continue to upload the file using this signed
  request.
*/
function getSignedRequest(file) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/sign-s3?file-name=${file.name}&file-type=${file.type}`);
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                uploadFile(file, response.data, response.url);
            } else {
                alert('Could not get signed URL.');
            }
        }
    };
    xhr.send();
}

/*
   Function called when file input updated. If there is a file selected, then
   start upload procedure by asking for a signed request from the app.
*/
function initUpload() {
    const files = document.getElementById('file-input').files;
    const file = files[0];
    if (!file) {
        return alert('No file selected.');
    }
    getSignedRequest(file);
}
