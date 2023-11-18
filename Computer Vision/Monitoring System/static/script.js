// Inside script.js

// Function to load the uploaded video for preview
function loadVideoPreview() {
  const videoInput = document.getElementById("video-upload");
  if (videoInput.files && videoInput.files[0]) {
    const uploadedVideo = document.getElementById("uploaded-video");
    uploadedVideo.src = URL.createObjectURL(videoInput.files[0]);
    uploadedVideo.onload = function () {
      URL.revokeObjectURL(uploadedVideo.src);
    };
  }
}

// Attach the loadVideoPreview function to the video input
document
  .getElementById("video-upload")
  .addEventListener("change", loadVideoPreview);

// Add the processVideo function
function processVideo(filename) {
  fetch(`/process-video/${filename}`)
    .then((response) => response.text())
    .then((data) => {
      console.log(data);
      // Handle the response, display results, etc.
    });
}
