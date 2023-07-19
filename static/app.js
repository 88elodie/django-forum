FilePond.registerPlugin(FilePondPluginFileValidateSize);
FilePond.registerPlugin(FilePondPluginFileValidateType);
FilePond.registerPlugin(FilePondPluginImagePreview);
FilePond.registerPlugin(FilePondPluginImageTransform);
FilePond.registerPlugin(FilePondPluginImageCrop);
FilePond.registerPlugin(FilePondPluginImageResize);
FilePond.registerPlugin(FilePondPluginImageEdit);

// imageUrls.map(url => (console.log(url.fields)))

const getCookie = (name) => {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) {
      return parts.pop().split(";").shift();
    }
};
const csrfToken = getCookie('csrftoken');

FilePond.setOptions({
    server: {
        url: 'http://localhost:8000/fp',
        headers: {
            'X-CSRFToken': csrfToken,
          },
        process: {
            url: '/process/',
            withCredentials: true,
          },
        patch: {
            url: '/patch/',
            withCredentials: true,
          },
        revert: {
            url: '/revert/',
            withCredentials: true,
          },
        fetch: {
            url: '/fetch/?target=',
            withCredentials: true,
          },
        load: {
            url: '/load/',
            withCredentials: true,
          },
    }
});

const inputElement = document.querySelector('input[type="file"]');
// Create a FilePond instance
if(location.pathname.includes("/posts/")){
    const pond = FilePond.create(inputElement, {
        maxFiles: 3,
        maxFileSize: '2MB',
        acceptedFileTypes: ['image/*'],
        // files:[{ source: '?id='+imageUrls[0].fields.upload_id, options: { type: 'local' }}]
        //keep gif format
        //source : https://stackoverflow.com/questions/58874156/make-filepond-image-transform-plugin-ignore-animated-gifs
        imageTransformImageFilter: (file) => new Promise(resolve => {

            // no gif mimetype, do transform
            if (!/image\/gif/.test(file.type)) return resolve(true);
    
            const reader = new FileReader();
            reader.onload = () => {
    
                var arr = new Uint8Array(reader.result),
                i, len, length = arr.length, frames = 0;
    
                // make sure it's a gif (GIF8)
                if (arr[0] !== 0x47 || arr[1] !== 0x49 || 
                    arr[2] !== 0x46 || arr[3] !== 0x38) {
                    // it's not a gif, we can safely transform it
                    resolve(true);
                    return;
                }
    
                for (i=0, len = length - 9; i < len, frames < 2; ++i) {
                    if (arr[i] === 0x00 && arr[i+1] === 0x21 &&
                        arr[i+2] === 0xF9 && arr[i+3] === 0x04 &&
                        arr[i+8] === 0x00 && 
                        (arr[i+9] === 0x2C || arr[i+9] === 0x21)) {
                        frames++;
                    }
                }
    
                // if frame count > 1, it's animated, don't transform
                if (frames > 1) {
                    return resolve(false);
                }
    
                // do transform
                resolve(true);
            }
            reader.readAsArrayBuffer(file);
    
        })
    });
}else if(location.pathname.includes("/accounts/profile/")) {
    const pond = FilePond.create(inputElement, {
        maxFiles: 1,
        maxFileSize: '2MB',
        acceptedFileTypes: ['image/*'],
        imageResizeUpscale: false,
        imagePreviewHeight: 170,
        imageCropAspectRatio: '1:1',
        imageResizeTargetWidth: 200,
        imageResizeTargetHeight: 200,
        stylePanelLayout: 'compact circle',
        styleLoadIndicatorPosition: 'center bottom',
        styleProgressIndicatorPosition: 'right bottom',
        styleButtonRemoveItemPosition: 'left bottom',
        styleButtonProcessItemPosition: 'right bottom',
        imageTransformImageFilter: (file) => new Promise(resolve => {

            // no gif mimetype, do transform
            if (!/image\/gif/.test(file.type)) return resolve(true);
    
            const reader = new FileReader();
            reader.onload = () => {
    
                var arr = new Uint8Array(reader.result),
                i, len, length = arr.length, frames = 0;
    
                // make sure it's a gif (GIF8)
                if (arr[0] !== 0x47 || arr[1] !== 0x49 || 
                    arr[2] !== 0x46 || arr[3] !== 0x38) {
                    // it's not a gif, we can safely transform it
                    resolve(true);
                    return;
                }
    
                for (i=0, len = length - 9; i < len, frames < 2; ++i) {
                    if (arr[i] === 0x00 && arr[i+1] === 0x21 &&
                        arr[i+2] === 0xF9 && arr[i+3] === 0x04 &&
                        arr[i+8] === 0x00 && 
                        (arr[i+9] === 0x2C || arr[i+9] === 0x21)) {
                        frames++;
                    }
                }
    
                // if frame count > 1, it's animated, don't transform
                if (frames > 1) {
                    return resolve(false);
                }
    
                // do transform
                resolve(true);
            }
            reader.readAsArrayBuffer(file);
    
        })
    });
}
