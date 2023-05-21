let dropzone = document.getElementById('dropzone')
let uploadBtn = document.getElementById('upload-btn')
let uploadForm = document.getElementById('upload-form')
let uploadSubmit = document.getElementById('upload-submit')
let progressBar = document.getElementById('progress-bar')
let uploadedImage = document.getElementById('uploaded-image')
function handleDragOver(e) {
  e.preventDefault()
  e.stopPropagation()
  dropzone.classList.add('border-primary')
}

function handleDragLeave(e) {
  e.preventDefault()
  e.stopPropagation()
  dropzone.classList.remove('border-primary')
}

function handleDrop(e) {
  e.preventDefault()
  e.stopPropagation()
  dropzone.classList.remove('border-primary')

  let files = e.dataTransfer.files

  // Check if the file is an image
  var isImage = /^image\//.test(files[0].type)

  if (!isImage) {
    alert('Please upload only image files.')
    return
  }

  // Get form data
  let formData = new FormData()
  formData.append('file', files[0])

  // Send form data via AJAX
  let xhr = new XMLHttpRequest()
  xhr.upload.addEventListener('progress', function (e) {
    if (e.lengthComputable) {
      let percentComplete = (e.loaded / e.total) * 100

      progressBar.style.width = percentComplete.toFixed(0) + '%'
      progressBar.innerHTML = percentComplete.toFixed(0) + '%'
    }
  })

  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        progressBar.style.width = '100%'
        uploadSubmit.disabled = true
      } else {
        alert('Upload failed.')
      }
    }
  }

  xhr.open('POST', uploadForm.action, true)
  xhr.send(formData)

  // Update file input and submixt button
  updateInput(files)
}

function handleInputChange() {
  let files = uploadBtn.files
  updateInput(files)
}

function handleFormSubmit(e) {
  e.preventDefault()

  // Reset progress bar
  progressBar.style.width = '0%'

  // Get form data
  let formData = new FormData()
  formData.append('file', uploadBtn.files[0])

  // Send form data via AJAX
  let xhr = new XMLHttpRequest()

  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        progressBar.style.width = '100%'
        uploadSubmit.disabled = true
      } else {
        alert('Upload failed.')
      }
    }
  }

  xhr.upload.addEventListener('progress', function (e) {
    if (e.lengthComputable) {
      let percentComplete = (e.loaded / e.total) * 100
      progressBar.style.width = percentComplete.toFixed(0) + '%'
      progressBar.innerHTML = percentComplete.toFixed(0) + '%'
    }
  })

  xhr.open('POST', uploadForm.action, true)
  xhr.send(formData)
}

function updateInput(files) {
  if (files.length > 0) {
    let fileNames = []
    for (let i = 0; i < files.length; i++) {
      fileNames.push(files[i].name)
    }
    let url = URL.createObjectURL(files[0])
    uploadedImage.src = url
    // uploadedImage.style.display = 'block'
    dropzone.style.display = 'none'
    uploadedImage.style.cssText =
      'display:block; max-width: 100%; max-height: 100%; width: auto; height: auto; margin: auto; border: 2px dashed #ccc;'

    // dropzone.style.color = 'red'
    // dropzone.style.fontWeight = 'bold'
    // dropzone.innerHTML = fileNames.join(', ')
    uploadSubmit.disabled = false
  } else {
    dropzone.innerHTML =
      '<i class="fas fa-cloud-upload-alt"></i><div class="text-muted">Drag and drop files here or click to select files</div>'
    uploadSubmit.disabled = true
  }
}

// Add event listeners
dropzone.addEventListener('dragover', handleDragOver)
dropzone.addEventListener('dragleave', handleDragLeave)
dropzone.addEventListener('drop', handleDrop)

uploadBtn.addEventListener('change', handleInputChange)

uploadForm.addEventListener('submit', handleFormSubmit)
