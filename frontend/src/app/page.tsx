/**
 * Main Dashboard Page - demonstrates study guide principles:
 * 
 * 1. SSG for static shell, CSR for dynamic data
 * 2. Component-based architecture with Tailwind CSS
 * 3. Proper data fetching patterns
 */
'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import MetricCard from '@/components/MetricCard';
import InsightPanel from '@/components/InsightPanel';
import LoadingSpinner from '@/components/LoadingSpinner';
import { Button } from '@/components/ui/Button';

// Type definitions matching backend Pydantic models
interface Metric {
  id: number;
  name: string;
  value: number;
  category: string;
  description?: string;
  timestamp: string;
  created_at: string;
  updated_at?: string;
}

interface Insight {
  id: number;
  text: string;
  type: 'trend' | 'risk' | 'opportunity' | 'recommendation' | 'observation';
  confidence: number;
  created_at: string;
}

export default function Dashboard() {
  // State management for dynamic data
  // Demonstrates study guide principle: client-side state management
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [loading, setLoading] = useState(true);
  const [insightsLoading, setInsightsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch metrics data
  // Demonstrates study guide principle: client-side data fetching
  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/metrics`);
      if (!response.ok) {
        throw new Error('Failed to fetch metrics');
      }
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Fetch insights data
  const fetchInsights = async () => {
    try {
      setInsightsLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/insights`);
      if (!response.ok) {
        throw new Error('Failed to fetch insights');
      }
      const data = await response.json();
      setInsights(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setInsightsLoading(false);
    }
  };

  // Generate AI insights
  const generateInsights = async () => {
    try {
      setInsightsLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/insights/generate/all`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to generate insights');
      }
      const result = await response.json();
      
      // Refresh insights after generation
      await fetchInsights();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setInsightsLoading(false);
    }
  };

  // Refresh metrics from BigQuery
  const refreshMetrics = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/metrics/refresh`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to refresh metrics');
      }
      
      // Refresh metrics after refresh
      await fetchMetrics();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Load data on component mount
  // Demonstrates study guide principle: useEffect for data fetching
  useEffect(() => {
    fetchMetrics();
    fetchInsights();
  }, []);

  // Error state
  if (error) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <div className="text-error-600 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-neutral-900 mb-2">Error Loading Dashboard</h3>
          <p className="text-neutral-600 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold text-neutral-900">Analytics Dashboard</h2>
          <p className="text-neutral-600 mt-1">
            AI-powered insights from your business metrics
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <Button
            variant="outline"
            onClick={refreshMetrics}
            loading={loading}
            disabled={loading}
          >
            Refresh Metrics
          </Button>
          <Button
            onClick={generateInsights}
            loading={insightsLoading}
            disabled={insightsLoading}
          >
            Generate AI Insights
          </Button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div>
        <h3 className="text-lg font-semibold text-neutral-900 mb-4">Business Metrics</h3>
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="bg-neutral-200 rounded-lg h-32"></div>
              </div>
            ))}
          </div>
        ) : metrics.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-neutral-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-neutral-900 mb-2">No metrics available</h3>
            <p className="text-neutral-600 mb-4">
              Click "Refresh Metrics" to fetch data from BigQuery
            </p>
            <Button onClick={refreshMetrics}>
              Refresh Metrics
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {metrics.map((metric) => (
              <MetricCard
                key={metric.id}
                name={metric.name}
                value={metric.value}
                category={metric.category}
                description={metric.description}
                confidence={0.8} // Placeholder confidence
              />
            ))}
          </div>
        )}
      </div>

      {/* AI Insights Section */}
      <div>
        <h3 className="text-lg font-semibold text-neutral-900 mb-4">AI Insights</h3>
        <InsightPanel
          insights={insights}
          loading={insightsLoading}
        />
      </div>
    </DashboardLayout>
  );
}