/**
 * InsightPanel Component - demonstrates study guide principle: "Embrace Component Extraction"
 * 
 * Displays AI-generated insights with consistent styling and formatting
 * Uses Tailwind CSS utility classes with component extraction
 */
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { cn } from '@/lib/utils';

export interface Insight {
  id: number;
  text: string;
  type: 'trend' | 'risk' | 'opportunity' | 'recommendation' | 'observation';
  confidence: number;
  created_at: string;
}

export interface InsightPanelProps {
  insights: Insight[];
  loading?: boolean;
  className?: string;
}

const InsightPanel: React.FC<InsightPanelProps> = ({
  insights,
  loading = false,
  className,
}) => {
  // Demonstrates study guide principle: design system usage
  // Using custom colors and spacing from tailwind.config.ts
  const getInsightTypeColor = (type: string) => {
    switch (type) {
      case 'trend':
        return 'bg-primary-100 text-primary-800 border-primary-200';
      case 'risk':
        return 'bg-error-100 text-error-800 border-error-200';
      case 'opportunity':
        return 'bg-accent-100 text-accent-800 border-accent-200';
      case 'recommendation':
        return 'bg-warning-100 text-warning-800 border-warning-200';
      default:
        return 'bg-neutral-100 text-neutral-800 border-neutral-200';
    }
  };

  const getInsightTypeIcon = (type: string) => {
    switch (type) {
      case 'trend':
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        );
      case 'risk':
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'opportunity':
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'recommendation':
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        );
      default:
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        );
    }
  };

  if (loading) {
    return (
      <Card variant="insight" className={cn("animate-pulse", className)}>
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-neutral-700">
            AI Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="space-y-2">
                <div className="h-4 bg-neutral-200 rounded w-3/4"></div>
                <div className="h-3 bg-neutral-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (insights.length === 0) {
    return (
      <Card variant="insight" className={cn(className)}>
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-neutral-700">
            AI Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <svg className="mx-auto h-12 w-12 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-neutral-900">No insights available</h3>
            <p className="mt-1 text-sm text-neutral-500">
              Generate AI insights to see intelligent analysis of your metrics.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card variant="insight" className={cn(className)}>
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-neutral-700">
          AI Insights ({insights.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {insights.map((insight) => (
            <div
              key={insight.id}
              className="p-4 rounded-lg border bg-white shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start space-x-3">
                <div className={cn(
                  "flex-shrink-0 p-2 rounded-full border",
                  getInsightTypeColor(insight.type)
                )}>
                  {getInsightTypeIcon(insight.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-2">
                    <span className={cn(
                      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border",
                      getInsightTypeColor(insight.type)
                    )}>
                      {insight.type.charAt(0).toUpperCase() + insight.type.slice(1)}
                    </span>
                    <span className="text-xs text-neutral-500">
                      {Math.round(insight.confidence * 100)}% confidence
                    </span>
                  </div>
                  <p className="text-sm text-neutral-900 leading-relaxed">
                    {insight.text}
                  </p>
                  <p className="mt-2 text-xs text-neutral-500">
                    {new Date(insight.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default InsightPanel;
