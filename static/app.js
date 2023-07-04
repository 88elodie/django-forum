FilePond.registerPlugin(FilePondPluginImageValidateSize);
FilePond.registerPlugin(FilePondPluginFileValidateType);
FilePond.registerPlugin(FilePondPluginImagePreview);

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
        url: 'https://localhost:8000/fp',
        process: '/process/',
        patch: '/patch/',
        revert: '/revert/',
        fetch: '/fetch/?target=',
        load: '/load/'
    }
});

const inputElement = document.querySelector('input[type="file"]');
// Create a FilePond instance
const pond = FilePond.create(inputElement, {
    server: {
        url: '/fp/process/',
        process: {
          method: 'POST', // HTTP method for the file upload
          headers: {
            'X-CSRFToken': csrfToken,
          },
          withCredentials: true, // If your server requires credentials
        },
    },
    maxFiles: 3
});

