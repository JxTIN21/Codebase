import { useState, useCallback } from 'react';
import { searchCodebase } from '../services/api';

export const useCodebaseSearch = (codebaseId) => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const search = useCallback(async (query) => {
    if (!query.trim() || !codebaseId) return;

    setLoading(true);
    setError(null);

    try {
      const searchResults = await searchCodebase(codebaseId, query.trim());
      setResults({
        query: query.trim(),
        ...searchResults,
      });
      return searchResults;
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [codebaseId]);

  const reset = useCallback(() => {
    setResults(null);
    setError(null);
  }, []);

  return {
    search,
    reset,
    loading,
    results,
    error,
  };
};