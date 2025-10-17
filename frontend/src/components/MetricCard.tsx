/**
 * MetricCard Component - demonstrates study guide principle: "Embrace Component Extraction"
 * 
 * Displays a single metric with consistent styling and formatting
 * Uses Tailwind CSS utility classes with component extraction to avoid repetition
 */
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { cn } from '@/lib/utils';

export interface MetricCardProps {
  name: string;
  value: number;
  category: string;
  description?: string;
  trend?: 'up' | 'down' | 'stable';
  confidence?: number;
  className?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  name,
  value,
  category,
  description,
  trend,
  confidence,
  className,
}) => {
  // Demonstrates study guide principle: design system usage
  // Using custom colors and spacing from tailwind.config.ts
  const formatValue = (val: number) => {
    if (val >= 1000000) {
      return `${(val / 1000000).toFixed(1)}M`;
    } else if (val >= 1000) {
      return `${(val / 1000).toFixed(1)}K`;
    }
    return val.toFixed(2);
  };

  const getTrendColor = (trend?: string) => {
    switch (trend) {
      case 'up':
        return 'text-success-600';
      case 'down':
        return 'text-error-600';
      default:
        return 'text-neutral-600';
    }
  };

  const getTrendIcon = (trend?: string) => {
    switch (trend) {
      case 'up':
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 17l9.2-9.2M17 17V7H7" />
          </svg>
        );
      case 'down':
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 7l-9.2 9.2M7 7v10h10" />
          </svg>
        );
      default:
        return (
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
          </svg>
        );
    }
  };

  return (
    <Card variant="metric" className={cn("hover:shadow-card-hover transition-all duration-200", className)}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-neutral-700 truncate">
            {name}
          </CardTitle>
          {trend && (
            <div className={cn("flex items-center space-x-1", getTrendColor(trend))}>
              {getTrendIcon(trend)}
            </div>
          )}
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-neutral-500 uppercase tracking-wide">
            {category}
          </span>
          {confidence && (
            <span className="text-xs text-neutral-400">
              {Math.round(confidence * 100)}% confidence
            </span>
          )}
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="space-y-2">
          <div className="text-2xl font-bold text-neutral-900">
            {formatValue(value)}
          </div>
          {description && (
            <p className="text-xs text-neutral-600 leading-relaxed">
              {description}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default MetricCard;
