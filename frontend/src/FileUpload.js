import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import LoadingSpinner from './components/LoadingSpinner'; // Import the loading spinner
import './App.css'; // Importing CSS styles

const FileUpload = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [programDescription, setProgramDescription] = useState('');
  const [outputFiles, setOutputFiles] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isProcessed, setIsProcessed] = useState(false);

  const onDrop = (acceptedFiles) => {
    setSelectedFiles([...selectedFiles, ...acceptedFiles]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: true,
  });

  const handleProgramDescriptionChange = (event) => {
    setProgramDescription(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (selectedFiles.length === 0 || !programDescription) {
      alert("Please upload files and provide a description of the program.");
      return;
    }

    setIsSubmitting(true); // Start loading state

    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append('files', file); // Appending files
    });
    formData.append('instruction', programDescription); // Appending description

    try {
      const response = await axios.post('http://localhost:8000/api/run-program/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob', // Important: expect a blob response
      });

      console.log(response.headers);

      // Extract the filename from the content-disposition header
      const filename = response.headers['content-disposition']
        .split('filename=')[1]
        .replace(/"/g, '');

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename); // Use the extracted filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setIsProcessed(true);
    } catch (error) {
      console.error('Error processing files:', error);
      alert("Failed to process the files. Please try again.");
    } finally {
      setIsSubmitting(false); // End loading state
    }
  };

  const handleDownload = (url) => {
    window.open(url, '_blank'); // Adjust this if needed
  };

  const handleRemoveFile = (fileToRemove) => {
    setSelectedFiles(selectedFiles.filter(file => file !== fileToRemove));
  };

  const handleRemoveAllFiles = () => {
    setSelectedFiles([]);
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    switch (extension) {
      case 'pdf':
        return 'fas fa-file-pdf'; // PDF icon
      case 'doc':
      case 'docx':
        return 'fas fa-file-word'; // Word icon
      case 'xls':
      case 'xlsx':
        return 'fas fa-file-excel'; // Excel icon
      case 'ppt':
      case 'pptx':
        return 'fas fa-file-powerpoint'; // PowerPoint icon
      case 'jpg':
      case 'jpeg':
      case 'png':
        return 'fas fa-file-image'; // Image icon
      case 'txt':
        return 'fas fa-file-alt'; // Text file icon
      default:
        return 'fas fa-file'; // Default file icon for other types
    }
  };

  return (
    <div className="file-upload-container">
      <h1>Process your files</h1>

      {/* File Upload Section */}
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        <p>Drag and drop files here, or click to select files</p>
      </div>

      <div className="file-list">
  <div className="file-list-header">
    <h3>Selected Files</h3>
    {selectedFiles.length > 0 && (
      <button onClick={handleRemoveAllFiles} className="remove-all-button">Remove All</button>
    )}
  </div>
  {selectedFiles.length > 0 && (
    <ul>
      {selectedFiles.map((file, index) => (
        <li key={index}>
          <i className={getFileIcon(file.name)} aria-hidden="true"></i> {/* File icon */}
          {file.name}
          <button onClick={() => handleRemoveFile(file)} className="remove-file-button">x</button>
        </li>
      ))}
    </ul>
  )}
</div>


      {/* Program Description Section */}
      <textarea
        value={programDescription}
        onChange={handleProgramDescriptionChange}
        placeholder="What do you want to do with the files?"
        rows="4"
        className="description-textarea"
      />

      {/* Submit Button */}
      <button onClick={handleSubmit} disabled={isSubmitting} className="submit-button">
        {isSubmitting ? <LoadingSpinner /> : 'Process Files'}
      </button>

      {/* Download Section
      {isProcessed && (
        <div className="output-section">
          <h2>Processed Files</h2>
          {Array.isArray(outputFiles) && outputFiles.length > 0 ? (
            outputFiles.map((fileUrl, index) => (
              <div key={index}>
                <button onClick={() => handleDownload(fileUrl)} className="download-button">Download File {index + 1}</button>
              </div>
            ))
          ) : (
            <p>No output files available for download.</p>
          )}
        </div>
      )} */}
    </div>
  );
};

export default FileUpload;
