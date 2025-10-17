/**
 * Button Component - demonstrates study guide principle: "Embrace Component Extraction"
 * 
 * Instead of repeating className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
 * in multiple places, this component encapsulates the styling and provides
 * a reusable, maintainable interface.
 */
import React from 'react';
import { cn } from '@/lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading = false, children, disabled, ...props }, ref) => {
    // Demonstrates study guide principle: design system usage
    // Using custom colors and spacing from tailwind.config.ts
    const baseClasses = "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50";
    
    const variants = {
      primary: "bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700",
      secondary: "bg-neutral-100 text-neutral-900 hover:bg-neutral-200 active:bg-neutral-300",
      outline: "border border-neutral-300 bg-transparent hover:bg-neutral-50 active:bg-neutral-100",
      ghost: "hover:bg-neutral-100 active:bg-neutral-200",
      danger: "bg-error-500 text-white hover:bg-error-600 active:bg-error-700",
    };
    
    const sizes = {
      sm: "h-8 px-3 text-sm",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
    };
    
    return (
      <button
        className={cn(
          baseClasses,
          variants[variant],
          sizes[size],
          loading && "opacity-50 cursor-not-allowed",
          className
        )}
        disabled={disabled || loading}
        ref={ref}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };
