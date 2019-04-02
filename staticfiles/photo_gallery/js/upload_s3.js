/*
     Function to carry out the actual POST request to S3 using the signed request from the Python app.
   */
function uploadFile(file, presigned_url) {
    const xhr = new XMLHttpRequest();
    const postData = new FormData();
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
    xhr.open('PUT', presigned_url, true);
    xhr.setRequestHeader('Content-type', file.type);
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
                uploadFile(file, response.presigned_url);
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
    if (files) {
        let parent = $('#files-list-container > ul');
        for (let i = 0; i < files.length; i++) {
            parent.append(
                "<li>" +
                files[i].name +
                "<button type=\"button\" class=\"btn btn-danger\ delete-item-button\">Delete</button>" +
                "</li>"
            );
            $(document).on('click', ".delete-item-button", function (event) {
                alert(event.target.id);
            });
        }
    }
}

function removeFromList(event) {
    // const files = Array.from(document.getElementById('file-input').files);
    // files.splice(i, 1);
    event.target.remove();
}
