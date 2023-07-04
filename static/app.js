FilePond.registerPlugin(FilePondPluginImageValidateSize);
FilePond.registerPlugin(FilePondPluginFileValidateType);

let files = []
const inputElement = document.querySelector('input[type="file"]');
// Create a FilePond instance
const pond = FilePond.create(inputElement, {
    onaddfile: (err, fileItem) => {
        files.push(fileItem.file)
    },
    onremovefile: (err, fileItem) => {
        const index = files.indexOf(fileItem.file)
        if (index > -1) {
            files.splice(index, 1)
        }
    },
    maxFiles: 3
});

