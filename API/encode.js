function encodeBase64ImageFile (image) {
    return new Promise((resolve, reject) => {
      let reader = new FileReader()
      // convert the file to base64 text
      reader.readAsDataURL(image)
      // on reader load somthing...
      reader.onload = (event) => {
        resolve(event.target.result)
      }
      reader.onerror = (error) => {
        reject(error)
      }
    })
  }