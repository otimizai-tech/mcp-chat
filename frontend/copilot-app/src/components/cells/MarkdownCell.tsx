interface MarkdownCellProps {
  metadata: Record<string, any>;
  source: string[];
  onClick?: () => void;
}

export function MarkdownCell({ source, onClick }: MarkdownCellProps) {
  const content = source[0].replace(/^\*\*Canvas\*\*: /, '');
  
  return (
    <div className="flex justify-start">
      <div
        className="max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap break-words bg-white border border-gray-200 text-gray-800 rounded-bl-none cursor-pointer hover:bg-gray-50"
        onClick={onClick}
      >
        <span className="text-base">{content}</span>
        <div className="mt-2 text-xs text-gray-500">
          Click to edit in canvas
        </div>
      </div>
    </div>
  );
}
