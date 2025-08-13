import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, FileText } from 'lucide-react';

const CodeViewer = ({ file }) => {
  const getLanguageFromExtension = (filename) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    const languageMap = {
      js: 'javascript',
      jsx: 'jsx',
      ts: 'typescript',
      tsx: 'tsx',
      py: 'python',
      java: 'java',
      cpp: 'cpp',
      c: 'c',
      h: 'c',
      cs: 'csharp',
      php: 'php',
      rb: 'ruby',
      go: 'go',
      rs: 'rust',
      swift: 'swift',
      kt: 'kotlin',
    };
    return languageMap[ext] || 'text';
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(file.content || file.snippet);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <FileText className="h-4 w-4 text-gray-500" />
          <span className="font-medium text-gray-900">{file.file_path}</span>
        </div>
        <button
          onClick={handleCopyCode}
          className="flex items-center space-x-1 text-sm text-gray-500 hover:text-gray-700"
        >
          <Copy className="h-4 w-4" />
          <span>Copy</span>
        </button>
      </div>
      <div className="max-h-96 overflow-auto">
        <SyntaxHighlighter
          language={getLanguageFromExtension(file.file_path)}
          style={oneDark}
          customStyle={{
            margin: 0,
            padding: '1rem',
            fontSize: '14px',
            lineHeight: '1.5',
          }}
        >
          {file.content || file.snippet || '// Content not available'}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default CodeViewer;