/**
 * DashboardLayout Component - demonstrates study guide principle: "Embrace Component Extraction"
 * 
 * Main layout wrapper for the analytics dashboard
 * Uses Tailwind CSS utility classes with component extraction
 */
import React from 'react';
import { cn } from '@/lib/utils';

export interface DashboardLayoutProps {
  children: React.ReactNode;
  className?: string;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  className,
}) => {
  return (
    <div className={cn("min-h-screen bg-neutral-50", className)}>
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-neutral-900">
                Analytics Dashboard
              </h1>
              <span className="ml-2 px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                AI-Powered
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-neutral-600">
                Modern Tech Stack Demo
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-neutral-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-neutral-600">
            <p>
              Built with Next.js, FastAPI, BigQuery, SQLModel, and LangGraph
            </p>
            <p className="mt-1">
              Demonstrating modern tech stack principles from the study guide
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default DashboardLayout;
