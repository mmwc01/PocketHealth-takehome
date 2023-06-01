import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [tagName, setTagName] = useState('');
  const [attributeValue, setAttributeValue] = useState('');
  const [dicomImage, setDicomImage] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleTagChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTagName(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedFile) {
      console.log('No file selected');
      return;
    }

    const data = new FormData();
    data.append('file', selectedFile);
    const response = await axios.post('http://127.0.0.1:5000/save_file?tag=' + tagName, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    setAttributeValue(response.data.attribute_value);
    setDicomImage(response.data.dicom_image);
  };

  return (
    <div>
      <h1>DICOM file processor</h1>
      <form onSubmit={handleSubmit}>
        <div>
          DICOM File:
          <input type="file" accept=".dcm" onChange={handleFileChange} />
        </div>
        <div>
          Tag Name:
          <input type="text" value={tagName} onChange={handleTagChange} />
        </div>
        <button type="submit">Upload</button>
      </form>
      <div>
        <h2>Response:</h2>
        {attributeValue && <p>Attribute Value: {attributeValue}</p>}
        {dicomImage && (
          <div>
            <p>DICOM Image:</p>
            <img src={`data:image/png;base64,${dicomImage}`} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;