document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const fileInput = document.getElementById('image-upload');
    const fileName = document.getElementById('file-name');
    const uploadButton = document.getElementById('upload-button');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('upload-progress');
    const progressText = document.getElementById('progress-text');
    const processingContainer = document.getElementById('processing-container');
    const resultModal = document.getElementById('result-modal');
    const resultImage = document.getElementById('result-image');
    const downloadLink = document.getElementById('download-link');
    const closeModalButton = document.getElementById('close-modal');
    const modalBackground = document.querySelector('.modal-background');
    const modalClose = document.querySelector('.modal-close');

    // Update file name display when a file is selected
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
            uploadButton.disabled = false;
        } else {
            fileName.textContent = 'No file selected';
            uploadButton.disabled = true;
        }
    });

    // Handle file upload
    uploadButton.addEventListener('click', async () => {
        if (!fileInput.files[0]) return;

        // Show progress bar
        progressContainer.style.display = 'block';
        progressBar.value = 0;
        progressText.textContent = '0%';

        // Create FormData
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);

        try {
            // Use XMLHttpRequest for progress tracking
            const xhr = new XMLHttpRequest();

            // Track upload progress
            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percentComplete = Math.round((event.loaded / event.total) * 100);
                    progressBar.value = percentComplete;
                    progressText.textContent = `${percentComplete}%`;

                    // When upload is complete, hide the progress container and show the processing container after a small delay
                    if (percentComplete === 100) {
                        // Add a small delay to ensure the progress bar is fully visible at 100% before showing the loader
                        setTimeout(() => {
                            progressContainer.style.display = 'none';
                            processingContainer.style.display = 'block';
                        }, 500); // 500ms delay
                    }
                }
            });

            // Handle response
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    // Create object URL from the response
                    const blob = new Blob([xhr.response], { type: 'image/png' });
                    const imageUrl = URL.createObjectURL(blob);

                    // Set image source and download link
                    resultImage.src = imageUrl;
                    downloadLink.href = imageUrl;

                    // Show the modal
                    resultModal.classList.add('is-active');
                } else {
                    alert('Error processing image. Please try again.');
                }

                // Reset progress and processing
                progressContainer.style.display = 'none';
                processingContainer.style.display = 'none';
            });

            // Handle errors
            xhr.addEventListener('error', () => {
                alert('Upload failed. Please try again.');
                progressContainer.style.display = 'none';
                processingContainer.style.display = 'none';
            });

            // Configure request
            xhr.open('POST', '/remove-background');
            xhr.responseType = 'arraybuffer';

            // Send the request
            xhr.send(formData);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
            progressContainer.style.display = 'none';
            processingContainer.style.display = 'none';
        }
    });

    // Close modal functions
    const closeModal = () => {
        resultModal.classList.remove('is-active');
        // Free memory
        URL.revokeObjectURL(resultImage.src);
        resultImage.src = '';
        downloadLink.href = '';
    };

    closeModalButton.addEventListener('click', closeModal);
    modalBackground.addEventListener('click', closeModal);
    modalClose.addEventListener('click', closeModal);

    // Close modal with escape key
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && resultModal.classList.contains('is-active')) {
            closeModal();
        }
    });
});
