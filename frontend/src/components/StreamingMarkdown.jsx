import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { CircularProgress } from './Progress';

const StreamingMarkdown = ({ content, isStreaming = false, streamingText = "Génération..." }) => {
  const [displayContent, setDisplayContent] = useState('');
  
  useEffect(() => {
    setDisplayContent(content || '');
  }, [content]);

  return (
    <div className="max-w-none text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer direction-rtl text-right leading-7">
      
      {/* NOUVELLE LOGIQUE D'AFFICHAGE */}
      {isStreaming && displayContent.length === 0 ? (
        // État 1: Streaming actif, mais aucun contenu reçu. On affiche un spinner.
        <div className='flex items-center justify-end gap-2 p-2'>
          <span className="text-bodyMedium italic text-light-onSecondaryContainer/80 dark:text-dark-onSecondaryContainer/80">
            {streamingText}
          </span>
          <CircularProgress size="small" />
        </div>
      ) : (
        // État 2: On affiche le contenu Markdown
        <>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ children }) => (
                <p className="mb-4 last:mb-0 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right leading-relaxed">
                  {children}
                </p>
              ),
              strong: ({ children }) => (
                <strong className="font-bold text-light-primary dark:text-dark-primary">
                  {children}
                </strong>
              ),
              em: ({ children }) => (
                <em className="italic text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer">
                  {children}
                </em>
              ),
              h1: ({ children }) => (
                <h1 className="text-2xl font-bold mb-6 mt-8 first:mt-0 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right border-b-2 border-light-primary/30 dark:border-dark-primary/30 pb-2">
                  {children}
                </h1>
              ),
              h2: ({ children }) => (
                <h2 className="text-xl font-bold mb-4 mt-6 first:mt-0 text-light-primary dark:text-dark-primary text-right bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh px-4 py-2 rounded-lg">
                  {children}
                </h2>
              ),
              h3: ({ children }) => (
                <h3 className="text-lg font-semibold mb-3 mt-5 first:mt-0 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right border-r-4 border-light-primary dark:border-dark-primary pr-3">
                  {children}
                </h3>
              ),
              h4: ({ children }) => (
                <h4 className="text-base font-semibold mb-2 mt-4 first:mt-0 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right">
                  {children}
                </h4>
              ),
              h5: ({ children }) => (
                <h5 className="text-sm font-semibold mb-2 mt-3 first:mt-0 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right">
                  {children}
                </h5>
              ),
              h6: ({ children }) => (
                <h6 className="text-xs font-semibold mb-2 mt-3 first:mt-0 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right">
                  {children}
                </h6>
              ),
              code: ({ node, inline, className, children, ...props }) => {
                return inline ? (
                  <code 
                    className="bg-light-tertiary/20 dark:bg-dark-tertiary/20 text-light-onTertiary dark:text-dark-onTertiary px-2 py-1 rounded text-sm font-mono font-semibold"
                    {...props}
                  >
                    {children}
                  </code>
                ) : (
                  <pre className="bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest p-4 rounded-lg overflow-x-auto my-4 border border-light-outline/20 dark:border-dark-outline/20">
                    <code className="text-light-onSurface dark:text-dark-onSurface text-sm font-mono" {...props}>
                      {children}
                    </code>
                  </pre>
                );
              },
              ul: ({ children }) => (
                <ul className="mr-6 mb-4 space-y-3 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right list-disc">
                  {children}
                </ul>
              ),
              ol: ({ children }) => (
                <ol className="mr-6 mb-4 space-y-3 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right list-decimal">
                  {children}
                </ol>
              ),
              li: ({ children }) => (
                <li className="text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right mb-2 leading-relaxed relative mr-4">
                  {children}
                </li>
              ),
              blockquote: ({ children }) => (
                <blockquote className="border-r-4 border-light-primary dark:border-dark-primary pr-4 mr-2 italic text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer my-6 bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh p-4 rounded-lg shadow-sm">
                  {children}
                </blockquote>
              ),
              table: ({ children }) => (
                <div className="overflow-x-auto my-6 rounded-lg border border-light-outline/20 dark:border-dark-outline/20">
                  <table className="min-w-full border-collapse">
                    {children}
                  </table>
                </div>
              ),
              th: ({ children }) => (
                <th className="border-b border-light-outline/30 dark:border-dark-outline/30 px-4 py-3 bg-light-primary/10 dark:bg-dark-primary/10 text-light-onSurface dark:text-dark-onSurface font-bold text-right">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="border-b border-light-outline/10 dark:border-dark-outline/10 px-4 py-3 text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer text-right">
                  {children}
                </td>
              ),
              a: ({ children, href, ...props }) => (
                <a 
                  className="text-light-primary dark:text-dark-primary underline hover:no-underline font-medium"
                  href={href}
                  {...props}
                >
                  {children}
                </a>
              ),
              hr: () => (
                <hr className="border-t-2 border-light-primary/30 dark:border-dark-primary/30 my-8 mx-8" />
              ),
            }}
          >
            {displayContent}
          </ReactMarkdown>
          
          {/* Le curseur n'apparaît que si du contenu est visible */}
          {isStreaming && displayContent.length > 0 && (
            <span className="inline-block w-0.5 h-5 bg-light-primary dark:bg-dark-primary ml-1 animate-pulse">
              |
            </span>
          )}
        </>
      )}
    </div>
  );
};

export default StreamingMarkdown;