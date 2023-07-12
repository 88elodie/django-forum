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
const pond = FilePond.create(inputElement, {
    maxFiles: 3,
    maxFileSize: '2MB',
    acceptedFileTypes: ['image/*'],
    files:[{ source: '?id='+imageUrls[0].fields.upload_id, options: { type: 'local' }}]
});
