import React, { useState, useRef } from 'react';
import { Upload, FolderOpen, AlertCircle, CheckCircle, FileText, Code, Plus, X } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import { uploadCodebase } from '../services/api';

const CodebaseUpload = ({ onUploadComplete }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [activeTab, setActiveTab] = useState('files'); // 'files' or 'text'
  const [textInputs, setTextInputs] = useState([{ id: 1, filename: '', content: '', language: 'javascript' }]);
  const fileInputRef = useRef(null);

  const supportedLanguages = [
    { value: 'javascript', label: 'JavaScript' },
    { value: 'typescript', label: 'TypeScript' },
    { value: 'python', label: 'Python' },
    { value: 'java', label: 'Java' },
    { value: 'cpp', label: 'C++' },
    { value: 'c', label: 'C' },
    { value: 'csharp', label: 'C#' },
    { value: 'php', label: 'PHP' },
    { value: 'ruby', label: 'Ruby' },
    { value: 'go', label: 'Go' },
    { value: 'rust', label: 'Rust' },
    { value: 'swift', label: 'Swift' },
    { value: 'kotlin', label: 'Kotlin' },
    { value: 'jsx', label: 'JSX' },
  ];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = Array.from(e.dataTransfer.files);
    setSelectedFiles(prev => [...prev, ...files]);
    setActiveTab('files');
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(prev => [...prev, ...files]);
  };

  const addTextInput = () => {
    const newId = Math.max(...textInputs.map(t => t.id)) + 1;
    setTextInputs(prev => [...prev, { id: newId, filename: '', content: '', language: 'javascript' }]);
  };

  const removeTextInput = (id) => {
    if (textInputs.length > 1) {
      setTextInputs(prev => prev.filter(input => input.id !== id));
    }
  };

  const updateTextInput = (id, field, value) => {
    setTextInputs(prev => prev.map(input => 
      input.id === id ? { ...input, [field]: value } : input
    ));
  };

  const createFileFromText = (textInput) => {
    const extension = getExtensionFromLanguage(textInput.language);
    const filename = textInput.filename || `code_snippet_${textInput.id}.${extension}`;
    const blob = new Blob([textInput.content], { type: 'text/plain' });
    const file = new File([blob], filename, { type: 'text/plain' });
    return file;
  };

  const getExtensionFromLanguage = (language) => {
    const extensions = {
      'javascript': 'js',
      'typescript': 'ts',
      'python': 'py',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'csharp': 'cs',
      'php': 'php',
      'ruby': 'rb',
      'go': 'go',
      'rust': 'rs',
      'swift': 'swift',
      'kotlin': 'kt'
    };
    return extensions[language] || 'txt';
  };

  const handleUpload = async () => {
    const filesToUpload = [...selectedFiles];
    
    // Add text inputs as files
    const validTextInputs = textInputs.filter(input => input.content.trim());
    validTextInputs.forEach(textInput => {
      const file = createFileFromText(textInput);
      filesToUpload.push(file);
    });

    if (filesToUpload.length === 0) {
      setUploadStatus({
        type: 'error',
        message: 'Please select files or add text content to upload.',
      });
      return;
    }

    setUploading(true);
    setUploadStatus(null);

    try {
      const formData = new FormData();
      filesToUpload.forEach((file) => {
        formData.append('files', file);
      });

      const result = await uploadCodebase(formData);
      
      setUploadStatus({
        type: 'success',
        message: `Successfully uploaded ${result.files_processed} files`,
      });
      
      setTimeout(() => {
        onUploadComplete(result.codebase_id);
      }, 1500);
      
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Upload failed. Please try again.',
      });
    } finally {
      setUploading(false);
    }
  };

  const totalItems = selectedFiles.length + textInputs.filter(input => input.content.trim()).length;

  return (
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Upload Your Codebase
        </h2>
        <p className="text-lg text-gray-600">
          Upload files or paste code directly to create a searchable knowledge base
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        {/* Tab Navigation */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('files')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'files'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <FolderOpen className="h-4 w-4" />
                <span>Upload Files</span>
                {selectedFiles.length > 0 && (
                  <span className="bg-indigo-100 text-indigo-800 text-xs font-medium px-2 py-0.5 rounded-full">
                    {selectedFiles.length}
                  </span>
                )}
              </div>
            </button>
            <button
              onClick={() => setActiveTab('text')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'text'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Code className="h-4 w-4" />
                <span>Paste Code</span>
                {textInputs.filter(input => input.content.trim()).length > 0 && (
                  <span className="bg-indigo-100 text-indigo-800 text-xs font-medium px-2 py-0.5 rounded-full">
                    {textInputs.filter(input => input.content.trim()).length}
                  </span>
                )}
              </div>
            </button>
          </nav>
        </div>

        <div className="p-8">
          {/* File Upload Tab */}
          {activeTab === 'files' && (
            <div className="space-y-6">
              <div
                className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-all ${
                  dragActive
                    ? 'border-indigo-400 bg-indigo-50'
                    : 'border-gray-300 hover:border-indigo-400'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  onChange={handleFileSelect}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  accept=".js,.jsx,.ts,.tsx,.py,.java,.cpp,.c,.h,.cs,.php,.rb,.go,.rs,.swift,.kt"
                />
                
                <div className="space-y-4">
                  <div className="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center">
                    <Upload className="h-8 w-8 text-indigo-500" />
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">
                      Drop your code files here
                    </h3>
                    <p className="text-gray-500 mt-2">
                      or click to browse your files
                    </p>
                  </div>
                  
                  <div className="text-sm text-gray-400">
                    Supports: JavaScript, TypeScript, Python, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin
                  </div>
                </div>
              </div>

              {selectedFiles.length > 0 && (
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-sm font-medium text-gray-900">
                      Selected Files ({selectedFiles.length})
                    </h4>
                    <button
                      onClick={() => setSelectedFiles([])}
                      className="text-sm text-red-600 hover:text-red-700"
                    >
                      Clear all
                    </button>
                  </div>
                  <div className="max-h-40 overflow-y-auto bg-gray-50 rounded-lg p-4 space-y-2">
                    {selectedFiles.map((file, index) => (
                      <div key={index} className="flex items-center justify-between bg-white rounded-md p-2">
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <FolderOpen className="h-4 w-4" />
                          <span>{file.name}</span>
                          <span className="text-gray-400">({(file.size / 1024).toFixed(1)} KB)</span>
                        </div>
                        <button
                          onClick={() => setSelectedFiles(prev => prev.filter((_, i) => i !== index))}
                          className="text-red-500 hover:text-red-700 p-1"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Text Input Tab */}
          {activeTab === 'text' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Paste Your Code</h3>
                <button
                  onClick={addTextInput}
                  className="flex items-center space-x-2 text-indigo-600 hover:text-indigo-700 text-sm font-medium"
                >
                  <Plus className="h-4 w-4" />
                  <span>Add Another File</span>
                </button>
              </div>

              {textInputs.map((textInput, index) => (
                <div key={textInput.id} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-sm font-medium text-gray-700">
                      Code Snippet {index + 1}
                    </h4>
                    {textInputs.length > 1 && (
                      <button
                        onClick={() => removeTextInput(textInput.id)}
                        className="text-red-500 hover:text-red-700 p-1"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Filename (optional)
                      </label>
                      <input
                        type="text"
                        value={textInput.filename}
                        onChange={(e) => updateTextInput(textInput.id, 'filename', e.target.value)}
                        placeholder="e.g., utils.js, main.py"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Language
                      </label>
                      <select
                        value={textInput.language}
                        onChange={(e) => updateTextInput(textInput.id, 'language', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        {supportedLanguages.map((lang) => (
                          <option key={lang.value} value={lang.value}>
                            {lang.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Code Content
                    </label>
                    <textarea
                      value={textInput.content}
                      onChange={(e) => updateTextInput(textInput.id, 'content', e.target.value)}
                      placeholder="Paste your code here..."
                      rows={12}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md font-mono text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Status and Upload Section */}
        <div className="border-t border-gray-200 bg-gray-50 px-8 py-6">
          {uploadStatus && (
            <div className={`mb-6 p-4 rounded-lg flex items-center space-x-3 ${
              uploadStatus.type === 'success' 
                ? 'bg-green-50 text-green-800 border border-green-200' 
                : 'bg-red-50 text-red-800 border border-red-200'
            }`}>
              {uploadStatus.type === 'success' ? (
                <CheckCircle className="h-5 w-5" />
              ) : (
                <AlertCircle className="h-5 w-5" />
              )}
              <span>{uploadStatus.message}</span>
            </div>
          )}

          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              {totalItems > 0 ? (
                <span>Ready to upload {totalItems} item{totalItems !== 1 ? 's' : ''}</span>
              ) : (
                <span>No files or code content selected</span>
              )}
            </div>

            <button
              onClick={handleUpload}
              disabled={totalItems === 0 || uploading}
              className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-6 rounded-lg transition-colors flex items-center space-x-2"
            >
              {uploading ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <Upload className="h-4 w-4" />
                  <span>Upload & Process Codebase</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodebaseUpload;