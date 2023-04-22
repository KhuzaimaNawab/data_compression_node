# Documentation for lzm compression API

# API link for compression

The API link for lzm compression is http://localhost:3000/compress.
# Description

This API is used for compressing text files using the lzm compression algorithm.
# Usage

To use this API, send a POST request to the API link with a single file attached in the request body. The file should be a text file, and it should be attached with the key name 'file'.

The API will read the contents of the file, compress it using the lzm algorithm, and return the compressed data in the response.
# Example

Here is an example of how to use the lzm compression API using curl:

curl -X POST -F "file=@/path/to/file.txt" http://localhost:3000/compress

# Response

The API will return a JSON response containing the compressed data.

If the compression is successful, the response will contain the compressed data as a string in the 'data' field.

If an error occurs during compression, the API will return an error message in the 'error' field of the response.