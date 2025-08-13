import React, { useState } from 'react';
import { Search, MessageSquare, Zap } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import { searchCodebase } from '../services/api';

const SearchInterface = ({ codebaseId, onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [searching, setSearching] = useState(false);

  const sampleQueries = [
    'Where is user authentication implemented?',
    'How does the payment system work?',
    'Show me the database connection logic',
    'Where are the API routes defined?',
    'How is error handling implemented?',
    'Find the configuration files',
  ];

  const handleSearch = async (searchQuery = query) => {
    if (!searchQuery.trim()) return;
    
    setSearching(true);
    try {
      const results = await searchCodebase(codebaseId, searchQuery.trim());
      onSearchResults({
        query: searchQuery.trim(),
        ...results,
      });
    } catch (error) {
      console.error('Search failed:', error);
      // Handle error appropriately
    } finally {
      setSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Ask Questions About Your Code
        </h2>
        <p className="text-lg text-gray-600">
          Use natural language to search and understand your codebase
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        <div className="relative">
          <div className="flex">
            <div className="relative flex-1">
              <MessageSquare className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask anything about your codebase... e.g., 'Where is user authentication implemented?'"
                className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none text-lg"
                rows={3}
                disabled={searching}
              />
            </div>
            <button
              onClick={() => handleSearch()}
              disabled={!query.trim() || searching}
              className="ml-4 btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 px-6"
            >
              {searching ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span>Searching...</span>
                </>
              ) : (
                <>
                  <Search className="h-5 w-5" />
                  <span>Search</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Zap className="h-5 w-5 mr-2 text-primary-500" />
            Quick Questions
          </h3>
          <div className="space-y-2">
            {sampleQueries.map((sampleQuery, index) => (
              <button
                key={index}
                onClick={() => handleSearch(sampleQuery)}
                disabled={searching}
                className="w-full text-left p-3 bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-all text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {sampleQuery}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Search Tips
          </h3>
          <ul className="space-y-3 text-sm text-gray-600">
            <li className="flex items-start">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0" />
              <span>Ask specific questions about functionality, architecture, or implementation patterns</span>
            </li>
            <li className="flex items-start">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0" />
              <span>Use technical terms like "authentication", "database", "API", "configuration"</span>
            </li>
            <li className="flex items-start">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0" />
              <span>Ask about relationships between different parts of your code</span>
            </li>
            <li className="flex items-start">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0" />
              <span>Request explanations of complex logic or design patterns</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SearchInterface;