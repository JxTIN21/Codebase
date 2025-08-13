import React, { useState } from "react";
import CodebaseUpload from './components/CodebaseUpload';
import SearchInterface from './components/SearchInterface';
import ResultsDisplay from './components/ResultsDisplay';
import { Search, Code, Database } from 'lucide-react';

function App() {
  const [currentView, setCurrentView] = useState('upload');
  const [codebaseId, setCodebaseId] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  
  const handleUploadComplete = (id) => {
    setCodebaseId(id);
    setCurrentView('search');
  };

  const handleSearchResults = (results) => {
    setSearchResults(results);
    setCurrentView('results');
  };

  const handleNewSearch = () => {
    setSearchResults(null);
    setCurrentView('search');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bh-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Code className="h-8 w-8 text-primary-500" />
              <h1 className="text-2xl font-bold text-gray-900">
                Codebase Search & Explainer
              </h1>
            </div>
            <nav className="flex space-x-4">
              <button
                onClick={() => setCurrentView("upload")}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === "upload"
                    ? "bg-primary-100 text-primary-700"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                <Database className="h-4 w-4" />
                <span>Upload</span>
              </button>
              <button
                onClick={() => setCurrentView("search")}
                disabled={!codebaseId}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === "search"
                    ? "bg-primary-100 text-primary-700"
                    : !codebaseId
                    ? "text-gray-300 cursor-not-allowed"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                <Search className="h-4 w-4" />
                <span>Search</span>
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === "upload" && (
          <CodebaseUpload onUploadComplete={handleUploadComplete} />
        )}

        {currentView === "search" && codebaseId && (
          <SearchInterface
            codebaseId={codebaseId}
            onSearchResults={handleSearchResults}
          />
        )}

        {currentView === "results" && searchResults && (
          <ResultsDisplay
            results={searchResults}
            onNewSearch={handleNewSearch}
          />
        )}
      </main>
    </div>
  );
}

export default App;