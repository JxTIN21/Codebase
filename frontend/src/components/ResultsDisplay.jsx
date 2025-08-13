import React, { useState } from 'react';
import { ArrowLeft, FileText, MessageSquare, Copy, ExternalLink, CheckCircle, Sparkles } from 'lucide-react';
import CodeViewer from './CodeViewer';

const ResultsDisplay = ({ results, onNewSearch }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleCopyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header with New Search Button */}
      <div className="mb-8">
        <button
          onClick={onNewSearch}
          className="group flex items-center space-x-2 text-indigo-600 hover:text-indigo-700 font-medium transition-colors"
        >
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" />
          <span>New Search</span>
        </button>
      </div>

      {/* Enhanced Explanation Section */}
      <div className="bg-gradient-to-br from-white via-indigo-50/30 to-purple-50/20 rounded-2xl shadow-xl border border-indigo-100/50 mb-8 overflow-hidden">
        {/* Header with Query */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 rounded-lg p-2">
              <MessageSquare className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">
                Search Query
              </h3>
              <p className="text-indigo-100 text-sm">
                "{results.query}"
              </p>
            </div>
          </div>
        </div>

        {/* AI Explanation Content */}
        <div className="p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Sparkles className="h-5 w-5 text-indigo-600" />
            <h4 className="text-lg font-semibold text-gray-900">AI Explanation</h4>
          </div>
          
          {/* Formatted Explanation */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
            <div className="p-6">
              <div className="prose prose-gray prose-indigo max-w-none">
                <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                  {results.explanation || results.answer}
                </div>
              </div>
            </div>
            
            {/* Copy Button */}
            <div className="border-t border-gray-100 px-6 py-3 bg-gray-50/50">
              <button
                onClick={() => handleCopyToClipboard(results.explanation || results.answer)}
                className={`flex items-center space-x-2 text-sm font-medium transition-colors ${
                  copied 
                    ? 'text-green-600' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                {copied ? (
                  <>
                    <CheckCircle className="h-4 w-4" />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4" />
                    <span>Copy explanation</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Relevant Files and Code Preview */}
      {results.relevant_files && results.relevant_files.length > 0 && (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-8">
          {/* Files List */}
          <div className="xl:col-span-1">
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <FileText className="h-5 w-5 mr-2 text-gray-600" />
                  Relevant Files
                  <span className="ml-2 bg-indigo-100 text-indigo-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    {results.relevant_files.length}
                  </span>
                </h3>
              </div>
              
              <div className="p-4 space-y-3 max-h-96 overflow-y-auto">
                {results.relevant_files.map((file, index) => (
                  <div
                    key={index}
                    className={`rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                      selectedFile === file
                        ? 'bg-indigo-50 border-2 border-indigo-200 shadow-md'
                        : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100 hover:border-gray-200'
                    }`}
                    onClick={() => setSelectedFile(file)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-900 mb-2 truncate" title={file.file_path}>
                          {file.file_path.split('/').pop()}
                        </h4>
                        <p className="text-xs text-gray-500 mb-2 truncate">
                          {file.file_path}
                        </p>
                        
                        {/* Relevance Score */}
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="flex-1 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${file.relevance_score * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-xs font-medium text-gray-600">
                            {(file.relevance_score * 100).toFixed(0)}%
                          </span>
                        </div>
                        
                        {/* Code Snippet Preview */}
                        {file.snippet && (
                          <div className="bg-gray-900 rounded-md p-2 text-xs font-mono overflow-hidden">
                            <div className="text-green-400 line-clamp-2">
                              {file.snippet}
                            </div>
                          </div>
                        )}
                      </div>
                      <ExternalLink className="h-4 w-4 text-gray-400 ml-2 flex-shrink-0" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Code Preview */}
          <div className="xl:col-span-2">
            {selectedFile ? (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Code Preview
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {selectedFile.file_path}
                  </p>
                </div>
                <div className="p-0">
                  <CodeViewer file={selectedFile} />
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border-2 border-dashed border-gray-300 p-12 text-center">
                <div className="bg-white rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4 shadow-sm">
                  <FileText className="h-10 w-10 text-gray-400" />
                </div>
                <h4 className="text-lg font-medium text-gray-900 mb-2">
                  Select a file to preview
                </h4>
                <p className="text-gray-600">
                  Click on any file from the list to view its contents here
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Code Examples */}
      {results.code_examples && results.code_examples.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
            <h3 className="text-xl font-semibold text-gray-900 flex items-center">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg p-2 mr-3">
                <FileText className="h-5 w-5 text-white" />
              </div>
              Code Examples
              <span className="ml-3 bg-indigo-100 text-indigo-800 text-sm font-medium px-3 py-1 rounded-full">
                {results.code_examples.length}
              </span>
            </h3>
          </div>
          
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {results.code_examples.map((example, index) => (
                <div key={index} className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200 overflow-hidden">
                  <div className="bg-white px-4 py-3 border-b border-gray-200">
                    <h4 className="font-semibold text-gray-900">
                      {example.title || `Example ${index + 1}`}
                    </h4>
                  </div>
                  
                  <div className="bg-gray-900 relative">
                    <div className="absolute top-3 right-3">
                      <button
                        onClick={() => handleCopyToClipboard(example.code)}
                        className="bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white p-1.5 rounded-md transition-colors"
                      >
                        <Copy className="h-3 w-3" />
                      </button>
                    </div>
                    <pre className="p-4 overflow-x-auto text-sm">
                      <code className="text-green-400">{example.code}</code>
                    </pre>
                  </div>
                  
                  {example.explanation && (
                    <div className="p-4 bg-white">
                      <p className="text-sm text-gray-600 leading-relaxed">
                        {example.explanation}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;