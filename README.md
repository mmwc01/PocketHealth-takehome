# pocket-health-takehome
RUNNING BACKEND:
1. In the backend folder, run Flask Backend: python app.py (runs on http://localhost:5000)
    -http://localhost:5000/  `GET /` is a health check
    
    -`POST /save_file?tag={tag}`: Uploads a DICOM file and extracts the specified DICOM tag. The response includes the extracted attribute value and the processed PNG image generated from the DICOM data.

        Request Parameters:

        tag (required): The DICOM tag for extracting the attribute value.
        Request Body:

        file (required): The DICOM file to upload.
        Response:

        attribute_value: The extracted attribute value based on the provided DICOM tag.
        dicom_image: Base64-encoded PNG image generated from the DICOM data.

RUNNING FRONTEND: 
2. In the frontend folder, run npm install, then npm start (runs on http://localhost:3000)