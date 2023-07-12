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
    });
}
