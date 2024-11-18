document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const fileError = document.getElementById('file-error');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-container');
    const imagePreview = document.getElementById('imagePreview');
    const btnUpload = document.getElementById('btn-upload');
    const btnPredict = document.getElementById('btn-predict');
    const loader = document.querySelector('.loader');
    const result = document.getElementById('result');

    let fileUploaded = false;

    fileInput.addEventListener('change', () => {
        const files = fileInput.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            fileError.style.display = 'block';
            progressContainer.style.display = 'none';
            imagePreview.style.display = 'none';
            btnPredict.disabled = true;
            return;
        }

        fileError.style.display = 'none';
        progressContainer.style.display = 'block';
        imagePreview.style.display = 'block';
        fileUploaded = true;

        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.style.backgroundImage = 'url(' + e.target.result + ')';
        };
        reader.readAsDataURL(file);

        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = progress + '%';
            if (progress >= 100) {
                clearInterval(interval);
                btnUpload.style.backgroundColor = 'gray';
                btnUpload.disabled = true;
                btnPredict.disabled = false;
            }
        }, 300);
    }

    btnUpload.addEventListener('click', (event) => {
        if (!fileUploaded) {
            fileError.textContent = 'No file chosen';
            fileError.style.display = 'block';
            event.preventDefault();
        }
    });

    btnPredict.addEventListener('click', () => {
        if (!fileUploaded) {
            fileError.textContent = 'You need to upload a file first';
            fileError.style.display = 'block';
        }
    });
});