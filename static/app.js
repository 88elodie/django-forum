FilePond.registerPlugin(FilePondPluginFileValidateSize);
FilePond.registerPlugin(FilePondPluginFileValidateType);
FilePond.registerPlugin(FilePondPluginImagePreview);

imageUrls.map(url => (console.log(url.fields)))

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
        process: {
            url: '/process/',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          },
        patch: {
            url: '/patch/',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          },
        revert: {
            url: '/revert/',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          },
        fetch: {
            url: '/fetch/?target=',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          },
        load: {
            url: '/load/',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          },
    }
});

const inputElement = document.querySelector('input[type="file"]');
// Create a FilePond instance
const pond = FilePond.create(inputElement, {
    maxFiles: 3,
    maxFileSize: '2MB',
    acceptedFileTypes: ['image/*'],
    files: imageUrls.length > 0 ? imageUrls.map(url => ({ source: '?id='+url.fields.upload_id, options: { type: 'local' } })) : []
});
